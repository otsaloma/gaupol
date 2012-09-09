#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

"""py2exe installation routines built on top of normal setup.py."""

from setup import *

includes = ("aeidon",
            "chardet",
            "enchant",
            "gaupol",
            "gi.repository.GLib",
            "gi.repository.GObject",
            "gi.repository.Gtk",
            )

setup_kwargs.update(dict(
    windows=[dict(script="bin/gaupol",
                  icon_resources=[(0, "data/icons/gaupol.ico")])],

    options=dict(py2exe=dict(includes=list(includes),
                             packages=list(includes)))))

if __name__ == "__main__":
    distutils.core.setup(**setup_kwargs)
