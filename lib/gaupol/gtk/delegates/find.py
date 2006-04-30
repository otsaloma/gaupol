# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Finding and replacing text."""


from gettext import gettext as _

import gtk

from gaupol.gtk.delegates    import Delegate, UIMAction
from gaupol.gtk.dialogs.find import FindDialog
from gaupol.gtk.util         import gtklib


class FindAction(UIMAction):

    """Finding text."""

    uim_action_item = (
        'find',
        gtk.STOCK_FIND,
        _('_Find...'),
        '<control>F',
        _('Search for text'),
        'on_find_activated'
    )

    uim_paths = ['/ui/menubar/search/find']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class FindNextAction(UIMAction):

    """Finding next match."""

    uim_action_item = (
        'find_next',
        None,
        _('Find _Next'),
        '<control>G',
        _('Search forwards for same text'),
        'on_find_next_activated'
    )

    uim_paths = ['/ui/menubar/search/next']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is not None:
            return False

        return application.find_active


class FindPreviousAction(UIMAction):

    """Finding previous match."""

    uim_action_item = (
        'find_previous',
        None,
        _('Find _Previous'),
        '<shift><control>G',
        _('Search backwards for same text'),
        'on_find_previous_activated'
    )

    uim_paths = ['/ui/menubar/search/previous']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is not None:
            return False

        return application.find_active


class ReplaceAction(UIMAction):

    """Replacing text."""

    uim_action_item = (
        'replace',
        gtk.STOCK_FIND_AND_REPLACE,
        _('_Replace...'),
        '<control>H',
        _('Search for and replace text'),
        'on_replace_activated'
    )

    uim_paths = ['/ui/menubar/search/replace']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class FindDelegate(Delegate):

    """Finding and replacing text."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self.__find_dialog    = None
        self.__replace_dialog = None

    def on_find_activated(self, *args):
        """Find text."""

        def _on_destroyed(dialog):
            gtklib.destroy_gobject(dialog)
            self.__find_dialog = None

        if self.__find_dialog is None:
            self.__find_dialog = FindDialog(self.window, self.master)
            self.__find_dialog.connect('destroyed', _on_destroyed)
        self.__find_dialog.present()

    def on_find_next_activated(self, *args):
        """Find next match."""

        pass

    def on_find_previous_activated(self, *args):
        """Find previous match."""

        pass

    def on_replace_activated(self, *args):
        """Replace text."""

        pass
