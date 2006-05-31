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


"""Gaupol GTK user interface controller."""


try:
    from psyco.classes import *
except ImportError:
    pass

import types

import gtk

from gaupol.gtk.delegates import Delegates
from gaupol.gtk.util      import config


class Application(object):

    """Gaupol GTK user interface controller."""

    def __init__(self):

        self.pages = []

        # Counter for naming unsaved projects
        self.counter = 0

        # Widgets
        self.framerate_combo = None
        self.main_statusbar  = None
        self.msg_statusbar   = None
        self.notebook        = None
        self.open_button     = None
        self.output_window   = None
        self.redo_button     = None
        self.tran_statusbar  = None
        self.undo_button     = None
        self.video_button    = None
        self.video_label     = None
        self.window          = None

        # UI manager and merge IDs
        self.uim             = None
        self.projects_uim_id = None
        self.recent_uim_id   = None

        # GObject timeout tag for message statusbar.
        self.message_tag = None

        # Tooltips, which are always enabled
        self.static_tooltips = gtk.Tooltips()

        # Tooltips, which are enabled when a document is open
        self.tooltips = gtk.Tooltips()

        # X clipboard
        self.clipboard = gtk.Clipboard()

        self.find_active = False

        self._delegations = {}
        self._init_delegations()

        config.read()
        self.init_gui()

    def _init_delegations(self):
        """Initialize delegate mappings."""

        # Loop through all delegates creating an instance of the delegate and
        # mapping all its methods that don't start with an underscore to that
        # instance.
        for cls in Delegates.classes:
            delegate = cls(self)
            for name in dir(delegate):
                if name.startswith('_'):
                    continue
                value = getattr(delegate, name)
                if type(value) == types.MethodType:
                    self._delegations[name] = delegate

    def __getattr__(self, name):
        """Delegate method calls to delegate objects."""

        return self._delegations[name].__getattribute__(name)

    def get_current_page(self):
        """
        Get currently active page.

        Return Page or None if no pages exist.
        """
        try:
            return self.pages[self.notebook.get_current_page()]
        except IndexError:
            return None

    def get_next_page(self, wrap=True):

        current_page = self.get_current_page()
        if current_page is None:
            return None

        index = self.pages.index(current_page)
        if index == len(self.pages) - 1:
            if not wrap:
                raise StopIteration
            return self.pages[0]
        else:
            return self.pages[index + 1]

    def get_page_count(self):

        return len(self.pages)

    def set_active_page(self, page):

        index = self.pages.index(page)
        self.notebook.set_current_page(index)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestApplication(Test):

        def test_init(self):

            application = Application()
            application.window.destroy()

    TestApplication().run()
