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

import gaupol.gtk
import gtk.glade


class TestModule(gaupol.gtk.TestCase):

    def test_delay_add(self):

        gaupol.gtk.util.delay_add(10, lambda: None)

    def test_document_to_text_field(self):

        translate = gaupol.gtk.util.document_to_text_field
        field = translate(gaupol.documents.MAIN)
        assert field == gaupol.gtk.fields.MAIN_TEXT
        field = translate(gaupol.documents.TRAN)
        assert field == gaupol.gtk.fields.TRAN_TEXT
        self.raises(ValueError, translate, None)

    def test_get_font(self):

        assert gaupol.gtk.util.get_font() == ""
        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "Serif 12"
        assert gaupol.gtk.util.get_font() == "Serif 12"

    def test_get_glade_xml(self):

        gaupol.gtk.util.get_glade_xml("dialogs", "debug.glade")

    def test_get_text_view_size(self):

        text_view = gtk.TextView(gtk.TextBuffer())
        gaupol.gtk.util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):

        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.gtk.util.get_tree_view_size(tree_view)

    def test_prepare_text_view__no_show_lengths(self):

        gaupol.gtk.util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = False
        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "Serif 12"

    def test_prepare_text_view__show_lengths(self):

        gaupol.gtk.util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = True
        gaupol.gtk.conf.editor.use_custom_font = False
        gaupol.gtk.conf.editor.custom_font = ""

    def test_raise_default(self):

        function = gaupol.gtk.util.raise_default
        self.raises(gaupol.gtk.Default, function, True)
        gaupol.gtk.util.raise_default(False)

    def test_resize_dialog(self):

        dialog = gtk.Dialog()
        gaupol.gtk.util.resize_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        gaupol.gtk.util.resize_dialog(dialog, 2000, 2000, 0.3)
        width, height = dialog.get_size()
        assert width < gtk.gdk.screen_width()
        assert height < gtk.gdk.screen_height()

    def test_resize_message_dialog(self):

        dialog = gtk.Dialog()
        gaupol.gtk.util.resize_message_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        gaupol.gtk.util.resize_message_dialog(dialog, 2000, 2000, 0.3)
        width, height = dialog.get_size()
        assert width < gtk.gdk.screen_width()
        assert height < gtk.gdk.screen_height()

    def test_separate_combo(self):

        combo_box = gtk.ComboBox()
        combo_box.set_row_separator_func(gaupol.gtk.util.separate_combo)

    def test_set_button(self):

        button = gtk.Button(gtk.STOCK_CLOSE)
        gaupol.gtk.util.set_button(button, "test")
        gaupol.gtk.util.set_button(button, "test", gtk.STOCK_QUIT)
        gaupol.gtk.util.set_button(button, "test")

    def test_set_cursor_busy(self):

        window = gtk.Window()
        window.show_all()
        gaupol.gtk.util.set_cursor_normal(window)
        gaupol.gtk.util.set_cursor_busy(window)
        window.destroy()

    def test_set_cursor_normal(self):

        window = gtk.Window()
        window.show_all()
        gaupol.gtk.util.set_cursor_busy(window)
        gaupol.gtk.util.set_cursor_normal(window)
        window.destroy()

    def test_set_label_font(self):

        label = gtk.Label("testing...")
        gaupol.gtk.util.set_label_font(label, "Serif 12")

    def test_set_widget_font(self):

        label = gtk.Label("testing...")
        gaupol.gtk.util.set_label_font(label, "Serif 12")

    def test_text_field_to_document(self):

        translate = gaupol.gtk.util.text_field_to_document
        doc = translate(gaupol.gtk.fields.MAIN_TEXT)
        assert doc == gaupol.documents.MAIN
        doc = translate(gaupol.gtk.fields.TRAN_TEXT)
        assert doc == gaupol.documents.TRAN
        self.raises(ValueError, translate, None)
