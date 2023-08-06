# pytools 
[![Build Status](https://app.travis-ci.com/mauriciodoerr/pytools.svg?branch=main)](https://app.travis-ci.com/mauriciodoerr/pytools) 
[![Updates](https://pyup.io/repos/github/mauriciodoerr/pytools/shield.svg)](https://pyup.io/repos/github/mauriciodoerr/pytools/)
[![Python 3](https://pyup.io/repos/github/mauriciodoerr/pytools/python-3-shield.svg)](https://pyup.io/repos/github/mauriciodoerr/pytools/)

Code samples regarding the module Pytools from DevPro Platform

Supported Python version 3

1. [Implemented Libs](https://github.com/mauriciodoerr/pytools#implemented-libs)
2. [Installing](https://github.com/mauriciodoerr/pytools#installing)
3. [Useful Commands](https://github.com/mauriciodoerr/pytools#useful-python-commands)
   - [Virtual Environment](https://github.com/mauriciodoerr/pytools#create-and-activate-venv)
   - [PyPi Local Lib](https://github.com/mauriciodoerr/pytools#install-pypi-local-lib1)
   - [Publish at PyPi](https://github.com/mauriciodoerr/pytools#publish-at-pypi)
## Implemented Libs:
- Requests: HTTP for Humans™

## Installing

```console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Check for Code Quality following PEP8, execute:
```console
flake8
```

## Useful Python commands

#### Create and activate venv

```console
python3 -m venv .venv
source .venv/bin/activate
```

#### Install PyPi local Lib[^1]

```console
pip install -e "path to setup.py inside the lib"
```
> E.g. pip install -e ./pytools

Validate installation
```console
python3
from libhttprequests.github_api import get_github_avatar
get_github_avatar('mauriciodoerr')
```

#### Publish at PyPi
```console
python3 setup.py sdist
pip install twine
twine upload dist/*
```

[^1]: List Classifiers for PyPi can be found at https://pypi.org/pypi?%3Aaction=list_classifiers
