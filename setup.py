#!/usr/bin/env python

"""
There are three relevant customizations to the standard distutils installation
process: (1) writing the gaupol.paths module, (2) handling translating of
various files and (3) installing extensions.

(1) Gaupol finds non-Python files based on the paths written in module
    gaupol.paths. In gaupol/paths.py the paths default to the ones in the
    source directory. During the 'install_lib' command the file gets rewritten
    to build/gaupol/paths.py with the installation paths and that file will be
    installed. The paths are based on variable 'install_data' with the 'root'
    variable stripped if it is given. If doing distro-packaging, make sure this
    file gets correctly written.

(2) During installation, the .po files are compiled into .mo files, the desktop
    file, pattern files and extension metadata files are translated. This
    requires gettext and intltool, more specifically, executables 'msgfmt' and
    'intltool-merge' in $PATH.

(3) Extensions are installed under the data directory. All python code included
    in the extensions are compiled during the 'install_data' command, using the
    same arguments for 'byte_compile' as used by the 'install_lib' command. If
    the 'install_lib' command was given '--no-compile' option, then the
    extensions are not compiled either.
"""

from __future__ import with_statement

import glob
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

from distutils import log
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.command.sdist import sdist
from distutils.core import setup
from distutils.util import byte_compile

os.chdir(os.path.dirname(__file__) or ".")
sys.path.insert(0, os.path.dirname(__file__))
from gaupol import __version__


class Clean(clean):

    """Command to remove files and directories created."""

    def run(self):
        """Remove files and directories listed in MANIFEST.junk."""

        clean.run(self)

        fobj = open(os.path.join("manifest", "junk-files"), "r")
        for targets in (glob.glob(x.strip()) for x in fobj):
            for target in filter(os.path.isdir, targets):
                log.info("removing '%s'" % target)
                if not self.dry_run: shutil.rmtree(target)
            for target in filter(os.path.isfile, targets):
                log.info("removing '%s'" % target)
                if not self.dry_run: os.remove(target)
        fobj.close()


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

    def __build_extensions(self):
        """Build all Python code files in extensions."""

        get_command_obj = self.distribution.get_command_obj
        if not get_command_obj("install_lib").compile: return
        optimize = get_command_obj("install_lib").optimize
        data_dir = get_command_obj("install_data").install_dir
        data_dir = os.path.join(data_dir, "share", "gaupol")
        files = glob.glob("extensions/*/*.py")
        files = [os.path.join(data_dir, x) for x in files]
        byte_compile(files, optimize, self.force, self.dry_run)

    def __get_desktop_file(self):
        """Return a tuple for the translated desktop file."""

        path = os.path.join("data", "gaupol.desktop")
        command = "intltool-merge -d po %s.in %s" % (path, path)
        run_command_or_exit(command)
        return ("share/applications", (path,))

    def __get_extension_file(self, extension, extension_file):
        """Return a tuple for the translated extension metadata file."""

        assert extension_file.endswith(".in")
        path = extension_file[:-3]
        command = "intltool-merge -d po %s.in %s" % (path, path)
        run_command_or_exit(command)
        return ("share/gaupol/extensions/%s" % extension, (path,))

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
        command = "msgfmt %s -o %s" % (po_file, mo_file)
        run_command_or_exit(command)
        return (dest_dir, (mo_file,))

    def __get_pattern_file(self, pattern_file):
        """Return a tuple for the translated pattern file."""

        assert pattern_file.endswith(".in")
        path = pattern_file[:-3]
        command = "intltool-merge -d po %s.in %s" % (path, path)
        run_command_or_exit(command)
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
        for extension in os.listdir("extensions"):
            pattern = "extensions/%s/*.gaupol-extension.in" % extension
            for extension_file in glob.glob(pattern):
                t = self.__get_extension_file(extension, extension_file)
                self.data_files.append(t)
        self.data_files.append(self.__get_desktop_file())
        install_data.run(self)
        self.__build_extensions()


class InstallLib(install_lib):

    """Command to install library files."""

    def install(self):
        """Install library files after writing changes."""

        # Allow --root to be used as a destination directory.
        root = self.distribution.get_command_obj("install").root
        prefix = self.distribution.get_command_obj("install").install_data
        if root is not None:
            root = os.path.abspath(root)
            prefix = os.path.abspath(prefix)
            prefix = prefix.replace(root, "")
        data_dir = os.path.join(prefix, "share", "gaupol")
        extension_dir = os.path.join(data_dir, "extensions")
        locale_dir = os.path.join(prefix, "share", "locale")

        # Write changes to the gaupol.paths module.
        path = os.path.join(self.build_dir, "gaupol", "paths.py")
        text = open(path, "r").read()
        patt = "DATA_DIR = get_data_directory()"
        repl = "DATA_DIR = %s" % repr(data_dir)
        text = text.replace(patt, repl)
        assert text.count(repr(data_dir)) > 0
        patt = "EXTENSION_DIR = get_extension_directory()"
        repl = "EXTENSION_DIR = %s" % repr(extension_dir)
        text = text.replace(patt, repl)
        assert text.count(repr(extension_dir)) > 0
        patt = "LOCALE_DIR = get_locale_directory()"
        repl = "LOCALE_DIR = %s" % repr(locale_dir)
        text = text.replace(patt, repl)
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

        if os.path.isfile("ChangeLog"):
            os.remove("ChangeLog")
        os.system("tools/generate-change-log > ChangeLog")
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
            raise SystemExit("Must edit MANIFEST.in")
        shutil.rmtree(test_dir)

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
        os.chdir("..")
        log.info("creating 'latest.txt'")
        with open("latest.txt", "w") as fobj:
            fobj.write("%s\n" % __version__)


def get_data_files():
    """Return a list of data files read from file."""

    data_files = []
    fok = lambda x: not x.endswith((".in", ".pyc"))
    fobj = open(os.path.join("manifest", "data-files"), "r")
    for line in (x.strip() for x in fobj):
        if not line: continue
        if line.startswith("["):
            dest = line[1:-1]
            continue
        files = filter(fok, glob.glob(line))
        assert files
        data_files.append((dest, files))
    fobj.close()
    return data_files

def get_packages():
    """Return a list of all packages under gaupol."""

    packages = []
    for (root, dirs, files) in os.walk("gaupol"):
        init_path = os.path.join(root, "__init__.py")
        if not os.path.isfile(init_path): continue
        path = root.replace(os.sep, ".")
        if path.endswith(".test"): continue
        packages.append(path[path.find("gaupol"):])
    return packages

def run_command_or_exit(command):
    """Run command in shell and raise SystemExit if it fails."""

    if os.system(command) != 0:
        raise SystemExit("Error: Command '%s' failed." % command)

setup_kwargs = dict(
    name="gaupol",
    version=__version__,
    requires=("gtk (>=2.12.0)",),
    platforms=("Platform Independent",),
    author="Osmo Salomaa",
    author_email="otsaloma@cc.hut.fi",
    url="http://home.gna.org/gaupol/",
    description="Subtitle editor",
    license="GPL",
    packages=get_packages(),
    scripts=("bin/gaupol",),
    data_files=get_data_files(),
    cmdclass={
        "clean": Clean,
        "install": Install,
        "install_data": InstallData,
        "install_lib": InstallLib,
        "sdist_gna": SDistGna,})

if __name__ == "__main__":
    setup(**setup_kwargs)
