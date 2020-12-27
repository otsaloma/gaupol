Python Package aeidon for Subtitles
===================================

[![PyPI](https://img.shields.io/pypi/v/aeidon.svg)](https://pypi.org/project/aeidon/)

aeidon is a Python package that provides classes and functions for
dealing with text-based subtitle files of many different formats.
Functions exist for reading and writing subtitle files as well as
manipulating subtitle data, i.e. positions (times or frames) and texts.

## Installation

The latest stable release is available via PyPI.

```bash
pip install -U aeidon
```

## Documentation

https://otsaloma.io/gaupol/doc/api/aeidon.html

## Distro-Packaging

When packaging both aeidon and gaupol in a Linux distro, it's best to
use the switches in the main `setup.py` for a consistent whole.

    sudo python3 setup.py --without-gaupol install --prefix=/usr/local
    sudo python3 setup.py --without-aeidon install --prefix=/usr/local

Note that the `--with-*` and `--without-*` are global options and must
be placed before any commands.

Of the dependencies listed in the [`README.md`](README.md) file,
iso-codes and chardet are to be associated with aeidon. If aeidon is
installed using the `--without-iso-codes` switch, then iso-codes is
required instead of optional. gaupol should depend on the remaining
dependencies as well as aeidon of the same version.

## History

The aeidon package is part of the Gaupol subtitle editor, where the
other package, gaupol, provides the GTK user interface.

Separating a user interface independent general-purpose subtitle editing
package from Gaupol has been an afterthought and thus not well designed
to be a reusable component, but on the other hand is proven, working and
maintained code.
