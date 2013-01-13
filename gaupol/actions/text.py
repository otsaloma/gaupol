# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Text processing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk


class ConfigureSpellCheckAction(gaupol.Action):

    """Set languages and spell-check targets."""

    def __init__(self):
        """Initialize a :class:`ConfigureSpellCheckAction` object."""
        gaupol.Action.__init__(self, "configure_spell_check")
        self.props.label = _("Co_nfigure Spell-check…")
        self.props.tooltip = _("Set language and spell-check target")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(aeidon.util.enchant_available())


class CheckSpellingAction(gaupol.Action):

    """Check for incorrect spelling."""

    def __init__(self):
        """Initialize a :class:`CheckSpellingAction` object."""
        gaupol.Action.__init__(self, "check_spelling")
        self.props.label = _("_Check Spelling")
        self.props.short_label = _("Spelling")
        self.props.stock_id = Gtk.STOCK_SPELL_CHECK
        self.props.tooltip = _("Check for incorrect spelling")
        self.accelerator = "F7"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(aeidon.util.enchant_available())
        aeidon.util.affirm(gaupol.conf.spell_check.language)


class CorrectTextsAction(gaupol.Action):

    """Find and correct errors in texts."""

    def __init__(self):
        """Initialize a :class:`CorrectTextsAction` object."""
        gaupol.Action.__init__(self, "correct_texts")
        self.props.label = _("C_orrect Texts…")
        self.props.tooltip = _("Find and correct errors in texts")
        self.accelerator = "O"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
