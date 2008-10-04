#!/usr/bin/env python

"""
There are two relevant customizations to the standard distutils installation
process: (1) writing the gaupol.paths module and (2) handling translations.

(1) Gaupol finds non-Python files based on the paths written in module
    gaupol.paths. In gaupol/paths.py the paths default to the ones in the
    source directory. During the 'install_lib' command the file gets rewritten
    to build/gaupol/paths.py with the installation paths and that file will be
    installed. The paths are based on variable 'install_data' with the 'root'
    variable stripped if it is given. If doing distro-packaging, make sure this
    file gets correctly written.

(2) During installation, the .po files are compiled into .mo files, the desktop
    file and pattern files are translated. This requires gettext and intltool,
    more specifically, executables 'msgfmt' and 'intltool-merge' in $PATH.
"""

# pylint: disable-msg=W0621

from __future__ import with_statement

import glob
import itertools
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

if "py2exe" in sys.argv:
    import py2exe

from distutils import dir_util, log
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.command.sdist import sdist
from distutils.core import setup

os.chdir(os.path.dirname(__file__) or ".")
sys.path.insert(0, os.path.dirname(__file__))
from gaupol import __version__


class Clean(clean):

    """Command to remove files and directories created."""

    __glob_targets = (
        "build", "dist", "locale",
        "ChangeLog", "MANIFEST",
        "data/gaupol.desktop",
        "data/patterns/*.common-error",
        "data/patterns/*.hearing-impaired",
        "data/patterns/*.line-break",
        "data/patterns/*.capitalization",)

    def run(self):
        """Remove files and directories listed in self.__targets."""

        clean.run(self)

        log.info("removing .pyc and .pyo files under 'gaupol'")
        for (root, dirs, files) in os.walk("gaupol"):
            for name in (x for x in files if x.endswith((".pyc", ".pyo"))):
                path = os.path.join(root, name)
                if not self.dry_run: os.remove(path)

        targets = [glob.glob(x) for x in self.__glob_targets]
        iterator = itertools.chain(*targets)
        for target in (x for x in iterator if os.path.isdir(x)):
            dir_util.remove_tree(target, dry_run=self.dry_run)
        iterator = itertools.chain(*targets)
        for target in (x for x in iterator if os.path.isfile(x)):
            log.info("removing '%s'" % target)
            if not self.dry_run: os.remove(target)


class Install(install):

    """Command to install everything."""

    def run(self):
        """Install everything and update the desktop file database."""

        install.run(self)

        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        data_dir = get_command_obj("install_data").install_dir
        # Assume we're actually installing if --root was not given.
        if (root is not None) or (data_dir is None): return

        directory = os.path.join(data_dir, "share", "applications")
        log.info("updating desktop database in '%s'" % directory)
        try: subprocess.call(("update-desktop-database", directory))
        except OSError: log.info("...failed")


class InstallData(install_data):

    """Command to install data files."""

    def __get_desktop_file(self):
        """Return a tuple for the translated desktop file."""

        path = os.path.join("data", "gaupol.desktop")
        os.system("intltool-merge -d po %s.in %s" % (path, path))
        return ("share/applications", (path,))

    def __get_mo_file(self, po_file):
        """Return a tuple for the compiled .mo file."""

        locale = os.path.basename(po_file[:-3])
        mo_dir = os.path.join("locale", locale, "LC_MESSAGES")
        if not os.path.isdir(mo_dir):
            log.info("creating %s" % mo_dir)
            os.makedirs(mo_dir)
        mo_file = os.path.join(mo_dir, "gaupol.mo")
        dest_dir = os.path.join("share", mo_dir)
        log.info("compiling '%s'" % mo_file)
        os.system("msgfmt %s -o %s" % (po_file, mo_file))
        return (dest_dir, (mo_file,))

    def __get_pattern_file(self, pattern_file):
        """Return a tuple for the translated pattern file."""

        assert pattern_file.endswith(".in")
        path = pattern_file[:-3]
        os.system("intltool-merge -d po %s.in %s" % (path, path))
        return ("share/gaupol/patterns", (path,))

    def run(self):
        """Install data files after translating them."""

        if "py2exe" in sys.argv:
            # Do not try compiling translations on Windows,
            # instead expect them to have been precompiled.
            return install_data.run(self)
        for po_file in glob.glob("po/*.po"):
            self.data_files.append(self.__get_mo_file(po_file))
        for pattern_file in glob.glob("data/patterns/*.in"):
            self.data_files.append(self.__get_pattern_file(pattern_file))
        self.data_files.append(self.__get_desktop_file())
        return install_data.run(self)


class InstallLib(install_lib):

    """Command to install library files."""

    def install(self):
        """Install library files after writing changes."""

        # Allow --root to be used as a destination directory.
        root = self.distribution.get_command_obj("install").root
        parent = self.distribution.get_command_obj("install").install_data
        if root is not None:
            root = os.path.abspath(root)
            parent = os.path.abspath(parent)
            parent = parent.replace(root, "")
        data_dir = os.path.join(parent, "share", "gaupol")
        locale_dir = os.path.join(parent, "share", "locale")

        # Write changes to the gaupol.paths module.
        path = os.path.join(self.build_dir, "gaupol", "paths.py")
        text = open(path, "r").read()
        string = 'get_directory("data")'
        text = text.replace(string, repr(data_dir))
        assert text.count(repr(data_dir)) > 0
        string = 'get_directory("locale")'
        text = text.replace(string, repr(locale_dir))
        assert text.count(repr(locale_dir)) > 0
        open(path, "w").write(text)

        return install_lib.install(self)


