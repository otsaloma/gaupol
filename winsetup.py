#!/usr/bin/env python

"""
py2exe installation routines built on top of normal setup.py.

All translatable data are expected to have been precompiled with 'msgfmt' and
'intltool-merge' on a Unix system where they conveniently available. For
creating the complete bundled installer, see the file tools/py2exe.bat.
"""
# pylint: disable-msg=W0614

from setup import *
import py2exe

def add_translated_gettext_files(data_files):
    """Add translated gettext po files to data_files."""

    for locale in os.listdir("locale"):
        src = "locale/%s/LC_MESSAGES/gaupol.mo" % locale
        dst = "share/locale/%s/LC_MESSAGES" % locale
        data_files.append((dst, (src,)))

def add_translated_extension_files(data_files):
    """Add translated extension metadata files to data_files."""

    for extension in os.listdir("extensions"):
        files = [x[:-3] for x in glob.glob("extensions/%s/*.in" % extension)]
        data_files.append(("share/gaupol/extensions/%s" % extension, files))

def add_translated_pattern_files(data_files):
    """Add translated pattern files to data_files."""

    paths = [x[:-3] for x in glob.glob("data/patterns/*.in")]
    return [("share/gaupol/patterns", paths)]

add_translated_gettext_files(setup_kwargs["data_files"])
add_translated_extension_files(setup_kwargs["data_files"])
add_translated_pattern_files(setup_kwargs["data_files"])

setup_kwargs.update(dict(
    windows=[dict(
        script="bin/gaupol",
        icon_resources=[(0, "data/icons/gaupol.ico")])],
    py2exe_options=dict(
        includes=["atk",],
        packages=[
            "cairo",
            "chardet",
            "enchant",
            "gaupol",
            "gobject",
            "gtk",
            "pangocairo",
            "pygtk",])))

if __name__ == "__main__":
    setup(**setup_kwargs)
