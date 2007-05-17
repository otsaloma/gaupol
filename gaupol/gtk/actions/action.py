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


"""Base class for UI manager actions."""


class UIMAction(object):

    """Base class for UI manager actions.

    Class variables:

        action_item = (
            name,
            stock-id,
            label,
            accelerator,
            tooltip,)

        menu_item = (
            name,
            stock-id,
            label,
            accelerator,
            tooltip,)

        radio_items = (
            [(name,
              stock-id,
              label,
              accelerator,
              tooltip,
              index),
             (...),],
            value)

        toggle_item = (
            name,
            stock-id,
            label,
            accelerator,
            tooltip,
            active)

        paths:   List of UI manager paths for action
        widgets: List of attribute widget names for action
    """

    action_item = None
    menu_item   = None
    radio_items = None
    toggle_item = None
    paths       = []
    widgets     = []

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return True