class SDistGna(sdist):

    description = "create source distribution for gna.org"

    def finalize_options(self):
        """Set the distribution directory to 'dist/X.Y'."""

        # pylint: disable-msg=W0201
        sdist.finalize_options(self)
        branch = ".".join(__version__.split(".")[:2])
        self.dist_dir = os.path.join(self.dist_dir, branch)

    def run(self):

        os.system("tools/change-log")
        assert os.path.isfile("ChangeLog")
        sdist.run(self)
        basename = "gaupol-%s" % __version__
        tarballs = os.listdir(self.dist_dir)
        os.chdir(self.dist_dir)

        # Compare tarball contents with working copy.
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)
        tobj = tarfile.open(tarballs[-1], "r")
        for member in tobj.getmembers():
            tobj.extract(member, temp_dir)
        log.info("comparing tarball (tmp) with working copy (../..)")
        os.system('diff -qr -x ".*" -x "*.pyc" ../.. %s' % test_dir)
        response = raw_input("Are all files in the tarball [Y/n]? ")
        if response.lower() == "n":
            raise SystemExit("Must edit MANIFEST.in.")
        dir_util.remove_tree(test_dir)

        # Create extra distribution files.
        log.info("calculating md5sums")
        os.system("md5sum * > %s.md5sum" % basename)
        log.info("creating '%s.changes'" % basename)
        source = os.path.join("..", "..", "ChangeLog")
        shutil.copyfile(source, "%s.changes" % basename)
        log.info("creating '%s.news'" % basename)
        source = os.path.join("..", "..", "NEWS")
        shutil.copyfile(source, "%s.news" % basename)
        for tarball in tarballs:
            log.info("signing '%s'" % tarball)
            os.system("gpg --detach %s" % tarball)

        # Create latest.txt.
        os.chdir("..")
        log.info("creating 'latest.txt'")
        with open("latest.txt", "w") as fobj:
            fobj.write("%s\n" % __version__)


data_files = [
    ("share/gaupol", ("data/gaupol.gtk.conf.spec",)),
    ("share/gaupol/codes", glob.glob("data/codes/*")),
    ("share/gaupol/glade/dialogs",
     glob.glob("data/glade/dialogs/*.glade")),
    ("share/gaupol/glade/assistants/text",
     glob.glob("data/glade/assistants/text/*.glade")),
    ("share/gaupol/headers", glob.glob("data/headers/*")),
    ("share/gaupol/patterns", glob.glob("data/patterns/*.conf")),
    ("share/gaupol/ui", glob.glob("data/ui/*")),
    ("share/man/man1", ("doc/gaupol.1",)),]

for size in ("16x16", "22x22", "24x24", "32x32", "scalable"):
    files  = glob.glob("data/icons/hicolor/%s/apps/*.png" % size)
    files += glob.glob("data/icons/hicolor/%s/apps/*.svg" % size)
    data_files.append(("share/icons/hicolor/%s/apps" % size, files))

if "py2exe" in sys.argv:
    # Add translated data files, which must have been separately compiled,
    paths = [x[:-3] for x in glob.glob("data/patterns/*.in")]
    data_files.append(("share/gaupol/patterns", paths))
    for locale in os.listdir("locale"):
        mo_path = "locale/%s/LC_MESSAGES/gaupol.mo" % locale
        destination = "share/locale/%s/LC_MESSAGES" % locale
        data_files.append((destination, (mo_path,)))

packages = []

for (root, dirs, files) in os.walk("gaupol"):
    init_path = os.path.join(root, "__init__.py")
    if not os.path.isfile(init_path): continue
    path = root.replace(os.sep, ".")
    path = path[path.find("gaupol"):]
    if not path.endswith(".test"):
        packages.append(path)

kwargs = {}

if "py2exe" in sys.argv:
    windows = [{
        "script": "bin/gaupol",
        "icon_resources": [(0, "data/icons/gaupol.ico")],}]
    py2exe_options = {
        "includes": ["atk",],
        "packages": [
            "cairo",
            "chardet",
            "enchant",
            "gaupol",
            "gobject",
            "gtk",
            "pangocairo",
            "pygtk",],}
    kwargs["windows"] = windows
    kwargs["options"] = {"py2exe": py2exe_options}


setup(
    name="gaupol",
    version=__version__,
    requires=("gtk (>=2.12.0)",),
    platforms=("Platform Independent",),
    author="Osmo Salomaa",
    author_email="otsaloma@cc.hut.fi",
    url="http://home.gna.org/gaupol/",
    description="Subtitle editor",
    license="GPL",
    packages=packages,
    scripts=("bin/gaupol",),
    data_files=data_files,
    cmdclass={
        "clean": Clean,
        "install": Install,
        "install_data": InstallData,
        "install_lib": InstallLib,
        "sdist_gna": SDistGna,},
    **kwargs)
