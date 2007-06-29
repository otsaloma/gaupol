#!/usr/bin/env python

"""
Relevant customizations in this file
 (1) gaupol.paths module
 (2) Translations

(1) Gaupol finds non-Python files based on the paths written in module
    gaupol.paths. In gaupol/paths.py the paths default to the ones in the
    source directory. During installation the file gets rewritten to
    build/gaupol/paths.py with the installation paths and that file will be
    installed. The paths are based on variable 'install_data' with the 'root'
    variable stripped if it is given. If doing distro-packaging, make sure this
    file gets correctly written.

(2) During installation, the .po files are compiled and the desktop file is
    translated. This requires gettext and intltool, more specifically,
    executables 'msgfmt' and 'intltool-merge' in $PATH.
"""

# pylint: disable-msg=W0621


from __future__ import with_statement

import glob
import os
import shutil
import sys
import tarfile
import tempfile

from distutils import dir_util
from distutils.command.clean import clean
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.command.sdist import sdist
from distutils.core import setup
from distutils.log import info

os.chdir(os.path.dirname(__file__) or ".")
sys.path.insert(0, os.path.dirname(__file__))
from gaupol import __version__


class Clean(clean):

    def finalize_options(self):

        clean.finalize_options(self)
        if self.dry_run:
            raise SystemExit("--dry-run not supported")

    def run(self):

        clean.run(self)

        desktop_file = os.path.join("data", "gaupol.desktop")
        for path in ("MANIFEST", desktop_file):
            if os.path.isfile(path):
                info("removing '%s'" % path)
                os.remove(path)

        info("removing .pyc and .pyo files under 'gaupol'")
        for (root, dirs, files) in os.walk("gaupol"):
            for name in (x for x in files if x.endswith((".pyc", ".pyo"))):
                os.remove(os.path.join(root, name))

        for path in ("build", "dist", "locale"):
            if os.path.isdir(path):
                dir_util.remove_tree(path)


class InstallData(install_data):

    def __get_desktop_file(self):

        path = os.path.join("data", "gaupol.desktop")
        os.system("intltool-merge -d po %s.in %s" % (path, path))
        return [("share/applications", [path])]

    def __get_mo_files(self):

        mo_files = []
        for po_file in glob.glob("po/*.po"):
            locale = os.path.basename(po_file[:-3])
            mo_dir = os.path.join("locale", locale, "LC_MESSAGES")
            mo_file = os.path.join(mo_dir, "gaupol.mo")
            dest_dir = os.path.join("share", mo_dir)
            if not os.path.isdir(mo_dir):
                info("creating %s" % mo_dir)
                os.makedirs(mo_dir)
            info("compiling '%s'" % mo_file)
            os.system("msgfmt %s -o %s" % (po_file, mo_file))
            if os.path.isfile(mo_file):
                mo_files.append((dest_dir, [mo_file]))
        return mo_files

    def run(self):

        # Translate files and add them to data files.
        self.data_files.extend(self.__get_mo_files())
        self.data_files.extend(self.__get_desktop_file())

        install_data.run(self)


class InstallLib(install_lib):

    def install(self):

        # Allow --root to be used as a destination directory.
        root = self.distribution.get_command_obj("install").root
        parent = self.distribution.get_command_obj("install").install_data
        if root is not None:
            root = os.path.abspath(root)
            parent = os.path.abspath(parent).replace(root, "")
        data_dir = os.path.join(parent, "share", "gaupol")
        locale_dir = os.path.join(parent, "share", "locale")
        profile_dir = 'os.path.join(os.path.expanduser("~"), ".gaupol")'

        # Write gaupol.paths module.
        path = os.path.join(self.build_dir, "gaupol", "paths.py")
        with open(path, "w") as fobj:
            fobj.write("import os\n\n")
            fobj.write("DATA_DIR = %r\n" % data_dir)
            fobj.write("LOCALE_DIR = %r\n" % locale_dir)
            fobj.write("PROFILE_DIR = %s\n" % profile_dir)

        return install_lib.install(self)


class SDistGna(sdist):

    description = "create source distribution for gna.org"

    def finalize_options(self):

        sdist.finalize_options(self)

        # Set distribution directory to "dist/X.Y".
        # pylint: disable-msg=W0201
        self.dist_dir = os.path.join(self.dist_dir, __version__[:3])

    def run(self):

        sdist.run(self)
        basename = "gaupol-%s" % __version__
        tarballs = os.listdir(self.dist_dir)
        os.chdir(self.dist_dir)

        # Compare tarball contents with working copy.
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)
        tarfile.open(tarballs[-1], "r").extractall(temp_dir)
        info("comparing tarball (tmp) with working copy (../..)")
        os.system('diff -qr -x ".*" -x "*.pyc" ../.. %s' % test_dir)
        response = raw_input("Are all files in the tarball [Y/n]? ")
        if response.lower() == "n":
            raise SystemExit("Must edit MANIFEST.in.")

        # Create extra distribution files.
        info("calculating md5sums")
        os.system("md5sum * > %s.md5sum" % basename)
        info("creating '%s.changes'" % basename)
        source = os.path.join("..", "..", "ChangeLog")
        shutil.copyfile(source, "%s.changes" % basename)
        info("creating '%s.news'" % basename)
        source = os.path.join("..", "..", "NEWS")
        shutil.copyfile(source, "%s.news" % basename)
        for tarball in tarballs:
            info("signing '%s'" % tarball)
            os.system("gpg --detach %s" % tarball)

        # Create latest.txt.
        os.chdir("..")
        info("creating 'latest.txt'")
        with open("latest.txt", "w") as fobj:
            fobj.write("%s\n" % __version__)


packages = []
for (root, dirs, files) in os.walk("gaupol"):
    if os.path.isfile(os.path.join(root, "__init__.py")):
        path = root.replace(os.sep, ".")
        path = path[path.find("gaupol"):]
        if not path.endswith(".test"):
            packages.append(path)
packages.remove("gaupol.unittest")
packages.remove("gaupol.gtk.unittest")

data_files = [
    ("share/gaupol", ["data/conf.spec", "data/gtkrc", "data/ui.xml"]),
    ("share/gaupol/glade", glob.glob("data/glade/*.glade")),
    ("share/gaupol/headers", glob.glob("data/headers/*.txt")),
    ("share/man/man1", ["doc/gaupol.1"]),]

for name in ("16x16", "22x22", "24x24", "32x32", "scalable"):
    directory = "share/icons/hicolor/%s/apps" % name
    files = glob.glob("data/icons/hicolor/%s/apps/*.png" % name)
    files += glob.glob("data/icons/hicolor/%s/apps/*.svg" % name)
    data_files.append((directory, files))

setup(
    name="gaupol",
    version=__version__,
    requires=["gtk (>=2.10.0)"],
    platforms=["Platform Independent"],
    author="Osmo Salomaa",
    author_email="otsaloma@cc.hut.fi",
    url="http://home.gna.org/gaupol/",
    description="Subtitle editor",
    license="GPL",
    packages=packages,
    scripts=["bin/gaupol"],
    data_files=data_files,
    cmdclass={
        "clean": Clean,
        "install_data": InstallData,
        "install_lib": InstallLib,
        "sdist_gna": SDistGna},)
