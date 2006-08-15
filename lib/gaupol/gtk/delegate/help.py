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


"""Help and information."""


from gettext import gettext as _
import re

import gtk

from gaupol                  import __version__
from gaupol.base.error       import TimeoutError
from gaupol.base.util        import wwwlib
from gaupol.gtk.delegate     import Delegate, UIMAction
from gaupol.gtk.dialog.about import AboutDialog
from gaupol.gtk.urls         import BUG_REPORT_URL, DOWNLOAD_URL, VERSION_URL
from gaupol.gtk.util         import gtklib


_RE_VERSION = re.compile(r'^\d+\.\d+\.\d+$')


class _HelpAction(UIMAction):

    """Base class for help actions."""

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class CheckLatestVersionAction(_HelpAction):

    """Checking latest version."""

    action_item = (
        'check_latest_version',
        None,
        _('_Check Latest Version'),
        None,
        _('Check if you have the latest version'),
        'on_check_latest_version_activate'
    )

    paths = ['/ui/menubar/help/check_latest_version']


class ReportABugAction(_HelpAction):

    """Reporting a bug."""

    action_item = (
        'report_a_bug',
        None,
        _('_Report A Bug'),
        None,
        _('Submit a bug report'),
        'on_report_a_bug_activate'
    )

    paths = ['/ui/menubar/help/report_a_bug']


class ViewAboutDialogAction(_HelpAction):

    """Viewing about dialog."""

    action_item = (
        'view_about_dialog',
        gtk.STOCK_ABOUT,
        _('_About'),
        None,
        _('Information about Gaupol'),
        'on_view_about_dialog_activate'
    )

    paths = ['/ui/menubar/help/about']


class _VersionErrorDialog(gtk.MessageDialog):

    """Dialog for informing that version check failed."""

    def __init__(self, parent, message):

        gtk.MessageDialog.__init__(
            self,
            parent,
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_NONE,
            _('Failed to check latest version')
        )
        self.format_secondary_text(message)
        self.add_button(_('_Go to Download Page'), gtk.RESPONSE_ACCEPT)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)


class _VersionInfoDialog(gtk.MessageDialog):

    """Dialog for informing whether user has the latest version or not."""

    def __init__(self, parent, local, remote):

        parsed_remote = list(int(x) for x in remote.split('.'))
        parsed_local  = list(int(x) for x in  local.split('.'))

        if parsed_remote > parsed_local:
            title = _('Version %s is available') % remote
            message = _('You are currently using %s.') % local
        else:
            title = _('You have the latest version')
            message = _('Which is %s.') % local

        gtk.MessageDialog.__init__(
            self,
            parent,
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_NONE,
            title
        )
        self.format_secondary_text(message)
        self.add_button(_('_Go to Download Page'), gtk.RESPONSE_ACCEPT)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)


class HelpDelegate(Delegate):

    """Help and information."""

    def on_check_latest_version_activate(self, *args):
        """Check latest version online."""

        gtklib.set_cursor_busy(self._window)

        def show_error(message):
            dialog = _VersionErrorDialog(self._window, message)
            gtklib.set_cursor_normal(self._window)
            response = gtklib.run(dialog)
            if response == gtk.RESPONSE_ACCEPT:
                wwwlib.browse_url(DOWNLOAD_URL)

        try:
            version = wwwlib.read_url(VERSION_URL, 12).strip()
        except IOError, instance:
            show_error(_('Failed to connect to URL "%s": %s.') % (
                VERSION_URL, instance.args[1][1]))
            return
        except TimeoutError:
            show_error(_('Connection timed out.'))
            return
        if not _RE_VERSION.match(version):
            show_error(_('No version information found at URL "%s".') \
                % VERSION_URL)
            return

        dialog = _VersionInfoDialog(self._window, __version__, version)
        gtklib.set_cursor_normal(self._window)
        response = gtklib.run(dialog)
        if response == gtk.RESPONSE_ACCEPT:
            wwwlib.browse_url(DOWNLOAD_URL)

    def on_report_a_bug_activate(self, *args):
        """Report a bug."""

        wwwlib.browse_url(BUG_REPORT_URL)

    def on_view_about_dialog_activate(self, *args):
        """View about dialog."""

        gtklib.run(AboutDialog(self._window))
