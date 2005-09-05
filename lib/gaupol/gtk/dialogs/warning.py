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

        gtk.MessageDialog.__init__(self, parent, FLAGS, TYPE, BUTTONS, title)
        
        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL          , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE            , gtk.RESPONSE_YES   )
        
        self.set_default_response(gtk.RESPONSE_YES)
        
        self.format_secondary_text( \
            _('If you don\'t save, changes will be permanently lost.') \
        )


class CloseMainWarningDialog(CloseDocumentWarningDialog):

    """Dialog to warn when closing main document with unsaved changes."""
    
    def __init__(self, parent, basename):
        """
        Initialize a CloseMainWarningDialog object.
        
        basename: basename of the document being closed
        """
        title = _('Save changes to main document "%s" before closing?') \
                % basename

        CloseDocumentWarningDialog.__init__(self, parent, title)


class CloseTranslationWarningDialog(CloseDocumentWarningDialog):

    """Dialog to warn when closing translation with unsaved changes."""
    
    def __init__(self, parent, basename):
        """
        Initialize a CloseTranslationWarningDialog object.
        
        basename: basename of the document being closed
        """
        title = _('Save changes to translation document "%s" before closing?')\
                % basename

        CloseDocumentWarningDialog.__init__(self, parent, title)


class ImportTranslationWarningDialog(gtk.MessageDialog):

    """Dialog to warn when importing a translation over a changed one."""
    
    def __init__(self, parent, basename):
        """
        Initialize an ImportTranslationWarningDialog object.
        
        basename: basename of the file being opened
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Save changes to translation document "%s" before importing a new one?') \
            % basename
        )
        
        self.add_button(_('Import _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL           , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE             , gtk.RESPONSE_YES   )
        
        self.set_default_response(gtk.RESPONSE_YES)
        
        self.format_secondary_text( \
            _('If you don\'t save, changes will be permanently lost.') \
        )


class OpenBigFileWarningDialog(gtk.MessageDialog):

    """Dialog to warn when opening a file over 1 MB."""
    
    def __init__(self, parent, basename, size):
        """
        Initialize an OpenBigFileWarningDialog object.
        
        basename: basename of the file being opened
        size    : file's size in megabytes
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Open abnormally large file "%s"?') % basename
        )
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_OPEN  , gtk.RESPONSE_YES)
        
        self.set_default_response(gtk.RESPONSE_NO)
        
        self.format_secondary_text( \
            _('Size of the file is %.1f MB, which is abnormally large for a text-based subtitle file. Please, check that you are not trying to open a binary file.') \
            % size \
        )
