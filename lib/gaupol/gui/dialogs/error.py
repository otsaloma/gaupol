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


"""Error message dialogs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk


FLAGS   = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT
TYPE    = gtk.MESSAGE_ERROR
BUTTONS = gtk.BUTTONS_OK


class PasteFitErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that clipboard contents don't fit where pasted."""
    
    def __init__(self, parent, lacking):

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Not enough subtitles to fit cliboard contents')
        )
        self.format_secondary_text( \
            _('To paste to the current location, first create %d new subtitles.') \
            % lacking \
        )


class ReadFileErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that IOError occured while reading."""
    
    def __init__(self, parent, basename, detail):
        """
        Initialize a ReadFileErrorDialog object.
        
        basename: basename of the file being opened
        detail  : detailed error message from IOError
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Failed to read file "%s"') % basename
        )

        self.format_secondary_text('%s.' % detail)


class UnicodeDecodeErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that UnicodeError occured while reading."""
    
    def __init__(self, parent, basename, codec):
        """
        Initialize a UnicodeDecodeErrorDialog object.
        
        basename: basename of the file being opened
        codec   : character encoding used for conversion
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Failed to decode file "%s" with codec "%s"') % (basename, codec)
        )
        self.format_secondary_text( \
            _('Please try to open the file with a different character encoding.') \
        )


class UnicodeEncodeErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that UnicodeError occured while writing."""
    
    def __init__(self, parent, basename, codec):
        """
        Initialize a UnicodeEncodeErrorDialog object.
        
        basename: basename of the file being written
        codec   : character encoding used for conversion
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Failed to encode file "%s" with codec "%s"') % (basename, codec)
        )
        self.format_secondary_text( \
            _('Please try to save the file with a different character encoding.') \
        )


class UnknownFileFormatErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that filetype is not supported."""
    
    def __init__(self, parent, basename):
        """
        Initialize an UnknownFileFormatErrorDialog object.
        
        basename: basename of the file being opened
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Failed to recognize format of file "%s"') % basename
        )
        self.format_secondary_text( \
            _('Please check that the file you are trying to open is a subtitle file of a format supported by Gaupol.') \
        )


class VersionCheckErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that version check failed."""
    
    def __init__(self, parent, detail):

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, gtk.BUTTONS_NONE,
            _('Failed to check latest version')
        )

        self.add_button(_('_Go To Download Page'), gtk.RESPONSE_ACCEPT)
        self.add_button(gtk.STOCK_OK             , gtk.RESPONSE_OK    )

        self.set_default_response(gtk.RESPONSE_OK)

        self.format_secondary_text(detail)


class WriteFileErrorDialog(gtk.MessageDialog):
    
    """Dialog to inform that IOError occured while writing."""
    
    def __init__(self, parent, basename, detail):
        """
        Initialize a WriteFileErrorDialog object.
        
        basename: basename of the file being opened
        detail  : detailed error message from IOError
        """
        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, BUTTONS,
            _('Failed to write file "%s"') % basename
        )
        
        self.format_secondary_text('%s.' % detail)
