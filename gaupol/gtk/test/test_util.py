# Copyright (C) 2005-2007 Osmo Salomaa
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


import gaupol.gtk
import gtk.glade

from gaupol.gtk import unittest
from .. import util


class TestModule(unittest.TestCase):

    def test_attributes(self):

        assert hasattr(util, "COMBO_SEPARATOR")
        assert hasattr(util, "EXTRA")
        assert hasattr(util, "BUSY_CURSOR")
        assert hasattr(util, "HAND_CURSOR")
        assert hasattr(util, "INSERT_CURSOR")
        assert hasattr(util, "NORMAL_CURSOR")

    def test_document_to_text_column(self):

        doc = gaupol.gtk.DOCUMENT.MAIN
        col = util.document_to_text_column(doc)
        assert col == gaupol.gtk.COLUMN.MAIN_TEXT
        doc = gaupol.gtk.DOCUMENT.TRAN
        col = util.document_to_text_column(doc)
        assert col == gaupol.gtk.COLUMN.TRAN_TEXT

    def test_get_font(self):

        assert util.get_font() == ""
        gaupol.gtk.conf.editor.use_default_font = False
        gaupol.gtk.conf.editor.font = "Serif 12"
        assert util.get_font() == "Serif 12"

    def test_get_glade_xml(self):

        glade_xml = util.get_glade_xml("debug-dialog")
        glade_xml = util.get_glade_xml("debug-dialog", "text_view")

    def test_get_text_view_size(self):

        text_view = gtk.TextView(gtk.TextBuffer())
        width, height = util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):

        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        width, height = util.get_tree_view_size(tree_view)

    def test_prepare_text_view(self):

        util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = True
        gaupol.gtk.conf.editor.use_default_font = True
        gaupol.gtk.conf.editor.font = ""

        util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = False
        gaupol.gtk.conf.editor.use_default_font = False
        gaupol.gtk.conf.editor.font = "Serif 12"

    def test_resize_dialog(self):

        dialog = gtk.Dialog()
        util.resize_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        util.resize_dialog(dialog, 2000, 2000, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_resize_message_dialog(self):

        dialog = gtk.Dialog()
        util.resize_message_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        util.resize_message_dialog(dialog, 2000, 2000, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_separate_combo(self):

        combo_box = gtk.ComboBox()
        combo_box.set_row_separator_func(util.separate_combo)

    def test_set_button(self):

        button = gtk.Button(gtk.STOCK_CLOSE)
        util.set_button(button, "test")
        util.set_button(button, "test", gtk.STOCK_QUIT)
        button = gtk.Button(gtk.STOCK_CLOSE)
        util.set_button(button, "test", gtk.STOCK_QUIT)
        util.set_button(button, "test")

    def test_set_cursor_busy(self):

        window = gtk.Window()
        window.show_all()
        util.set_cursor_normal(window)
        util.set_cursor_busy(window)
        window.destroy()

    def test_set_cursor_normal(self):

        window = gtk.Window()
        window.show_all()
        util.set_cursor_busy(window)
        util.set_cursor_normal(window)
        window.destroy()

    def test_set_label_font(self):

        util.set_label_font(gtk.Label(""), "Serif 12")

    def test_set_widget_font(self):

        util.set_label_font(gtk.Label(""), "Serif 12")

    def test_text_column_to_document(self):

        col = gaupol.gtk.COLUMN.MAIN_TEXT
        doc = util.text_column_to_document(col)
        assert doc == gaupol.gtk.DOCUMENT.MAIN
        col = gaupol.gtk.COLUMN.TRAN_TEXT
        doc = util.text_column_to_document(col)
        assert doc == gaupol.gtk.DOCUMENT.TRAN
