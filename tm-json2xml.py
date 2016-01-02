#!/usr/bin/env python
#
# Copyright (C) 2015 minedev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Converts a set of JSON files to a TextMate compliant XML format.

The goal of this script is to ease the development of TextMate configuration
files by converting more the human readable JSON to TextMate compliant XML.
"""


from __future__ import print_function
from optparse import OptionParser
import codecs
import json
import collections
from xml.dom import minidom
import uuid
import os.path


def json2xml(json_data, make_uuid=False):
	"""Convert json data to TextMate compliant xml"""

	data = json.loads(json_data, object_pairs_hook=collections.OrderedDict)

	imp = minidom.DOMImplementation()
	doctype = imp.createDocumentType("plist",
		"-//Apple Computer//DTD PLIST 1.0//EN",
		"http://www.apple.com/DTDs/PropertyList-1.0.dtd")

	document = imp.createDocument("", "plist", doctype)

	plist = document.documentElement
	plist.setAttribute("version", "1.0")
	document.appendChild(plist)

	generate_xml_tree(plist, data, document)

	if make_uuid and len(plist.childNodes) > 0:
		first_child = plist.childNodes[0]

		key = create_text_node(document, "key", "uuid")
		value = create_text_node(document, "string", str(uuid.uuid1()))

		first_child.appendChild(key)
		first_child.appendChild(value)

	return document.toprettyxml(indent="    ", encoding="UTF-8")


def create_text_node(document, tag_name, text):
	"""Create an element with a text node containing the text"""

	node = document.createElement(tag_name)
	node_text = document.createTextNode(text)

	node.appendChild(node_text)

	return node


def generate_xml_tree(tree, data, document):
	"""Recursively traverse the data to create the xml tree"""
	data_type = type(data)

	if data_type is dict or data_type is collections.OrderedDict:
		dictionary = document.createElement("dict")

		for key in data.keys():
			key_node = create_text_node(document, "key", key)
			dictionary.appendChild(key_node)

			generate_xml_tree(dictionary, data[key], document)

		tree.appendChild(dictionary)
	elif data_type is list:
		array = document.createElement("array")

		for e in data:
			generate_xml_tree(array, e, document)

		tree.appendChild(array)
	else:
		plain = create_text_node(document, "string", str(data))
		tree.appendChild(plain)


def convert_file(path, uuid=False, extension="tm", override=False):
	"""Convert a file to a TextMate compliant format.

	Optionally generate an uuid.
	"""

	with codecs.open(path, "r", encoding="utf-8") as source_file:
		json_data = source_file.read()

	xml = json2xml(json_data, uuid)

	dot_index = path.rfind(".")

	if dot_index > 0:
		path = path[:dot_index]

	path += "." + extension

	if os.path.exists(path) and not override:
		raise IOError("Output file (%s) already exists" % path)

	with codecs.open(path, "wb", encoding="utf-8") as dest_file:
		dest_file.write(xml.decode("utf-8"))


if __name__ == "__main__":
	parser = OptionParser(usage="Usage: %prog [options] file1.json file2.json ...")

	parser.add_option("-u", "--uuid",
		action="store_true",
		dest="uuid",
		help="Add a generated UUID to the json data")

	parser.add_option("-o", "--override",
		action="store_true",
		dest="override",
		help="Override existing files")

	parser.add_option("-e", "--ext",
		dest="extension",
		metavar="EXT",
		help="Change the extension of the generated files")

	(options, args) = parser.parse_args()

	if len(args) == 0:
		parser.print_help()
	else:
		extension = options.extension if options.extension else "tm"

		for element in args:
			try:
				convert_file(element, options.uuid, extension, options.override)
			except Exception as exception:
				print("%s: %s" % (element, str(exception)))
