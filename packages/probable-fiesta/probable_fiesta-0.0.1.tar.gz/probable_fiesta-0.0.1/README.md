# probable-fiesta

> There's probably a fiesta somewhere.

Python Package Core 

A Python package core for building a Python package.

## Installation

## Installation using pip


```bash
pip install probable-fiesta
```

## Installation with automatic build and install


> It is recommended to setup a [virtual environment](https://docs.python.org/3/library/venv.html).

To install locally with automatic build and install, run the following command in the root directory of the project.

```bash
git clone https://github.com/sergio-munoz/probable-fiesta.git
cd probable-fiesta
chmod +x scripts/build_install.sh
./scripts/build_install.sh
```

## Installation with manual build and install

Setup a new virtual environment and install packages in `requirements.txt`.

```bash
python -m venv build_venv
source build_venv/bin/activate
(build_venv) $ pip install -r build_requirements.txt
(build_venv) $ hatch build
(build_venv) $ pip install dist/probable_fiesta-${VERSION}.tar.gz
```

### Installation in Jupyter Notebook

To install the into the Jupyter Notebook kernel:

```bash
import sys
!{sys.executable} -m pip install -U --no-deps probable-fiesta
```

## Usage

```bash
probable_fiesta --help
```

## Build and Run

### Build and Run command

Build and a command. Pass flags, for example `--version`:

```bash
./scripts/build_install.sh & probable_fiesta --version
```


