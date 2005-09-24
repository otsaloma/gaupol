#!/usr/bin/env python


import glob
import os
import shutil
import sys
import tarfile
import tempfile

from distutils.command.install_data import install_data
from distutils.command.install_lib  import install_lib
from distutils.command.sdist        import sdist
from distutils.core                 import Command
from distutils.core                 import setup
from distutils.log                  import info

# "lib" directory must be first in path to avoid getting version number from
# a previous installed version.
sys.path.insert(0, 'lib')
from gaupol import __version__


UNINSTALL_WARNING = '''
This uninstallation feature is not a part of Python distutils, but instead an
unstable extension that has not been tested enough.

The uninstallation process will first remove all files listed in
"installed-files.log", which was generated during installation. The log file
does not list directories created during installation and therefore they
cannot be deleted automatically. For all empty parent directories of the
installed files, you will be asked if you want the directory removed.

Note: The "--dry-run" option is not supported. All files will actually be
removed if you choose to continue.
'''

packages = []

# Recursively find all packages in the "lib" directory.
for (dirpath, dirnames, filenames) in os.walk('lib'):
    if os.path.isfile(os.path.join(dirpath, '__init__.py')):
        path = dirpath.replace(os.sep, '.')
        path = path[path.find('gaupol'):]
        packages.append(path)

scripts = ['gaupol']

glade_files = glob.glob(os.path.join('data', 'glade', '*.glade'))
icon_files  = glob.glob(os.path.join('data', 'icons', '*.png'  ))
ui_files    = glob.glob(os.path.join('data', 'ui'   , '*.xml'  ))

doc_files = (
    'AUTHORS',
    'ChangeLog',
    'COPYING',
    'NEWS',
    'README',
    'README.translators',
    'TODO'
)

data_files = [
    ('share/gaupol/glade', glade_files),
    ('share/gaupol/icons',  icon_files),
    ('share/gaupol/ui'   ,    ui_files),
    ('share/doc/gaupol'  ,   doc_files),
    ('share/applications', ['gaupol.desktop']),
    ('share/pixmaps'     , ['data/icons/gaupol.png']),
]


class InstallData(install_data):

    """Installation of data files."""

    def _get_mo_files(self):

        mo_files = []

        for po_path in glob.glob(os.path.join('po', '*.po')):

            lang = os.path.basename(po_path[:-3])

            mo_dir  = os.path.join('locale', lang, 'LC_MESSAGES')
            mo_path = os.path.join(mo_dir, 'gaupol.mo')
            destination = os.path.dirname(os.path.join('share', mo_path))

            if not os.path.isdir(mo_dir):
                info('creating %s' % mo_dir)
                os.makedirs(mo_dir)

            info('compiling %s' % mo_path)
            os.system('msgfmt -cv %s -o %s' % (po_path, mo_path))

            if os.path.isfile(mo_path):
                mo_files.append((destination, [mo_path]))

        return mo_files

    def run(self):

        # Compile translations and add them to data files.
        self.data_files.extend(self._get_mo_files())

        install_data.run(self)


class InstallLib(install_lib):

    """Installation of library files."""

    def install(self):

        # Write path information to file "paths.py".

        paths_path = os.path.join(self.build_dir, 'gaupol', 'paths.py')

        prefix = self.distribution.get_command_obj('install').prefix

        data_dir   = os.path.join(prefix, 'share', 'gaupol')
        glade_dir  = os.path.join(data_dir, 'glade')
        icon_dir   = os.path.join(data_dir, 'icons')
        ui_dir     = os.path.join(data_dir, 'ui'   )
        locale_dir = os.path.join(prefix, 'share', 'locale')

        paths_file = open(paths_path, 'a')

        paths_file.write('DATA_DIR   = %r\n' % data_dir  )
        paths_file.write('GLADE_DIR  = %r\n' % glade_dir )
        paths_file.write('ICON_DIR   = %r\n' % icon_dir  )
        paths_file.write('UI_DIR     = %r\n' % ui_dir    )
        paths_file.write('LOCALE_DIR = %r\n' % locale_dir)

        paths_file.close()

        return install_lib.install(self)


