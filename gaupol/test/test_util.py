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

import gaupol
import gtk.glade


class TestModule(gaupol.TestCase):

    def test_delay_add(self):

        gaupol.util.delay_add(10, lambda: None)

    def test_document_to_text_field(self):

        translate = gaupol.util.document_to_text_field
        field = translate(aeidon.documents.MAIN)
        assert field == gaupol.fields.MAIN_TEXT
        field = translate(aeidon.documents.TRAN)
        assert field == gaupol.fields.TRAN_TEXT
        self.raises(ValueError, translate, None)

    def test_get_font(self):

        assert gaupol.util.get_font() == ""
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "Serif 12"
        assert gaupol.util.get_font() == "Serif 12"

    def test_get_glade_xml(self):

        gaupol.util.get_glade_xml("dialogs", "debug.glade")

    def test_get_preview_command(self):

        gaupol.conf.preview.use_custom = False
        for player in aeidon.players:
            gaupol.conf.preview.video_player = player
            gaupol.conf.preview.force_utf_8 = True
            command = gaupol.util.get_preview_command()
            assert command == player.command_utf_8
            gaupol.conf.preview.force_utf_8 = False
            command = gaupol.util.get_preview_command()
            assert command == player.command
        gaupol.conf.preview.use_custom = True
        command = gaupol.util.get_preview_command()
        assert command == gaupol.conf.preview.custom_command

    def test_get_text_view_size(self):

        text_view = gtk.TextView(gtk.TextBuffer())
        gaupol.util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):

        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.get_tree_view_size(tree_view)

    def test_prepare_text_view__no_show_lengths(self):

        gaupol.util.prepare_text_view(gtk.TextView())
        gaupol.conf.editor.show_lengths_edit = False
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "Serif 12"

    def test_prepare_text_view__show_lengths(self):

        gaupol.util.prepare_text_view(gtk.TextView())
        gaupol.conf.editor.show_lengths_edit = True
        gaupol.conf.editor.use_custom_font = False
        gaupol.conf.editor.custom_font = ""

    def test_raise_default(self):

        function = gaupol.util.raise_default
        self.raises(gaupol.Default, function, True)
        gaupol.util.raise_default(False)

    def test_resize_dialog(self):

        dialog = gtk.Dialog()
        gaupol.util.resize_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        gaupol.util.resize_dialog(dialog, 2000, 2000, 0.3)
        width, height = dialog.get_size()
        assert width < gtk.gdk.screen_width()
        assert height < gtk.gdk.screen_height()

    def test_resize_message_dialog(self):

        dialog = gtk.Dialog()
        gaupol.util.resize_message_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        gaupol.util.resize_message_dialog(dialog, 2000, 2000, 0.3)
        width, height = dialog.get_size()
        assert width < gtk.gdk.screen_width()
        assert height < gtk.gdk.screen_height()

    def test_separate_combo(self):

        combo_box = gtk.ComboBox()
        combo_box.set_row_separator_func(gaupol.util.separate_combo)

    def test_set_button(self):

        button = gtk.Button(gtk.STOCK_CLOSE)
        gaupol.util.set_button(button, "test")
        gaupol.util.set_button(button, "test", gtk.STOCK_QUIT)
        gaupol.util.set_button(button, "test")

    def test_set_cursor_busy(self):

        window = gtk.Window()
        window.show_all()
        gaupol.util.set_cursor_normal(window)
        gaupol.util.set_cursor_busy(window)
        window.destroy()

    def test_set_cursor_normal(self):

        window = gtk.Window()
        window.show_all()
        gaupol.util.set_cursor_busy(window)
        gaupol.util.set_cursor_normal(window)
        window.destroy()

    def test_set_label_font(self):

        label = gtk.Label("testing...")
        gaupol.util.set_label_font(label, "Serif 12")

    def test_set_widget_font(self):

        label = gtk.Label("testing...")
        gaupol.util.set_label_font(label, "Serif 12")

    def test_text_field_to_document(self):

        translate = gaupol.util.text_field_to_document
        doc = translate(gaupol.fields.MAIN_TEXT)
        assert doc == aeidon.documents.MAIN
        doc = translate(gaupol.fields.TRAN_TEXT)
        assert doc == aeidon.documents.TRAN
        self.raises(ValueError, translate, None)
