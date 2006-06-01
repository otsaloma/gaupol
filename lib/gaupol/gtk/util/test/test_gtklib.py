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


import gtk
import gtk.glade

from gaupol.gtk.util import gtklib
from gaupol.test     import Test


class TestModule(Test):

    def test_destroy_gobject(self):

        gtklib.destroy_gobject(gtk.Label())

    def test_get_glade_xml(self):

        glade_xml = gtklib.get_glade_xml('debug-dialog')
        assert isinstance(glade_xml, gtk.glade.XML)

    def test_get_event_box(self):

        label = gtk.Label()
        event_box = gtk.EventBox()
        event_box.add(label)
        widget = gtklib.get_event_box(label)
        assert widget == event_box

    def test_get_parent_widget(self):

        label = gtk.Label()
        event_box = gtk.EventBox()
        event_box.add(label)
        widget = gtklib.get_parent_widget(label, gtk.EventBox)
        assert widget == event_box

    def test_get_text_view_size(self):

        text_view = gtk.TextView(gtk.TextBuffer())
        size = gtklib.get_text_view_size(text_view)
        assert isinstance(size[0], int)
        assert isinstance(size[1], int)

    def test_get_tree_view_size(self):

        tree_view = gtk.TreeView()
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add(tree_view)
        size = gtklib.get_tree_view_size(tree_view)
        assert isinstance(size[0], int)
        assert isinstance(size[1], int)

    def test_resize_dialog(self):

        dialog = gtk.Dialog()
        gtklib.resize_dialog(dialog, 200, 200)
        size = dialog.get_size()
        assert size == (200, 200)

        dialog = gtk.Dialog()
        gtklib.resize_dialog(dialog, 200, 200, 0.5, 0.5)
        size = dialog.get_size()
        assert size == (200, 200)

        dialog = gtk.Dialog()
        gtklib.resize_dialog(dialog, 2000, 2000, 0.3, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_resize_message_dialog(self):

        dialog = gtk.Dialog()
        gtklib.resize_message_dialog(dialog, 200, 200)
        size = dialog.get_size()
        assert size == (200, 200)

        dialog = gtk.Dialog()
        gtklib.resize_message_dialog(dialog, 200, 200, 0.5, 0.5)
        size = dialog.get_size()
        assert size == (200, 200)

        dialog = gtk.Dialog()
        gtklib.resize_message_dialog(dialog, 2000, 2000, 0.3, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_set_cursors(self):

        window = gtk.Window()
        window.show_all()
        gtklib.set_cursor_busy(window)
        gtklib.set_cursor_normal(window)
        window.destroy()

    def test_set_label_font(self):

        gtklib.set_label_font(gtk.Label('test'), 'monospace 10')

    def test_set_widget_font(self):

        gtklib.set_label_font(gtk.Label('test'), 'monospace 10')
