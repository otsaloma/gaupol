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
from gaupol.gtk.util     import conf


class Application(object):

    """
    GTK user interface controller.

    Instance variables:

        _clipboard:       gtk.Clipboard (X clipboard)
        _counter:         Integer for naming unsaved projects
        _delegations:     Dictionary mapping method names to Delegates
        _framerate_combo: gtk.ComboBox
        _main_statusbar:  gtk.Statusbar
        _msg_statusbar:   gtk.Statusbar
        _notebook:        gtk.Notebook
        _open_button:     gtk.MenuToolButton
        _output_window:   OutputWindow
        _redo_button:     gtk.MenuToolButton
        _static_tooltips: gtk.Tooltips, enabled always
        _tooltips:        gtk.Tooltips, enbaled if a document is open
        _tran_statusbar:  gtk.Statusbar
        _uim:             gtk.UIManager
        _undo_button:     gtk.MenuToolButton
        _video_button:    gtk.Button
        _video_label:     gtk.Label
        _window:          gtk.Window
        pages:            List of Pages

    """

    def __getattr__(self, name):

        return self._delegations[name].__getattribute__(name)

    def __init__(self):

        self._clipboard       = gtk.Clipboard()
        self._counter         = 0
        self._delegations     = {}
        self._framerate_combo = None
        self._main_statusbar  = None
        self._msg_statusbar   = None
        self._notebook        = None
        self._open_button     = None
        self._output_window   = None
        self._redo_button     = None
        self._static_tooltips = gtk.Tooltips()
        self._tooltips        = gtk.Tooltips()
        self._tran_statusbar  = None
        self._uim             = None
        self._undo_button     = None
        self._video_button    = None
        self._video_label     = None
        self._window          = None
        self.pages            = []

        self._init_delegations()
        conf.read()
        self.init_gui()

    def _init_delegations(self):
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
        index = self._notebook.get_current_page()
        if index == -1:
            return None
        return self.pages[index]
