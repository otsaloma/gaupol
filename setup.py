#!/usr/bin/env python3

"""
There are four relevant customizations to the standard distutils installation
process: (1) allowing separate installations of aeidon and gaupol, (2) writing
the aeidon.paths module, (3) handling translations and (4) extensions.

(1) Allowing separate installations of aeidon and gaupol are handled through
    global options --with-aeidon, --without-aeidon, --with-gaupol and
    --without-gaupol. See 'python3 setup.py --help' and the file
    'README.aeidon.md' for documentation and the Distribution class defined
    in this file for the implementation and logic of how that is handled.

(2) Gaupol finds non-Python files based on the paths written in module
    aeidon.paths. In aeidon/paths.py the paths default to the ones in the
    source directory. During the 'install_lib' command the file gets rewritten
    to build/aeidon/paths.py with the installation paths and that file will be
    installed. The paths are based on variable 'install_data' with the 'root'
    variable stripped if it is given. If doing distro-packaging, make sure this
    file gets correctly written.

(3) During installation, the .po files are compiled into .mo files and the
    appdata, desktop, pattern and extension metadata files are translated.
    This requires gettext.

(4) Extensions are installed under the data directory. All python code included
    in the extensions are compiled during the 'install_data' command, using the
    same arguments for 'byte_compile' as used by the 'install_lib' command.
    If the 'install_lib' command was given the '--no-compile' option, then
    extensions are not compiled either.
"""

import distutils
import glob
import os
import re
import shutil
import sys

from distutils import log
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.dist import Distribution as distribution


distribution.global_options.extend([
    ("mandir=", None, "relative installation directory for man pages (defaults to 'share/man')"),
    ("with-aeidon", None, "install the aeidon package"),
    ("without-aeidon", None, "don't install the aeidon package"),
    ("with-gaupol", None, "install the gaupol package"),
    ("without-gaupol", None, "don't install the gaupol package"),
    ("with-iso-codes", None, "install iso-codes JSON files"),
    ("without-iso-codes", None, "don't install iso-codes JSON files"),
])

distribution.negative_opt.update({
    "without-aeidon": "with-aeidon",
    "without-gaupol": "with-gaupol",
    "without-iso-codes": "with-iso-codes",
})


def get_aeidon_version():
    path = os.path.join("aeidon", "__init__.py")
    text = open(path, "r", encoding="utf_8").read()
    return re.search(r"__version__ *= *['\"](.*?)['\"]", text).group(1)

def get_gaupol_version():
    path = os.path.join("gaupol", "__init__.py")
    text = open(path, "r", encoding="utf_8").read()
    return re.search(r"__version__ *= *['\"](.*?)['\"]", text).group(1)

def run_or_exit(cmd):
    if os.system(cmd) == 0: return
    log.error("command {!r} failed".format(cmd))
    raise SystemExit(1)

def run_or_warn(cmd):
    if os.system(cmd) == 0: return
    log.warn("command {!r} failed".format(cmd))


class Clean(clean):

    def run(self):
        clean.run(self)
        f = open(os.path.join("manifests", "clean.manifest"), "r")
        for targets in [glob.glob(x.strip()) for x in f]:
            for target in filter(os.path.isdir, targets):
                log.info("removing {}".format(target))
                if not self.dry_run:
                    shutil.rmtree(target)
            for target in filter(os.path.isfile, targets):
                log.info("removing {}".format(target))
                if not self.dry_run:
                    os.remove(target)
        f.close()


