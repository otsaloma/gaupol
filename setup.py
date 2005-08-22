#!/usr/bin/env python

from distutils.core import Command
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
from distutils.core import setup
from distutils.log import info
from glob import glob
import os
import sys

sys.path.append('lib')
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
doc_files   = ('AUTHORS', 'ChangeLog', 'COPYING', 'NEWS', 'README')

data_files = [
    ('share/gaupol/glade', glade_files),
    ('share/gaupol/icons',  icon_files),
    ('share/gaupol/ui'   ,    ui_files),
    ('share/docs/gaupol' ,   doc_files),
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

Note: the "--dry-run" option is not supported. All files will actually be
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
    name='Gaupol',
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
        'uninstall'   : Uninstall
    }
)
