#!/usr/bin/env python

import glob
import os
import shutil
import sys
import tarfile
import tempfile

from distutils                      import dir_util
from distutils.command.clean        import clean
from distutils.command.install_data import install_data
from distutils.command.install_lib  import install_lib
from distutils.command.sdist        import sdist
from distutils.core                 import Command
from distutils.core                 import setup
from distutils.log                  import info

sys.path.insert(0, 'lib')
from gaupol import __version__


packages = []
for (root, dirs, files) in os.walk('lib'):
    if os.path.isfile(os.path.join(root, '__init__.py')):
        path = root.replace(os.sep, '.')
        path = path[path.find('gaupol'):]
        if path.find('.test') == -1:
            packages.append(path)

scripts = ['gaupol']

data_files = [
    ('share/doc/gaupol'                 , ['AUTHORS', 'COPYING', 'README']),
    ('share/gaupol/glade'               , glob.glob('data/glade/*.glade') ),
    ('share/gaupol/headers'             , glob.glob('data/headers/*.txt') ),
    ('share/gaupol/icons'               , ['data/icons/gaupol.png']       ),
    ('share/gaupol/ui'                  , glob.glob('data/ui/*.xml')      ),
    ('share/icons/hicolor/48x48/apps'   , ['data/icons/gaupol.png']       ),
    ('share/icons/hicolor/scalable/apps', ['data/icons/gaupol.svg']       ),
]


class Clean(clean):

    def run(self):

        clean.run(self)

        desktop_file = os.path.join('data', 'gaupol.desktop')
        if os.path.isfile(desktop_file):
            os.remove(desktop_file)

        for name in ('installed-files.log', 'MANIFEST'):
            if os.path.isfile(name):
                os.remove(name)

        lib_dir = os.path.abspath('lib')
        for (root, dirs, files) in os.walk(lib_dir):
            os.chdir(root)
            for name in files:
                if name.endswith('.pyc'):
                    os.remove(name)

        dir_util.remove_tree('locale')


class InstallData(install_data):

    def _get_desktop_file(self):

        desktop_file = 'data/gaupol.desktop'
        os.system('intltool-merge -d po %s.in %s' % (
            desktop_file, desktop_file))
        return ('share/applications', [desktop_file])

    def _get_mo_files(self):

        mo_files = []
        for po_file in glob.glob('po/*.po'):
            lang = os.path.basename(po_file[:-3])
            mo_dir = 'locale/%s/LC_MESSAGES' % lang
            mo_file = mo_dir + '/gaupol.mo'
            dest_dir = 'share/' + mo_dir
            if not os.path.isdir(mo_dir):
                info('creating %s' % mo_dir)
                os.makedirs(mo_dir)
            info('compiling %s' % mo_file)
            os.system('msgfmt -cv %s -o %s' % (po_file, mo_file))
            if os.path.isfile(mo_file):
                mo_files.append((dest_dir, [mo_file]))
        return mo_files

    def initialize_options(self):

        install_data.initialize_options(self)

        # List of created directories.
        self.__output_dirs = []

    def get_outputs(self):

        # Add created directories to the list of outputs.
        outputs = install_data.get_outputs(self)
        return outputs + self.__output_dirs

    def mkpath(self, *args, **kwargs):

        created_dirs = dir_util.mkpath(self, *args, **kwargs)

        # List created directories.
        for entry in created_dirs:
            if entry not in self.__output_dirs:
                self.__output_dirs.append(entry)

    def run(self):

        # Translate files and add them to data files.
        self.data_files.extend(self._get_mo_files())
        self.data_files.extend(self._get_desktop_file())

        install_data.run(self)


class InstallLib(install_lib):

    def get_outputs(self):

        outputs = install_lib.get_outputs(self)

        # Add created directories to outputs.
        output_dirs = []
        gaupol_dir = os.path.join(self.install_dir, 'gaupol')
        output_dirs.append(gaupol_dir)
        for root, dirs, files in os.walk(gaupol_dir):
            for name in dirs:
                output_dirs.append(os.path.join(root, name))

        return outputs + output_dirs

    def install(self):

        # Write path information to file "paths.py".
        paths_file = os.path.join(self.build_dir, 'gaupol', 'base', 'paths.py')
        parent = self.distribution.get_command_obj('install').install_data
        data_dir    = os.path.join(parent, 'data')
        locale_dir  = os.path.join(parent, share, 'locale')
        profile_dir = "os.path.join(os.path.expanduser('~'), '.gaupol')"

        fobj = open(paths_file, 'w')
        fobj.write('import os\n\n')
        fobj.write('DATA_DIR    = %r\n' % data_dir   )
        fobj.write('LOCALE_DIR  = %r\n' % locale_dir )
        fobj.write('PROFILE_DIR = %r\n' % profile_dir)
        fobj.close()

        return install_lib.install(self)


