# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Base classes for UI manager actions."""

import gaupol.gtk
import gtk

__all__ = (
    "Action",
    "MenuAction",
    "RadioAction",
    "ToggleAction",
    "TopMenuAction",)


class Action(gtk.Action):

    """Base class for UI manager actions.

    Instance variable 'accelerator' defines a string string in the format
    understood by the gtk.accelerator_parse, None to use the stock accelerator
    or undefined to use a blank string as a fallback. The 'widgets' instance
    variable defines a tuple of names of application widgets, acquirable with
    from application getattr, whose sensitivities should be synced with action.
    """

    # pylint: disable-msg=W0232

    accelerator = ""
    widgets = ()

    def __init__(self, name):

        gtk.Action.__init__(self, name, None, None, None)

    def _affirm_doable(self, application, page):
        """Raise AffirmationError if action cannot be done."""

        pass

    def finalize(self, application):
        """Connect action to the widgets and methods of application."""

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
        except gaupol.AffirmationError:
            return self.set_sensitive(False)
        return self.set_sensitive(True)


class MenuAction(Action):

    """Base class for actions that are menu items with a submenu."""

    def finalize(self, application):
        """Connect action to the widgets and methods of application."""

        self.widgets = tuple(getattr(application, x) for x in self.widgets)


class ToggleAction(Action, gtk.ToggleAction):

    """Base class for UI manager toggle actions."""

    def finalize(self, application):
        """Connect action to the widgets and methods of application."""

        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "on_%s_toggled" % self.props.name
        self.connect("toggled", getattr(application, callback))


class TopMenuAction(MenuAction):

    """Base class for actions that are top-level menu items with a submenu."""

    def update_sensitivity(self, application, page):
        """Update the sensitivity of action and all its widgets."""

        pass


class RadioAction(ToggleAction, gtk.RadioAction):

    """Base class for UI manager radio actions.

    Instance variable 'group' should be a unique string to recognize group
    members by the class name of the first of the radio actions. The actual
    'group' property is set once all the actions are instantiated.
    """

    def finalize(self, application):
        """Connect action to the widgets and methods of application."""

        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        if self.__class__.__name__ != self.group: return
        callback = "on_%s_changed" % self.props.name
        self.connect("changed", getattr(application, callback))
