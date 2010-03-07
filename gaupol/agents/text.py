# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Processing texts."""

import aeidon
import gaupol


class TextAgent(aeidon.Delegate):

    """Checking spelling."""

    def on_check_spelling_activate(self, *args):
        """Check for incorrect spelling."""

        gaupol.util.set_cursor_busy(self.window)
        try: # Fails if no dictionary for conf.spell_check.language.
            dialog = gaupol.SpellCheckDialog(self.window, self)
        except ValueError:
            return gaupol.util.set_cursor_normal(self.window)
        gaupol.util.set_cursor_normal(self.window)
        gaupol.util.flash_dialog(dialog)

    def on_configure_spell_check_activate(self, *args):
        """Set languages and spell-check targets."""

        gaupol.util.set_cursor_busy(self.window)
        dialog = gaupol.LanguageDialog(self.window)
        gaupol.util.set_cursor_normal(self.window)
        gaupol.util.flash_dialog(dialog)
        self.update_gui()

    def on_correct_texts_activate(self, *args):
        """Find and correct errors in texts."""

        gaupol.util.set_cursor_busy(self.window)
        assistant = gaupol.TextAssistant(self.window, self)
        gaupol.util.set_cursor_normal(self.window)
        assistant.show()
