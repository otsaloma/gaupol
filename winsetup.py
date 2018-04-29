#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cx_Freeze installation routines built on top of normal setup.py."""

import glob
import os
import site

os.environ["GAUPOL_FREEZING"] = "1"
from setup import setup_kwargs
import cx_Freeze

includes = ["aeidon", "cairo", "gaupol", "gi"]
include_files = [(os.path.join("build", "usr", "share"), "share")]
site_path = site.getsitepackages()[1]

gnome_path = os.path.join(site_path, "gnome")
for dll in glob.glob("{}/*.dll".format(gnome_path)):
    include_files.append((dll, os.path.basename(dll)))
include_files.append((os.path.join(gnome_path, "etc"), "etc"))
include_files.append((os.path.join(gnome_path, "lib"), "lib"))
include_files.append((os.path.join(gnome_path, "share"), "share"))

# PyEnchant ships with DLLs provided by pygi-aio as well.
# Keep the pygio-aio DLLs, but add PyEnchant data files.
enchant_path = os.path.join(site_path, "enchant")
include_files.append((os.path.join(enchant_path, "lib"), "lib"))
include_files.append((os.path.join(enchant_path, "share"), "share"))

setup_kwargs.update(dict(
    options=dict(build_exe=dict(
        compressed=False,
        includes=includes,
        packages=includes,
        include_files=include_files,
    )),
    executables=[cx_Freeze.Executable(
        script="bin/gaupol",
        base="WIN32GUI",
        icon="data/icons/gaupol.ico",
    )],
))

def patch_build():
    # Enable header bars on builtin GTK+ dialogs.
    path = glob.glob("build/exe.*/etc/gtk-3.0/settings.ini")[0]
    print("patching {}".format(path))
    with open(path, "a", encoding="us_ascii") as f:
        f.write("\ngtk-dialogs-use-header = 1\n")

if __name__ == "__main__":
    cx_Freeze.setup(**setup_kwargs)
    patch_build()