class SDistGna(sdist):

    description  = 'create a source distribution for Gna!'

    def finalize_options(self):

        sdist.finalize_options(self)

        # Set distribution directory to "dist/x.y".
        self.dist_dir = os.path.join(self.dist_dir, __version__[:3])

    def run(self):

        basename = 'gaupol-%s' % __version__
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)

        Clean().run()
        sdist.run(self)
        tarballs = os.listdir(self.dist_dir)

        # Compare tarball contents with working copy.
        for tarball in tarballs:
            tarball_file = os.path.join(self.dist_dir, tarball)
            if not tarfile.is_tarfile(tarball_file):
                continue
            tarobj = tarfile.open(tarball_file, 'r')
            for member in tarobj.getmembers():
                tarobj.extract(member, temp_dir)
            info('comparing tarball (tmp) with working copy (.)')
            os.system('diff -r -x *.pyc -x .svn -x .hidden . %s' % test_dir)
            response = raw_input('Are all files in the tarball [Y/n]? ')
            if response.lower() == 'n':
                raise SystemExit('aborted')
            break

        # Create extra distribution files.
        os.chdir(self.dist_dir)
        info('calculating md5sums')
        os.system('md5sum * > %s.md5sum' % basename)
        info('creating %s.changes' % basename)
        path = os.path.join('..', '..', 'ChangeLog')
        shutil.copyfile(path, '%s.changes' % basename)
        info('creating %s.news' % basename)
        path = os.path.join('..', '..', 'NEWS')
        shutil.copyfile(path, '%s.news' % basename)
        for tarball in tarballs:
            info('signing %s' % tarball)
            os.system('gpg --detach %s' % tarball)

        # Create latest.txt.
        os.chdir('..')
        info('creating latest.txt')
        fobj = open('latest.txt', 'w')
        fobj.write('%s\n' % __version__)
        fobj.close()


class Uninstall(Command):

    description  = 'uninstall installed files'
    user_options = []

    def initialize_options(self):

        pass

    def finalize_options(self):

        pass

    def run (self):

        log_file = 'installed-files.log'
        question = 'Remove all files listed in %s? [y/N]? ' % log_file
        response = raw_input(question)
        if response.lower() != 'y':
            raise SystemExit('aborted')

        try:
            fobj = open(log_file, 'r')
            try:
                paths = fobj.readlines()
            finally:
                fobj.close()
        except IOError, (no, message):
            info('failed to read file "%s": %s' % (log_file, message))
            raise SystemExit(1)

        # Sort list so that files precede directories.
        paths = list(x.strip() for x in paths)
        paths.sort()
        paths.reverse()

        for path in paths:
            if os.path.isfile(path):
                info('removing file %s' % path)
                if not self.dry_run:
                    try:
                        os.remove(path)
                    except (IOError, OSError), (no, message):
                        info('failed to remove file %s: %s' % (path, message))
            elif os.path.isdir(path):
                info('removing directory %s' % path)
                if not self.dry_run:
                    try:
                        os.rmdir(path)
                    except (IOError, OSError), (no, message):
                        info('failed to remove directory %s: %s' % (
                            path, message))
            else:
                info('file %s not found' % path)


setup(
    name='gaupol',
    version=__version__,
    author='Osmo Salomaa',
    author_email='otsaloma@cc.hut.fi',
    url='http://home.gna.org/gaupol',
    description='Subtitle editor',
    license='GNU GPL',
    package_dir={'': 'lib'},
    packages=packages,
    scripts=scripts,
    data_files=data_files,
    cmdclass={
        'clean'       : Clean,
        'install_data': InstallData,
        'install_lib' : InstallLib,
        'sdist_gna'   : SDistGna,
        'uninstall'   : Uninstall
    }
)
