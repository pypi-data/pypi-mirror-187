# Functions

This is a gigantic folder, with multiple functions for multiple use cases. The only folder that you will need, is [PythonFunctions](./src/PythonFunctions/).

## Documentation

Every file has it own documentation, which can be found here: [Documentation](https://python-functions.readthedocs.io/en/latest/).

## Expanding

This file is still in development and more is to come! If you want to contribute, follow the same file structure and submit a pull request.
What you see now is not the final version.

## Contributing

Please read [Contributing.md](Contribution.md)

## Update Log

### 1.1.10

- Updated `Version.py` to not do anything if the setting says it should be muted.

### 1.1.9

- Updated tests
- Fixed an issue with `None` or `''` being passed into os.makedirs in `src/PythonFunctions/SaveModules/NORMAL.py`
- Added `__main__.py` with `-s` and `-v` arguments. (`-s` generates `PyFuncSet.json` file, `-v` prints the module version)
- Updated `Version.py` to not run at start (the out of data check) unless mainally called.
- Updated `__init__.py` to accomodate for `Version.py` changes
- Added `CreateStringVar` to `ui.py` for easy creation of string variables (without having to also import tk into your module)
- Updated documentation
- Removed old documentation (A: online is more up to date. B: If you have the source code, you can view the online version even if offline)
- Updated contributing information

Updates before 1.1.9 are in [Updatelog.md](Updatelog.md)

## Credits

This project uses functions and modules from other people to run. Most of the modules have been auto imported (and kept up to date) but some require you to manually install them (check that module infomation).

### Colourama

[Github](https://github.com/tartley/colorama)
Brings colours to the terminal

### Readchar

[Github](https://github.com/magmax/python-readchar)
Taking an input straight away, instead of getting the user to press enter afterwards

### Cryptography

[Github](https://github.com/pyca/cryptography)
Encrypting and decrypting data. Quick and simple

### Requests

[Github](https://github.com/psf/requests)
Checking if you have the latest version
