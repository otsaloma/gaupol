#!/usr/bin/env python

from distutils.core import Command
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.command.sdist import sdist
from distutils.core import setup
from distutils.log import info
from glob import glob
import os
import shutil
import sys
import tarfile
import tempfile


sys.path.insert(0, 'lib')
from gaupol.constants import VERSION


packages = []

# Recursively find all packages in the "lib" directory.
for (dirpath, dirnames, basenames) in os.walk('lib'):
    if os.path.isfile(os.path.join(dirpath, '__init__.py')):
        path = dirpath.replace(os.sep, '.')
        path = path[path.find('gaupol'):]
        packages.append(path)

scripts = ['gaupol']

glade_files = glob(os.path.join('data', 'glade', '*.glade'))
icon_files  = glob(os.path.join('data', 'icons', '*.png'  ))
ui_files    = glob(os.path.join('data', 'ui'   , '*.xml'  ))

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


UNINSTALL_WARNING = '''
This uninstallation feature is not a part of Python distutils, but instead an
unstable extension. No responsibility will be taken for possible data loss.

The uninstallation process will first remove all files listed in
"installed-files.log", which was generated during the installation. That log
contains only files, not directories. After all the files have been removed,
the process will continue by recursively going through all the empty parent
directories and asking if you want them removed.

Note: The "--dry-run" option is not supported. All files will actually be
removed if you choose to continue.
'''


class InstallData(install_data):

    def run(self):

        self.data_files.extend(self._get_mo_files())
        
        install_data.run(self)

    def _get_mo_files(self):
    
        mo_files = []
        
        for po_path in glob(os.path.join('po', '*.po')):
        
            lang = os.path.basename(po_path[:-3])
            
            mo_dir  = os.path.join('locale', lang, 'LC_MESSAGES')
            mo_path = os.path.join(mo_dir, 'gaupol.mo')
            destination = os.path.dirname(os.path.join('share', mo_path))
            
            if not os.path.isdir(mo_dir):
                info('creating %s' % mo_dir)
                os.makedirs(mo_dir)
            
            info('compiling %s' % mo_path)
            os.system('msgfmt %s -o %s' % (po_path, mo_path))

            if os.path.isfile(mo_path):
                mo_files.append((destination, [mo_path]))
                
        return mo_files


class InstallLib(install_lib):

    def install(self):
    
        paths_path = os.path.join(self.build_dir, 'gaupol', 'paths.py')
        
        install = self.distribution.get_command_obj('install')
        
        data_dir   = os.path.join(install.prefix, 'share', 'gaupol')
        glade_dir  = os.path.join(data_dir, 'glade')
        icon_dir   = os.path.join(data_dir, 'icons')
        ui_dir     = os.path.join(data_dir, 'ui'   )
        locale_dir = os.path.join(install.prefix, 'share', 'locale')
        
        paths_file = open(paths_path, 'a')
        
        paths_file.write('DATA_DIR   = %r\n' % data_dir  )
        paths_file.write('GLADE_DIR  = %r\n' % glade_dir )
        paths_file.write('ICON_DIR   = %r\n' % icon_dir  )
        paths_file.write('UI_DIR     = %r\n' % ui_dir    )
        paths_file.write('LOCALE_DIR = %r\n' % locale_dir)
        
        paths_file.close()
        
        return install_lib.install(self)


class SDist(sdist):

    def finalize_options(self):
    
        sdist.finalize_options(self)
        
        # Set distribution directory to "dist/x.y".
        self.dist_dir = os.path.join(self.dist_dir, VERSION[:3])

    def run(self):
    
        basename = 'gaupol-%s' % VERSION
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)
    
        # Remove build and test directories.
        for dir in ('build', 'dist', 'locale', test_dir):
            info('removing %s' % dir)
            for root, dirs, files in os.walk(dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            if os.path.isdir(dir):
                os.rmdir(dir)
        
        # Remove build files.
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
                
            tar_file = tarfile.open(tarball_path, 'r')
            for member in tar_file.getmembers():
                tar_file.extract(member, temp_dir)
            
            info('comparing tarball (temp) with working copy (.)')
            os.system('diff -r -x *.pyc -x .svn . %s' % test_dir)
            
            # Stop and ask if all necessary files are included.
            response = raw_input('Are all files in the tarball [Y/n]? ')
            if response.lower() == 'n':
                info('aborted')
                return
            
            break
            
        # Change to directory "dist/x.y".
        os.chdir(self.dist_dir)

        # Calculate md5sums.
        info('calculating md5sums')
        os.system('md5sum * > %s.md5sum' % basename)
        
        # Create changes file.
        path = os.path.join('..', '..', 'ChangeLog')
        info('creating %s.changes' % basename)
        shutil.copyfile(path, '%s.changes' % basename)
        
        # Create news file.
        path = os.path.join('..', '..', 'NEWS')
        info('creating %s.news' % basename)
        shutil.copyfile(path, '%s.news' % basename)
        
        # Sign tarballs.
        for tarball in tarballs:
            info('signing %s' % tarball)
            os.system('gpg --detach %s' % tarball)
        
        # Create symlink to latest file (tar.gz).
        info('creating LATEST-IS-%s' % VERSION)
        os.symlink('%s.tar.gz' % basename, 'LATEST-IS-%s' % VERSION)
        
        # Change to directory "dist".
        os.chdir('..')
        
        # Create and sign latest.txt file.
        info('creating latest.txt')
        latest_file = open('latest.txt', 'w')
        latest_file.write('%s\n' % VERSION)
        latest_file.close()
        info('signing latest.txt')
        os.system('gpg --detach latest.txt')


class Uninstall(Command):

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
            return

        log_path = 'installed-files.log'
        
        try:
            log_file = open(log_path, 'r')
            try:
                lines = log_file.readlines()
            finally:
                log_file.close()
        except IOError, (errno, detail):
            info('Failed to read file "%s": %s.' % (log_path, detail))
            return
        
        paths = [line.strip() for line in lines]
        
        # Remove files.
        for path in paths:
            if os.path.isfile(path):
                info('removing file %s' % path)
                try:
                    os.remove(path)
                except (IOError, OSError):
                    info('failed to remove file %s' % path)
            else:
                info('file %s not found' % path)
        
        # Remove empty parent directories.
        while paths:

            # Get parent directories and remove duplicates.
            paths = [os.path.dirname(path) for path in paths]
            paths.sort()
            for i in reversed(range(1, len(paths))):
                if paths[i] == paths[i - 1]:
                    paths.pop(i)
            
            for i in reversed(range(len(paths))):
            
                path = paths[i]
                
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
                except (IOError, OSError):
                    info('failed to remove directory %s' % path)


setup(
    name='gaupol',
    version=VERSION,
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
