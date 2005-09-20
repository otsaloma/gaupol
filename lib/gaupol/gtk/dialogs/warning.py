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


"""Warning message dialogs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk


FLAGS   = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT
TYPE    = gtk.MESSAGE_WARNING
BUTTONS = gtk.BUTTONS_NONE


class CloseDocumentWarningDialog(gtk.MessageDialog):

    """Base class for document closing warning dialogs."""

    def __init__(self, parent, title):

        detail = _('If you don\'t save, changes will be permanently lost.')

        gtk.MessageDialog.__init__(self, parent, FLAGS, TYPE, BUTTONS, title)

        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL          , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE            , gtk.RESPONSE_YES   )

        self.set_default_response(gtk.RESPONSE_YES)

        self.format_secondary_text(detail)


class CloseMainWarningDialog(CloseDocumentWarningDialog):

    """Dialog to warn when closing main document."""

    def __init__(self, parent, basename):

        title = _('Save changes to main document "%s" before closing?') \
                % basename

        CloseDocumentWarningDialog.__init__(self, parent, title)


class CloseTranslationWarningDialog(CloseDocumentWarningDialog):

    """Dialog to warn when closing translation document."""

    def __init__(self, parent, basename):

        title = _('Save changes to translation document "%s" before closing?')\
                % basename

        CloseDocumentWarningDialog.__init__(self, parent, title)


class OpenTranslationWarningDialog(gtk.MessageDialog):

    """Dialog to warn when opening a translation file."""

    def __init__(self, parent, basename):

        title  = _('Save changes to translation document "%s" before opening a new one?') \
                 % basename
        detail = _('If you don\'t save, changes will be permanently lost.')

        gtk.MessageDialog.__init__(self, parent, FLAGS, TYPE, BUTTONS, title)

        self.add_button(_('Import _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL           , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE             , gtk.RESPONSE_YES   )

        self.set_default_response(gtk.RESPONSE_YES)

        self.format_secondary_text(detail)


class OpenBigFileWarningDialog(gtk.MessageDialog):

    """Dialog to warn when opening a file over 1 MB."""

    def __init__(self, parent, basename, size):
        """
        Initialize an OpenBigFileWarningDialog object.

        size is in megabytes.
        """
        title  = _('Open abnormally large file "%s"?') % basename
        detail = _('Size of the file is %.1f MB, which is abnormally large for a text-based subtitle file. Please, check that you are not trying to open a binary file.') \
                 % size

        gtk.MessageDialog.__init__(self, parent, FLAGS, TYPE, BUTTONS, title)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_OPEN  , gtk.RESPONSE_YES)

        self.set_default_response(gtk.RESPONSE_NO)

        self.format_secondary_text(detail)
