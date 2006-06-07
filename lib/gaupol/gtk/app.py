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


"""GTK user interface controller."""


import types

import gtk

from gaupol.gtk.delegate import Delegates
from gaupol.gtk.util     import config


class Application(object):

    """
    GTK user interface controller.

    Instance variables:

        _delegations    -- Dictionary mapping method names to Delegates
        clipboard       -- gtk.Clipboard (X clipboard)
        counter         -- Integer for naming unsaved projects
        find_active     -- True if a pattern set for find
        framerate_combo -- gtk.ComboBox
        main_statusbar  -- gtk.Statusbar
        msg_statusbar   -- gtk.Statusbar
        notebook        -- gtk.Notebook
        open_button     -- gtk.MenuToolButton
        output_window   -- OutputWindow
        pages           -- List of Pages
        redo_button     -- gtk.MenuToolButton
        static_tooltips -- gtk.Tooltips, enabled always
        tooltips        -- gtk.Tooltips, enbaled if a document is open
        tran_statusbar  -- gtk.Statusbar
        uim             -- gtk.UIManager
        undo_button     -- gtk.MenuToolButton
        video_button    -- gtk.Button
        video_label     -- gtk.Label
        window          -- gtk.Window

    """

    def __getattr__(self, name):

        return self._delegations[name].__getattribute__(name)

    def __init__(self):

        self._delegations    = {}
        self.clipboard       = gtk.Clipboard()
        self.counter         = 0
        self.find_active     = False
        self.framerate_combo = None
        self.main_statusbar  = None
        self.msg_statusbar   = None
        self.notebook        = None
        self.open_button     = None
        self.output_window   = None
        self.pages           = []
        self.redo_button     = None
        self.static_tooltips = gtk.Tooltips()
        self.tooltips        = gtk.Tooltips()
        self.tran_statusbar  = None
        self.uim             = None
        self.undo_button     = None
        self.video_button    = None
        self.video_label     = None
        self.window          = None

        self.__init_delegations()
        config.read()
        self.init_gui()

    def __init_delegations(self):
        """Initialize delegate mappings."""

        for cls in Delegates.classes:
            delegate = cls(self)
            for name in dir(delegate):
                if name.startswith('_'):
                    continue
                value = getattr(delegate, name)
                if type(value) is types.MethodType:
                    self._delegations[name] = delegate

    def get_current_page(self):
        """
        Get currently active page.

        Return Page or None.
        """
        index = self.notebook.get_current_page()
        if index == -1:
            return None
        return self.pages[index]
