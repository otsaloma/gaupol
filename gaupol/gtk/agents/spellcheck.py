# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Checking spelling."""


from gaupol.base import Delegate
from gaupol.gtk import util
from gaupol.gtk.dialogs import LanguageDialog, SpellCheckDialog


class SpellCheckAgent(Delegate):

    """Checking spelling."""

    # pylint: disable-msg=E0203,W0201

    def on_check_spelling_activate(self, *args):
        """Check for incorrect spelling."""

        util.set_cursor_busy(self.window)
        dialog = SpellCheckDialog(self.window, self)
        util.set_cursor_normal(self.window)
        self.flash_dialog(dialog)
        self.update_gui()

    def on_configure_spell_check_activate(self, *args):
        """Set languages and spell-check targets."""

        util.set_cursor_busy(self.window)
        dialog = LanguageDialog(self.window)
        util.set_cursor_normal(self.window)
        self.flash_dialog(dialog)
        self.update_gui()
