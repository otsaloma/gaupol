# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Extensions for gaupol.gtk.app.Application."""


import inspect

from gaupol.base.delegate import Delegate


_MODULES = (
    'action',
    'appupdate',
    'edit',
    'fileclose',
    'fileopen',
    'filesave',
    'find',
    'format',
    'guiinit',
    'help',
    'menuupdate',
    'position',
    'pref',
    'preview',
    'spellcheck',
    'view',
    'viewupdate',
)


class Delegate(Delegate):

    """Base class for delegates."""

    pass


class UIMAction(object):

    """
    Base class for UI manager actions.

    Class variables:

        action_item = (
            name,
            stock-icon,
            label,
            accelerator,
            tooltip,
            callback
        )

        toggle_item = (
            name,
            stock-icon,
            label,
            accelerator,
            tooltip,
            callback,
            state
        )

        menu_item = (
            name,
            stock-icon,
            label
        )

        radio_items = (
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

        paths:   List of UI manager paths for action
        widgets: List of widget names for action

    Because the lists of UI manager items are evaluated on import before
    configuration file is read, toggle and radio items need some arbitrary
    value. A proper value is obtained through methods "get_toggle_value" and
    "get_radio_index", which can be defined to return a value based on the
    conf module.
    """

    action_item = None
    menu_item   = None
    radio_items = None
    toggle_item = None
    paths       = []
    widgets     = []

    @classmethod
    def get_radio_index(cls):
        """Get active index of radio items."""

        raise NotImplementedError

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        raise NotImplementedError

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        raise NotImplementedError


class Delegates(object):

    """All delegates."""

    classes = []


class UIMActions(object):

    """All UI manager actions."""

    classes = []


def list_classes():
    """List all delegate and action classes."""

    for module_name in _MODULES:
        path = 'gaupol.gtk.delegate.' + module_name
        module = __import__(path, None, None, [''])
        for name in dir(module):
            if name.startswith('_'):
                continue
            value = getattr(module, name)
            if inspect.getmodule(value) != module:
                continue
            try:
                if issubclass(value, Delegate):
                    Delegates.classes.append(value)
                elif issubclass(value, UIMAction):
                    UIMActions.classes.append(value)
            except TypeError:
                continue

if not Delegates.classes or not UIMActions.classes:
    list_classes()
