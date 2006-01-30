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


"""Connecting to remote documents."""


import os
import sys
import threading
import urllib
import webbrowser

from gaupol.base.error import TimeoutError


class URLReadThread(threading.Thread):

    """Threaded reading of a remote document."""

    def __init__(self, url):

        threading.Thread.__init__(self)

        self.url      = url
        self.text     = None
        self.io_error = None

    def run(self):
        """Run thread."""

        try:
            self.text = urllib.urlopen(self.url).read()
        except IOError:
            self.io_error = sys.exc_info()[1]


def read_url(url, timeout_seconds):
    """
    Read remote document.

    Document reading is done in a thread that ends with or without success
    after timeout has ended.

    Raise IOError if reading fails.
    Raise TimeoutError if reading times out.
    """
    thread = URLReadThread(url)
    thread.start()
    thread.join(timeout_seconds)

    if thread.io_error is not None:
        raise thread.io_error
    if thread.text is None:
        raise TimeoutError

    return thread.text

def open_url(url):
    """Open url in web-browser."""

    # TODO:
    # The Python webbrowser module is not very good. It will open some browser,
    # but not the default browser. Add detection and start commands for other
    # OSs and DEs if such exist.

    # Windows
    if sys.platform == 'win32':
        os.startfile(url)
        return

    # GNOME
    if os.getenv('GNOME_DESKTOP_SESSION_ID') is not None:
        return_value = os.system('gnome-open "%s"' % url)
        if return_value == 0:
            return

    webbrowser.open(url)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestLib(Test):

        def test_read_url(self):

            text = read_url('http://download.gna.org/gaupol/latest.txt', 20)
            assert isinstance(text, basestring)

            try:
                read_url('http://download.gna.org/gaupol/latest.txt', 0.001)
                raise AssertionError
            except TimeoutError:
                pass

            try:
                read_url('http://aaaaaaaaaaaaaaaaaaaaaaaaa.org/test.txt', 10)
                raise AssertionError
            except IOError:
                pass

    TestLib().run()