class Distribution(distribution):

    def __init__(self, attrs=None):
        if sys.platform == "win32":
            self.executables = []
        self.mandir = "share/man"
        self.with_aeidon = True
        self.with_gaupol = True
        self.with_iso_codes = True
        distribution.__init__(self, attrs)
        self.data_files = []
        self.packages = []
        self.scripts = []

    def __find_data_files(self, name):
        fok = lambda x: not x.endswith((".in", ".pyc"))
        basename = "{}.manifest".format(name)
        f = open(os.path.join("manifests", basename), "r")
        for line in [x.strip() for x in f]:
            if not line: continue
            if line.startswith("["):
                dest = line[1:-1]
                continue
            files = list(filter(fok, glob.glob(line)))
            files = list(filter(os.path.isfile, files))
            assert files
            self.data_files.append((dest, files))
        f.close()

    def __find_man_pages(self):
        mandir = self.mandir
        while mandir.endswith("/"):
            mandir = mandir[:-1]
        dest = "{}/man1".format(mandir)
        self.data_files.append((dest, ["data/gaupol.1"]))

    def __find_packages(self, name):
        for root, dirs, files in os.walk(name):
            init_path = os.path.join(root, "__init__.py")
            if not os.path.isfile(init_path): continue
            path = root.replace(os.sep, ".")
            if path.endswith(".test"): continue
            self.packages.append(path[path.find(name):])

    def __find_scripts(self, name):
        if name == "gaupol":
            self.scripts.append("bin/gaupol")

    def parse_command_line(self):
        value = distribution.parse_command_line(self)
        # Configuration files are parsed before the command line, so once the
        # command line is parsed, all options have their final values and thus
        # files corresponding to the packages to install can finally be set.
        if self.with_aeidon:
            self.__find_data_files("aeidon")
            self.__find_packages("aeidon")
        if self.with_aeidon and self.with_iso_codes:
            self.__find_data_files("iso-codes")
        if self.with_gaupol:
            self.__find_data_files("gaupol")
            self.__find_man_pages()
            self.__find_packages("gaupol")
            self.__find_scripts("gaupol")
        # Redefine name, version and requires metadata attributes. These are
        # used in the egg-info file written by distutils. While egg-info files
        # appear completely useless, it needs to be ensured that if aeidon and
        # gaupol are installed separately, they install differently named
        # egg-info files in order to avoid overwriting each other.
        if self.with_gaupol:
            self.metadata.name = "gaupol"
            self.metadata.version = get_gaupol_version()
        else: # without gaupol
            self.metadata.name = "aeidon"
            self.metadata.version = get_aeidon_version()
        return value

    def parse_config_files(self, filenames=None):
        value = distribution.parse_config_files(self, filenames)
        strtobool = distutils.util.strtobool
        for option in ["with_aeidon", "with_gaupol", "with_iso_codes"]:
            value = getattr(self, option)
            if isinstance(value, str):
                setattr(self, option, strtobool(value))
        return value


class Install(install):

    def run(self):
        install.run(self)
        if not self.distribution.with_gaupol: return
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        data_dir = get_command_obj("install_data").install_dir
        # Assume we're actually installing if --root was not given.
        if (root is not None) or (data_dir is None): return
        directory = os.path.join(data_dir, "share", "applications")
        log.info("updating desktop database in {}".format(directory))
        run_or_warn('update-desktop-database "{}"'.format(directory))


