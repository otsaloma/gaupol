#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cx_Freeze installation routines built on top of normal setup.py."""
import os, site

os.environ["GAUPOL_FREEZING"] = "1"
from setup import *
import cx_Freeze

includes = ["aeidon", "gaupol", "gi"]
include_files = [(os.path.join("build", "usr", "share"), "share")]
site_path = site.getsitepackages()[1]

gnome_path = os.path.join(site_path, "gnome")
for dll in glob.glob("{}\\*.dll".format(gnome_path)):
    include_files.append((dll, os.path.basename(dll)))
for lib in ("etc", "lib", "share"):
    include_files.append((os.path.join(gnome_path, lib), lib))

enchant_path = os.path.join(site_path, "enchant")
for dll in glob.glob("{}\\*.dll".format(enchant_path)):
    include_files.append((dll, os.path.basename(dll)))
for lib in ("lib", "share"):
    include_files.append((os.path.join(enchant_path, lib), lib))

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
