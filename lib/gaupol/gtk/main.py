# Copyright (C) 2005 Osmo Salomaa
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Module to start Gaupol GTK+ user interface."""


import logging
import os

import gtk

from gaupol.gui.application import Application


logger = logging.getLogger()


def main(args):
    """
    Start the Gaupol GTK+ UI and open files given as arguments.
    
    args: sys.argv[1:]
    """
    application = Application()
    paths = []

    for arg in args:
    
        # Get full path.
        basename = os.path.basename(arg)
        dirname  = os.path.abspath(os.path.dirname(arg))
        path     = os.path.join(dirname, basename)
        
        # Accept only existing files.
        if os.path.isfile(path):
            paths.append(path)
        else:
            logger.info('Disregarding non-existent file "%s".' % path)
    
    if paths:
        application.open_main_files(paths)
    
    gtk.main()
