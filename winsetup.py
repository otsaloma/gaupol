#!/usr/bin/env python3

"""cx_Freeze installation routines built on top of setup.py."""

import cx_Freeze
import glob
import os
import site

from setup import setup_kwargs

include_files = [(os.path.join("build", "usr", "share"), "share")]
gnome_dir = os.path.join(site.getsitepackages()[1], "gnome")
for dll in sorted(glob.glob("{}/*.dll".format(gnome_dir))):
    include_files.append((dll, os.path.basename(dll)))
include_files.append((os.path.join(gnome_dir, "etc"), "etc"))
include_files.append((os.path.join(gnome_dir, "lib"), "lib"))
include_files.append((os.path.join(gnome_dir, "share"), "share"))

setup_kwargs.update({
    "options": {"build_exe": {
        "compressed": False,
        "include_files": include_files,
        "includes": ["aeidon", "cairo", "gaupol", "gi"],
        "packages": ["aeidon", "cairo", "gaupol", "gi"],
    }},
    "executables": [cx_Freeze.Executable(
        script="bin/gaupol",
        base="WIN32GUI",
        icon="data/icons/io.otsaloma.gaupol.ico",
    )],
})

if __name__ == "__main__":
    cx_Freeze.setup(**setup_kwargs)
    # Enable header bars on builtin GTK dialogs.
    path = glob.glob("build/exe.*/etc/gtk-3.0/settings.ini")[0]
    with open(path, "a", encoding="us_ascii") as f:
        f.write("\ngtk-dialogs-use-header = 1\n")
