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


"""Reading documents on the WWW."""


import os
import sys
import threading
import urllib

try:
    from psyco.classes import *
except ImportError:
    pass


class TimeoutError(Exception):

    """Exception raised when operation times out."""

    pass


class URLDocument(object):

    """Reading documents on the WWW."""

    def __init__(self, url, timeout):
        """
        Initialize an URLDocument object.
        
        timeout is in seconds.
        """ 
        self.url     = url
        self.timeout = timeout
        self.text    = None

    def read(self):
        """
        Read document.
        
        Raise IOError, if reading fails.
        Raise TimeoutError, if reading times out.
        """
        thread = threading.Thread(target=self._read)
        
        thread.start()
        thread.join(self.timeout)
        
        if self.text is None:
            raise TimeoutError

        return self.text

    def _read(self):
        """
        Read document.
        
        Raise IOError, if reading fails.
        """
        self.text = urllib.urlopen(self.url).read()


def open_url(url):
    """Open url in web-browser."""

    # TODO:
    # webbrowser module is not very good. It will open some browser, but
    # not the default browser. Add detection and start commands for other
    # OSs and DEs if such exist.
    
    # Windows
    if sys.platform == 'win32':
        os.startfile(WEBSITE)
        return

    # Gnome
    if os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
        return_value = os.system('gnome-open "%s"' % url)
        if return_value == 0:
            return

    import webbrowser
    webbrowser.open(url)