class InstallData(install_data):

    def __build_extensions(self):
        get_command_obj = self.distribution.get_command_obj
        if not get_command_obj("install_lib").compile: return
        optimize = get_command_obj("install_lib").optimize
        data_dir = get_command_obj("install_data").install_dir
        data_dir = os.path.join(data_dir, "share", "gaupol")
        files = glob.glob("{}/extensions/*/*.py".format(data_dir))
        distutils.util.byte_compile(files, optimize, self.force, self.dry_run)
        # Figure out paths of the compiled files and add them to
        # self.outfiles so that 'setup.py --record' works correctly.
        def get_cache_pattern(path):
            dir, file = os.path.split(path)
            file = os.path.splitext(file)[0] + ".*"
            return os.path.join(dir, "__pycache__", file)
        for pattern in map(get_cache_pattern, files):
            for file in glob.glob(pattern):
                if not file in self.outfiles:
                    self.outfiles.append(file)

    def __generate_linguas(self):
        linguas = sorted(glob.glob("po/*.po"))
        linguas = [os.path.basename(x)[:-3] for x in linguas]
        with open("po/LINGUAS", "w") as f:
            f.write("\n".join(linguas) + "\n")

    def __get_appdata_file(self):
        path = os.path.join("data", "io.otsaloma.gaupol.appdata.xml")
        command = "msgfmt --xml -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/metainfo", [path])

    def __get_desktop_file(self):
        path = os.path.join("data", "io.otsaloma.gaupol.desktop")
        command = "msgfmt --desktop -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/applications", [path])

    def __get_extension_file(self, extension_file):
        assert extension_file.endswith(".in")
        path = extension_file[:-3]
        command = " ".join((
            "msgfmt --desktop -d po --template {}.in -o {}",
            "--keyword=",
            "--keyword=Name",
            "--keyword=Description",
        ))
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        extension = os.path.basename(os.path.dirname(extension_file))
        return ("share/gaupol/extensions/{}".format(extension), [path])

    def __get_extension_files(self):
        files = sorted(glob.glob("data/extensions/*/*.extension.in"))
        return [self.__get_extension_file(x) for x in files]

    def __get_mo_file(self, po_file):
        locale = os.path.basename(po_file[:-3])
        mo_dir = os.path.join("locale", locale, "LC_MESSAGES")
        mo_file = os.path.join(mo_dir, "gaupol.mo")
        log.info("compiling {}".format(mo_file))
        os.makedirs(mo_dir, exist_ok=True)
        run_or_exit("msgfmt {} -o {}".format(po_file, mo_file))
        dest_dir = os.path.join("share", mo_dir)
        return (dest_dir, [mo_file])

    def __get_mo_files(self):
        if sys.platform == "win32": return []
        files = sorted(glob.glob("po/*.po"))
        return [self.__get_mo_file(x) for x in files]

    def __get_pattern_file(self, pattern_file):
        assert pattern_file.endswith(".in")
        path = pattern_file[:-3]
        command = " ".join((
            "msgfmt --desktop -d po --template {}.in -o {}",
            "--keyword=",
            "--keyword=Name",
            "--keyword=Description",
        ))
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/gaupol/patterns", [path])

    def __get_pattern_files(self):
        files = sorted(glob.glob("data/patterns/*.in"))
        return [self.__get_pattern_file(x) for x in files]

    def run(self):
        self.__generate_linguas()
        if self.distribution.with_aeidon:
            self.data_files.extend(self.__get_mo_files())
            self.data_files.extend(self.__get_pattern_files())
        if self.distribution.with_gaupol:
            self.data_files.extend(self.__get_extension_files())
            self.data_files.append(self.__get_appdata_file())
            self.data_files.append(self.__get_desktop_file())
        install_data.run(self)
        if self.distribution.with_gaupol:
            self.__build_extensions()


class InstallLib(install_lib):

    def install(self):
        if not self.distribution.with_aeidon:
            return install_lib.install(self)
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        prefix = get_command_obj("install").install_data
        # Allow --root to be used like DESTDIR.
        if root is not None:
            prefix = os.path.abspath(prefix)
            prefix = prefix.replace(os.path.abspath(root), "")
        data_dir = os.path.join(prefix, "share", "gaupol")
        locale_dir = os.path.join(prefix, "share", "locale")
        # Write changes to the aeidon.paths module.
        path = os.path.join(self.build_dir, "aeidon", "paths.py")
        text = open(path, "r", encoding="utf_8").read()
        patt = r"^DATA_DIR = .*$"
        repl = "DATA_DIR = {!r}".format(data_dir)
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        patt = r"^LOCALE_DIR = .*$"
        repl = "LOCALE_DIR = {!r}".format(locale_dir)
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        open(path, "w", encoding="utf_8").write(text)
        return install_lib.install(self)


setup_kwargs = {
    "name": "gaupol",
    "version": get_gaupol_version(),
    "author": "Osmo Salomaa",
    "author_email": "otsaloma@iki.fi",
    "url": "https://otsaloma.io/gaupol/",
    "description": "Editor for text-based subtitle files",
    "license": "GPL",
    "distclass": Distribution,
    "cmdclass": {
        "clean": Clean,
        "install": Install,
        "install_data": InstallData,
        "install_lib": InstallLib,
    },
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__) or ".")
    distutils.core.setup(**setup_kwargs)
