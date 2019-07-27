aeidon
======

aeidon is a Python package for reading, writing and manipulating
text-based subtitle files. It is used by the gaupol package, which
provides a subtitle editor with a GTK+ user interface.

Separating a user interface independent general-purpose subtitle editing
package from Gaupol has been an afterthought and thus not well designed
to be a reusable component, but on the other hand is proven, working and
maintained code.

API Documentation: https://otsaloma.io/gaupol/doc/api/aeidon.html

## Installation

To install only either the aeidon or the gaupol package, use one of the
following commands

    sudo python3 setup.py --without-gaupol install --prefix=/usr/local
    sudo python3 setup.py --without-aeidon install --prefix=/usr/local

Note that the `--with-*` and `--without-*` are global options and must
be placed before any commands.

## Dependencies

Of the dependencies listed in the [`README.md`](README.md) file, Python,
iso-codes and chardet are to be associated with aeidon. If aeidon is
installed using the `--without-iso-codes` switch, then iso-codes is
required instead of optional. gaupol should depend on the remaining
dependencies as well as aeidon of the same version.
