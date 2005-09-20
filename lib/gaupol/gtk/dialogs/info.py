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


"""Information message dialogs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk


FLAGS = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT
TYPE  = gtk.MESSAGE_INFO


class VersionCheckInfoDialog(gtk.MessageDialog):

    """Dialog to inform whether user has the latest version or not."""

    def __init__(self, parent, local_version, remote_version):

        if remote_version > local_version:
            title = _('A newer version is available')
        else:
            title = _('You have the latest version')

        detail = _('The latest version is %s.\nYou are using %s.') \
                 % (remote_version, local_version)

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, gtk.BUTTONS_NONE, title
        )

        self.add_button(_('_Open Download Page'), gtk.RESPONSE_ACCEPT)
        self.add_button(gtk.STOCK_OK            , gtk.RESPONSE_OK    )

        self.set_default_response(gtk.RESPONSE_OK)

        self.format_secondary_text(detail)
