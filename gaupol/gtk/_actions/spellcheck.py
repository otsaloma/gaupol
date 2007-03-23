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


"""Spell-checking actions."""


from gettext import gettext as _

from gaupol.gtk import util
from ._action import UIMAction


class ConfigureSpellCheckAction(UIMAction):

    """Set languages and spell-check targets."""

    action_item = (
        "configure_spell_check",
        None,
        _("Co_nfigure Spell-check..."),
        None,
        _("Set languages and spell-check targets"),)

    paths = ["/ui/menubar/tools/configure_spell_check"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return util.enchant_available()
