# Copyright (C) 2005 Osmo Salomaa
#
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


"""Starting Gaupol GTK user interface."""


import os
import sys

import gobject
import gtk

from gaupol.gtk.application import Application
from gaupol.gtk.dialogs     import debug


def main(args):
    """
    Start the Gaupol GTK UI and open files given as arguments.

    args: list of files to open, should be sys.argv[1:]
    """
    # Catch exceptions to the debug dialog.
    sys.excepthook = debug.show

    # Initialize threading in a Windows-compatible manner.
    # http://www.async.com.br/faq/pygtk/index.py?req=show&file=faq20.006.htp
    # http://www.async.com.br/faq/pygtk/index.py?req=show&file=faq21.003.htp
    # http://www.mail-archive.com/pygtk@daa.com.au/msg10338.html
    gobject.threads_init()

    application = Application()

    paths = []
    for arg in args:
        path = os.path.abspath(arg)
        if os.path.isfile(path):
            paths.append(path)
    if paths:
        application.open_main_files(paths)

    gtk.main()
