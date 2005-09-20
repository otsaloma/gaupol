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


"""Question message dialogs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk


FLAGS = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT
TYPE  = gtk.MESSAGE_QUESTION


class OverwriteFileQuestionDialog(gtk.MessageDialog):

    """Dialog to ask whether to overwrite existing file or not."""

    def __init__(self, parent, basename):

        title  = _('A file named "%s" already exists') % basename
        detail = _('Do you want to replace it with the one you are saving?')

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, gtk.BUTTONS_NONE, title
        )

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(_('_Replace')   , gtk.RESPONSE_YES)

        self.set_default_response(gtk.RESPONSE_NO)

        self.format_secondary_text(detail)


class PasteFitQuestionDialog(gtk.MessageDialog):

    """Dialog to ask whether to add new subtitles to fit clipboard data."""

    def __init__(self, parent, lacking):

        title  = _('Not enough subtitles exist to fit clipboard contents')
        detail = _('Add %d new subtitles?') % lacking

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, gtk.BUTTONS_NONE, title
        )

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_ADD   , gtk.RESPONSE_YES)

        self.set_default_response(gtk.RESPONSE_YES)

        self.format_secondary_text(detail)


class RevertQuestionDialog(gtk.MessageDialog):

    """Dialog to ask whether to revert changes or not."""

    def __init__(self, parent, main_exists, tran_exists, main_changed,
                 tran_active, tran_changed, main_basename, tran_basename):
        """
        Initialize a RevertQuestionDialog object.

        Raise ValueError if called with nothing to revert.
        """
        main_ok = not main_changed
        tran_ok = not tran_active or not tran_changed

        main_revertable = main_exists and main_changed
        tran_revertable = tran_exists and tran_active and tran_changed

        main_loseable = not main_exists and main_changed
        tran_loseable = not tran_exists and tran_active and tran_changed

        if not main_revertable and not tran_revertable:
            raise ValueError('There\'s nothing to revert!')

        if main_revertable and tran_revertable:
            title = _('Revert unsaved changes to both main document "%s" and translation document "%s"?') \
                    % (main_basename, tran_basename)

        elif main_revertable and tran_loseable:
            title = _('Revert unsaved changes to main document "%s" and lose changes translation document "%s"?') \
                    % (main_basename, tran_basename)

        elif main_revertable and tran_ok:
            title = _('Revert unsaved changes to main document "%s"?') \
                    % main_basename

        elif main_loseable and tran_revertable:
            title = _('Revert unsaved changes to translation document "%s" and lose changes main document "%s"?') \
                    % (tran_basename, main_basename)

        elif main_ok and tran_revertable:
            title = _('Revert unsaved changes to translation document "%s"?') \
                    % tran_basename

        detail = _('If you revert, changes will be permanently lost.')

        gtk.MessageDialog.__init__(
            self, parent, FLAGS, TYPE, gtk.BUTTONS_NONE, title
        )

        self.add_button(gtk.STOCK_CANCEL         , gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_REVERT_TO_SAVED, gtk.RESPONSE_YES)

        self.set_default_response(gtk.RESPONSE_NO)

        self.format_secondary_text(detail)
