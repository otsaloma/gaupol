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


"""Common delegate affairs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import inspect


# List of all delegate module names. Methods of listed modules will be imported
# into the delegation system.
module_names = [
    'action',
    'appupdate',
    'edit',
    'fileclose',
    'fileopen',
    'filesave',
    'format',
    'guiinit',
    'help',
    'menuupdate',
    'preferences',
    'preview',
    'spellcheck',
    'timing',
    'view',
    'viewupdate',
]


class Delegate(object):

    """
    Base class for delegates.

    The purpose of the methods in this class is to provide direct access to
    the master class's attributes by redirecting all self.attribute calls not
    found in the delegate class.
    """

    # Code borrowed from
    # "Automatic delegation as an alternative to inheritance" by Alex Martelli
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52295

    def __init__(self, master):

        self.__dict__['master'] = master

    def __getattr__(self, name):
        """Get value of master object's attribute."""

        return getattr(self.master, name)

    def __setattr__(self, name, value):
        """Set value of master object's attribute."""

        return setattr(self.master, name, value)


class UIMAction(object):

    """
    Base class for UI manager actions.

    UI manager items:

    Callback methods and widgets are defined as strings without self, e.g.
    "on_quit_activated" and "open_button".

    uim_menu_item = (
      name,
      stock-icon,
      label
    )

    uim_action_item = (
      name,
      stock-icon,
      label,
      accelerator,
      tooltip,
      callback
    )

    uim_toggle_items = (
      name,
      stock-icon,
      label,
      accelerator,
      tooltip,
      callback,
      state
    )

    uim_radio_items = (
      (
          (
              name,
              stock-icon,
              label,
              accelerator,
              tooltip,
              index
          ), (
              ...
          )
      ),
      active,
      callback
    )

    Additionally a list of custom toolbar widgets can be given.
    widgets = []

    Because the lists of UI manager items are evaluated on import before the
    settings are available, toggle and radio items need some arbitrary value. A
    better value is obtained through methods "get_uim_toggle_item_value" and
    "get_uim_radio_items_index", which can be defined to return a value based
    on the config module.
    """

    uim_menu_item   = None
    uim_action_item = None
    uim_toggle_item = None
    uim_radio_items = None
    uim_paths       = []
    widgets         = []

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""
        raise NotImplementedError

    @classmethod
    def get_uim_radio_items_index(cls):
        """Return the active index of the UI manager radio items."""
        raise NotImplementedError

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""
        raise NotImplementedError


class UIMActions(object):

    """All UI manager actions."""

    classes = []


class Delegates(object):

    """All delegates."""

    module_names = module_names
    classes = []


def list_delegate_classes():
    """List all delegate classes."""

    for module_name in Delegates.module_names:

        path = 'gaupol.gtk.delegates.' + module_name
        module = __import__(path, None, None, [''])

        for name in dir(module):

            if name.startswith('_'):
                continue

            value = getattr(module, name)
            if inspect.getmodule(value) != module:
                continue

            try:
                if issubclass(value, UIMAction):
                    UIMActions.classes.append(value)
                elif issubclass(value, Delegate):
                    Delegates.classes.append(value)
            except TypeError:
                continue


# List delegates if they have not yet been listed.
if not UIMActions.classes or not Delegates.classes:
    list_delegate_classes()
