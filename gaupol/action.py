# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010-2011 Osmo Salomaa
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

"""Base classes for :class:`Gtk.UIManager` actions."""

import aeidon
import gaupol
import sys

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Action",
           "MenuAction",
           "RadioAction",
           "RecentAction",
           "ToggleAction",
           "TopMenuAction",
           )


class Action(Gtk.Action):

    """
    Base classes for :class:`Gtk.UIManager` actions.

    :ivar accelerator: Accelerator string or ``None``

       :attr:`accelerator` defines a string in the format understood by
       :func:`Gtk.accelerator_parse`, ``None`` to use the stock accelerator or
       unset to use a blank string.

    :ivar action_group: Name of action group to place action into

       Use "main-safe" for actions that do not conflict with widgets' own
       built-in keybindings (e.g. clipboard keybindings in entries) and
       "main-unsafe" for ones that do.

    :ivar tool_item_type: Class of tool item widget

        The default value is :class:`Gtk.ToolButton`. For buttons with a menu
        attached, use :class:`Gtk.MenuToolButton`.

    :ivar widgets: Tuple of names of related application widgets

       :attr:`widgets` should be acquirable with :func:`getattr` from
       :class:`gaupol.Application`. Their sensitivities will be kep in sync
       with sensitivity of the corresponding action.
    """

    accelerator = ""
    action_group = "main-unsafe"
    tool_item_type = Gtk.ToolButton
    widgets = ()

    def __init__(self, name):
        """Initialize an :class:`Action` object."""
        GObject.GObject.__init__(self, name=name)

    def _affirm_doable(self, application, page):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        pass

    def do_create_tool_item(self):
        """Return a tool button widget."""
        # This is a really fucking strange way to replace the deprecated
        # Gtk.Action.set_tool_item_type function, but it seems to work.
        # UI manager or whoever will set the correct labels and icons.
        if self.tool_item_type is Gtk.ToolButton:
            return Gtk.ToolButton()
        if self.tool_item_type is Gtk.MenuToolButton:
            return Gtk.MenuToolButton()
        raise ValueError("Bad value for self.tool_item_type: {}"
                         .format(repr(self.tool_item_type)))

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "_on_{}_activate".format(self.props.name)
        self.connect("activate", getattr(application, callback))

    def set_sensitive(self, sensitive):
        """Set the sensitivity of action and all its widgets."""
        for widget in self.widgets:
            widget.set_sensitive(sensitive)
        return Gtk.Action.set_sensitive(self, sensitive)

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
        callback = "_on_{}_activate".format(self.props.name)
        if hasattr(application, callback):
            self.connect("activate", getattr(application, callback))


class RecentAction(Gtk.RecentAction, Action):

    """
    Base class for :class:`Gtk.UIManager` recent file actions.

    :ivar group: Name of :class:`Gtk.RecentFilter` group
    """

    group = NotImplementedError

    def __init__(self, name):
        """Initialize an :class:`RecentAction` object."""
        GObject.GObject.__init__(self, name=name)
        if sys.platform == "win32":
            self.set_show_icons(False)
        self.set_show_numbers(False)
        self.set_show_not_found(False)
        self.set_show_tips(True)
        self.set_sort_type(Gtk.RecentSortType.MRU)
        recent_filter = Gtk.RecentFilter()
        # XXX: Gtk.RecentData fields cannot be set and thus group
        # never gets saved and cannot be used to make a distinction
        # between video files and main and translation files.
        # https://bugzilla.gnome.org/show_bug.cgi?id=678401
        # recent_filter.add_group(self.group)

        # While waiting for a fix, let's use a mimetype filter,
        # which as a downside leaves out some rarer formats for
        # which we don't have a mimetype.
        recent_filter.add_mime_type("application/x-subrip")
        recent_filter.add_mime_type("text/x-microdvd")
        recent_filter.add_mime_type("text/x-mpsub")
        recent_filter.add_mime_type("text/x-ssa")
        recent_filter.add_mime_type("text/x-subviewer")
        self.add_filter(recent_filter)
        self.set_filter(recent_filter)
        self.set_limit(gaupol.conf.file.max_recent)

    def finalize(self, application):
        """Connect action to widgets of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "_on_{}_activate".format(self.props.name)
        if hasattr(application, callback):
            self.connect("activate", getattr(application, callback))
        callback = "_on_{}_item_activated".format(self.props.name)
        self.connect("item-activated", getattr(application, callback))


class ToggleAction(Gtk.ToggleAction, Action):

    """Base class for UI manager toggle actions."""

    def __init__(self, name):
        """Initialize an :class:`ToggleAction` object."""
        GObject.GObject.__init__(self, name=name)

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        callback = "_on_{}_toggled".format(self.props.name)
        self.connect("toggled", getattr(application, callback))


class TopMenuAction(MenuAction):

    """Base class for actions that are top-level menu items with a submenu."""

    def update_sensitivity(self, application, page):
        """Update the sensitivity of action and all its widgets."""
        pass


class RadioAction(Gtk.RadioAction, Action):

    """
    Base class for :class:`Gtk.UIManager` radio actions.

    :ivar group: Class name of one action in the radio group
    """

    group = NotImplementedError

    def __init__(self, name):
        """Initialize an :class:`RadioAction` object."""
        GObject.GObject.__init__(self, name=name, value=0)

    def finalize(self, application):
        """Connect action to widgets and methods of `application`."""
        self.widgets = tuple(getattr(application, x) for x in self.widgets)
        if self.__class__.__name__ == self.group:
            callback = "_on_{}_changed".format(self.props.name)
            self.connect("changed", getattr(application, callback))
