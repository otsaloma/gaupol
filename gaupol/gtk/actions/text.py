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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Text processing actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .action import Action


class ConfigureSpellCheckAction(Action):

    """Set languages and spell-check targets."""

    def __init__(self):

        Action.__init__(self, "configure_spell_check")
        self.props.label = _("Co_nfigure Spell-check\342\200\246")
        self.props.tooltip = _("Set language and spell-check target")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert gaupol.gtk.util.enchant_available()


class CheckSpellingAction(Action):

    """Check for incorrect spelling."""

    def __init__(self):

        Action.__init__(self, "check_spelling")
        self.props.label = _("_Check Spelling")
        self.props.short_label = _("Spelling")
        self.props.stock_id = gtk.STOCK_SPELL_CHECK
        self.props.tooltip = _("Check for incorrect spelling")
        self.accelerator = "F7"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert gaupol.gtk.util.enchant_available()
        assert gaupol.gtk.conf.spell_check.language


class CorrectTextsAction(Action):

    """Find and correct errors in texts."""

    def __init__(self):

        Action.__init__(self, "correct_texts")
        self.props.label = _("C_orrect Texts\342\200\246")
        self.props.tooltip = _("Find and correct errors in texts")
        self.accelerator = "O"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
