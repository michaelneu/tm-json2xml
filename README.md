# tm-json2xml [![Build Status](https://travis-ci.org/michaelneu/tm-json2xml.svg?branch=master)](https://travis-ci.org/michaelneu/tm-json2xml)

tm-json2xml is a Python script to help you write more readable XML configuration files. It converts a set of JSON files to TextMate compliant XML format using built-in Python libs. 

## Usage
You can use tm-json2xml like a regular script because of it using the `optparse` library internally. 

```
$ python tm-json2xml.py
Usage: tm-json2xml.py [options] file1.json file2.json ...

Options:
  -h, --help         show this help message and exit
  -u, --uuid         Add a generated UUID to the json data
  -o, --override     Override existing files
  -e EXT, --ext=EXT  Change the extension of the generated files
```

## Contributing
As you can see in the [`.travis.yml`](.travis.yml) file, tm-json2xml uses `flake8` to ensure a consistent code style. Also note that the line limit is set to 80 characters but tabs are used. 

## License
tm-json2xml is licensed under the [MIT-License](LICENSE). 
