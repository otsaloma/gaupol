#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cx_Freeze installation routines built on top of normal setup.py."""
import os, site, sys

os.environ["GAUPOL_FREEZING"] = "1"
from setup import *
import cx_Freeze

includes = ("aeidon", "gaupol", "gi")
include_files = []
gtk_path = os.path.join(site.getsitepackages()[1], "gtk")
# XXX: How the fuck do we find out which DLLs are actually needed?
for dll in glob.glob("{}\\*.dll".format(gtk_path)):
    include_files.append((dll, os.path.basename(dll)))
for lib in ("etc", "lib", "share"):
    include_files.append((os.path.join(gtk_path, lib), lib))
include_files.append(("build/usr/share", "share"))

setup_kwargs.update(dict(
    options=dict(build_exe=dict(compressed=False,
                                includes=includes,
                                packages=includes,
                                include_files=include_files)),

    executables=[cx_Freeze.Executable(script="bin/gaupol",
                                      base="Win32GUI",
                                      icon="data/icons/gaupol.ico")],

))

if __name__ == "__main__":
    cx_Freeze.setup(**setup_kwargs)
