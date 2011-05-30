#!/usr/bin/env python

"""py2exe installation routines built on top of normal setup.py."""

# pylint: disable=W0614
from setup import *

includes = ("aeidon",
            "atk",
            "cairo",
            "chardet",
            "enchant",
            "gaupol",
            "gio",
            "glib",
            "gobject",
            "gtk",
            "pango",
            "pangocairo",
            "pygtk",
            )

setup_kwargs.update(dict(
    windows=[dict(script="bin/gaupol",
                  icon_resources=[(0, "data/icons/gaupol.ico")])],

    options=dict(py2exe=dict(includes=list(includes),
                             packages=list(includes)))))

if __name__ == "__main__":
    distutils.core.setup(**setup_kwargs)
