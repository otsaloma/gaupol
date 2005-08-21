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


"""Support and information."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.constants import VERSION
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.about import AboutDialog
from gaupol.gui.dialogs.error import VersionCheckErrorDialog
from gaupol.gui.dialogs.info import VersionCheckInfoDialog
from gaupol.gui.util import gui
from gaupol.lib.util import internet


BUG_REPORT_URL = 'http://gna.org/bugs/?func=additem&group=gaupol'
DOWNLOAD_URL   = 'http://home.gna.org/gaupol'
SUPPORT_URL    = 'http://gna.org/support/?func=additem&group=gaupol'
TIMEOUT_SEC    = 10
VERSION_URL    = 'http://download.gna.org/gaupol/latest.txt'


class Helper(Delegate):
    
    """Support and information."""

    def on_about_activated(self, *args):
        """Display about dialog."""
        
        dialog = AboutDialog(self.window)
        dialog.run()
        dialog.destroy()

    def on_check_latest_version_activated(self, *args):
        """Check latest version of Gaupol."""

        gui.set_cursor_busy(self.window)

        try:
            text = internet.URLDocument(VERSION_URL, TIMEOUT_SEC).read()
            
        except IOError, (errno, detail):
            message = '%s.' % detail
            dialog  = VersionCheckErrorDialog(self.window, message)
            
        except internet.TimeoutError:
            message = _('Operation timed out. Please try again later or proceed to the download page.')
            dialog  = VersionCheckErrorDialog(self.window, message)
            
        else:
            remote_version = text.strip()
            
            # Automated HTML error message must be distinguished from the
            # expected single-line version string.
            if remote_version.find('\n') != -1:
                message = _('No version information found at URL "%s".') \
                          % VERSION_URL
                dialog  = VersionCheckErrorDialog(self.window, message)
            else:
                dialog  = VersionCheckInfoDialog(self.window, VERSION,
                                                 remote_version)

        gui.set_cursor_normal(self.window)
        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_ACCEPT:
            internet.open_url(DOWNLOAD_URL)
        
    def on_report_a_bug_activated(self, *args):
        """Open the project bug report page in a web browser."""

        internet.open_url(BUG_REPORT_URL)
        
    def on_support_activated(self, *args):
        """Open the project support page in a web browser."""

        internet.open_url(SUPPORT_URL)