class SDist(sdist):

    """Building of source distribution."""

    def finalize_options(self):

        sdist.finalize_options(self)

        # Set distribution directory to "dist/x.y".
        self.dist_dir = os.path.join(self.dist_dir, __version__[:3])

    def run(self):

        basename = 'gaupol-%s' % __version__
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)

        # Remove leftover directories.
        for dir in ('build', 'dist', 'locale', test_dir):
            info('removing %s' % dir)
            for root, dirs, files in os.walk(dir, topdown=False):
                for entry in files:
                    os.remove(os.path.join(root, entry))
                for entry in dirs:
                    os.rmdir(os.path.join(root, entry))
            if os.path.isdir(dir):
                os.rmdir(dir)

        # Remove leftover files.
        for name in ('installed-files.log', 'MANIFEST'):
            if os.path.isfile(name):
                info('removing %s' % name)
                os.remove(name)

        # Compile all translations.
        os.system('./trantool -m all')

        # Create tarballs.
        sdist.run(self)
        tarballs = os.listdir(self.dist_dir)

        # Compare tarball contents with working copy.
        for tarball in tarballs:

            tarball_path = os.path.join(self.dist_dir, tarball)
            if not tarfile.is_tarfile(tarball_path):
                continue

            # Extract tarball to temp directory.
            tar_file = tarfile.open(tarball_path, 'r')
            for member in tar_file.getmembers():
                tar_file.extract(member, temp_dir)

            info('comparing tarball (tmp) with working copy (.)')
            os.system('diff -r -x *.pyc -x .svn . %s' % test_dir)

            # Stop and ask if all necessary files are included.
            response = raw_input('Are all files in the tarball [Y/n]? ')
            if response.lower() == 'n':
                info('aborted')
                raise SystemExit

            break

        # Change to directory "dist/x.y".
        os.chdir(self.dist_dir)

        # Calculate md5sums.
        info('calculating md5sums')
        os.system('md5sum * > %s.md5sum' % basename)

        # Create changes file.
        info('creating %s.changes' % basename)
        path = os.path.join('..', '..', 'ChangeLog')
        shutil.copyfile(path, '%s.changes' % basename)

        # Create news file.
        info('creating %s.news' % basename)
        path = os.path.join('..', '..', 'NEWS')
        shutil.copyfile(path, '%s.news' % basename)

        # Sign tarballs.
        for tarball in tarballs:
            info('signing %s' % tarball)
            os.system('gpg --detach %s' % tarball)

        # Create symlink to latest file (tar.gz).
        info('creating LATEST-IS-%s' % __version__)
        os.symlink('%s.tar.gz' % basename, 'LATEST-IS-%s' % __version__)

        # Change to directory "dist".
        os.chdir('..')

        # Create and sign latest.txt file.
        info('creating latest.txt')
        latest_file = open('latest.txt', 'w')
        latest_file.write('%s\n' % __version__)
        latest_file.close()
        info('signing latest.txt')
        os.system('gpg --detach latest.txt')


class Uninstall(Command):

    """Uninstallation of files listed in the installation log."""

    description = "uninstall installed files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run (self):

        print UNINSTALL_WARNING
        response = raw_input('Continue [y/N]? ')
        if response.lower() != 'y':
            raise SystemExit

        log_path = 'installed-files.log'

        # Get a list of the installed files.
        try:
            log_file = open(log_path, 'r')
            try:
                lines = log_file.readlines()
            finally:
                log_file.close()
        except IOError, (errno, detail):
            info('failed to read file "%s": %s' % (log_path, detail))
            raise SystemExit

        paths = [line.strip() for line in lines]

        # Remove files.
        for path in paths:
            if os.path.isfile(path):
                info('removing file %s' % path)
                try:
                    os.remove(path)
                except IOError,  (errno, detail):
                    info('failed to remove file %s: %s' % (path, detail))
                except OSError, detail:
                    info('failed to remove file %s: %s' % (path, detail))
            else:
                info('file %s not found' % path)

        # Remove empty parent directories.
        while paths:

            # Get a list of the parent directories and remove duplicates.
            paths = [os.path.dirname(path) for path in paths]
            paths.sort()
            for i in reversed(range(1, len(paths))):
                if paths[i] == paths[i - 1]:
                    paths.pop(i)

            for i in reversed(range(len(paths))):

                path = paths[i]

                # Skip directories already removed.
                if not os.path.isdir(path):
                    paths.pop(i)
                    continue

                # Skip non-empty directories.
                if os.listdir(path):
                    paths.pop(i)
                    continue

                # Remove empty directory.
                question = 'Remove empty directory %s [y/N]? ' % path
                response = raw_input(question)
                if response.lower() != 'y':
                    paths.pop(i)
                    continue
                try:
                    os.rmdir(path)
                except IOError,  (errno, detail):
                    info('failed to remove directory %s: %s' % (path, detail))
                except OSError, detail:
                    info('failed to remove directory %s: %s' % (path, detail))


setup(
    name='gaupol',
    version=__version__,
    description='Subtitle Editor',
    author='Osmo Salomaa',
    author_email='otsaloma@cc.hut.fi',
    url='http://home.gna.org/gaupol',
    license='GNU GPL',
    package_dir={'': 'lib'},
    packages=packages,
    scripts=scripts,
    data_files=data_files,
    cmdclass={
        'install_data': InstallData,
        'install_lib' : InstallLib,
        'sdist'       : SDist,
        'uninstall'   : Uninstall
    }
)
