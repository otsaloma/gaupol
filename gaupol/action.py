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

"""Base classes for :class:`gtk.UIManager` actions."""

import aeidon
import gtk

__all__ = ("Action",
           "MenuAction",
           "RadioAction",
           "ToggleAction",
           "TopMenuAction",
           )


class Action(gtk.Action):

    """Base classes for :class:`gtk.UIManager` actions.

    :ivar accelerator: Accelerator string or ``None``

       :attr:`accelerator` defines a string in the format understood by the
       :func:`gtk.accelerator_parse`, ``None`` to use the stock accelerator or
       undefined to use a blank string.

    :ivar action_group: Name of action group to place action into

       Use "main-safe" for actions that do not conflict with widgets' own
       built-in keybindings (e.g. clipboard keybindings in entries) and
       "main-unsafe" for ones that do.

    :ivar widgets: Tuple of names of related application widgets

       :attr:`widgets` should be acquirable with :func:`getattr` from
       :class:`gaupol.Application`. Their sensitivities will be kep in sync.
    """

    accelerator = ""
    action_group = "main-unsafe"
    widgets = ()

    def __init__(self, name):
        """Initialize an :class:`Action` object."""
        gtk.Action.__init__(self, name, None, None, None)

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        pass

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "on_%s_activate" % self.props.name
        self.connect("activate", getattr(application, callback))

    def set_sensitive(self, sensitive):
        """Set the sensitivity of action and all its widgets."""
        for widget in self.widgets:
            widget.set_sensitive(sensitive)
        return gtk.Action.set_sensitive(self, sensitive)

    def update_sensitivity(self, application, page):
        """Update the sensitivity of action and all its widgets."""
        try:
            self._affirm_doable(application, page)
        except aeidon.AffirmationError:
            return self.set_sensitive(False)
        return self.set_sensitive(True)


class MenuAction(Action):

    """Base class for actions that are menu items with a submenu."""

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "on_%s_activate" % self.props.name
        if hasattr(application, callback):
            self.connect("activate", getattr(application, callback))


class ToggleAction(Action, gtk.ToggleAction):

    """Base class for UI manager toggle actions."""

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "on_%s_toggled" % self.props.name
        self.connect("toggled", getattr(application, callback))


class TopMenuAction(MenuAction):

    """Base class for actions that are top-level menu items with a submenu."""

    def update_sensitivity(self, application, page):
        """Update the sensitivity of action and all its widgets."""
        pass


class RadioAction(ToggleAction, gtk.RadioAction):

    """Base class for :class:`gtk.UIManager` radio actions.

    :ivar group: Class name of one action in the radio group
    """

    group = NotImplementedError

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        if self.__class__.__name__ != self.group: return
        callback = "on_%s_changed" % self.props.name
        self.connect("changed", getattr(application, callback))
