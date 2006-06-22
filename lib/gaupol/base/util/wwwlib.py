# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Connecting to remote documents."""


import os
import subprocess
import sys
import threading
import urllib
import webbrowser

from gaupol.base.error import TimeoutError


class _URLReadThread(threading.Thread):

    """Threaded reading of a remote document."""

    def __init__(self, url):

        threading.Thread.__init__(self)

        self.url   = url
        self.text  = None
        self.error = None

    def run(self):
        """Run thread."""

        try:
            self.text = urllib.urlopen(self.url).read()
        except IOError:
            self.error = sys.exc_info()[1]


def browse_url(url, browser=None):
    """Open url in browser."""

    if browser is not None:
        subprocess.Popen('%s "%s"' % (browser, url), shell=True)

    elif os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
        subprocess.Popen('gnome-open "%s"' % url, shell=True)

    elif os.getenv('KDE_FULL_SESSION') is not None:
        subprocess.Popen('kfmclient exec "%s"' % url, shell=True)

    elif sys.platform == 'darwin':
        subprocess.Popen('open "%s"' % url, shell=True)

    elif sys.platform == 'win32':
        os.startfile(url)

    else:
        webbrowser.open(url)

def read_url(url, timeout=10):
    """
    Read remote document.

    Document reading is done in a thread that ends with or without success
    after amount of seconds specified by timeout has ended.

    Raise IOError if reading fails.
    Raise TimeoutError if reading times out.
    """
    thread = _URLReadThread(url)
    thread.start()
    thread.join(timeout)

    if thread.error is not None:
        raise thread.error
    if thread.text is None:
        raise TimeoutError

    return thread.text
