# Copyright (C) 2005-2008,200 Osmo Salomaa
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

import aeidon
import gaupol
import gtk


class TestModule(gaupol.TestCase):

    def test_char_to_px(self):
        assert gaupol.util.char_to_px(1) > 0
        assert gaupol.util.char_to_px(1, "monospace") > 0

    def test_delay_add(self):
        gaupol.util.delay_add(10, lambda: None)

    def test_document_to_text_field(self):
        doc2field = gaupol.util.document_to_text_field
        field = doc2field(aeidon.documents.MAIN)
        assert field == gaupol.fields.MAIN_TEXT
        field = doc2field(aeidon.documents.TRAN)
        assert field == gaupol.fields.TRAN_TEXT

    def test_get_font__set(self):
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "Serif 12"
        assert gaupol.util.get_font() == "Serif 12"

    def test_get_font__unset(self):
        gaupol.conf.editor.use_custom_font = False
        assert gaupol.util.get_font() == ""
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = None
        assert gaupol.util.get_font() == ""

    def test_get_preview_command(self):
        gaupol.conf.preview.use_custom = True
        gaupol.conf.preview.force_utf_8 = False
        gaupol.util.get_preview_command()
        gaupol.conf.preview.use_custom = False
        gaupol.conf.preview.force_utf_8 = True
        gaupol.util.get_preview_command()
        gaupol.conf.preview.use_custom = False
        gaupol.conf.preview.force_utf_8 = False
        gaupol.util.get_preview_command()

    def test_get_text_view_size(self):
        text_view = gtk.TextView(gtk.TextBuffer())
        gaupol.util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):
        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.get_tree_view_size(tree_view)

    def test_lines_to_px(self):
        assert gaupol.util.lines_to_px(1) > 0

    def test_prepare_text_view__hide_lengths(self):
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
        self.raises(gaupol.Default, gaupol.util.raise_default, True)
        gaupol.util.raise_default(False)

    def test_scale_to_content__text_view(self):
        text_view = gtk.TextView()
        scroller = gtk.ScrolledWindow()
        scroller.add(text_view)
        gaupol.util.scale_to_content(text_view, 1, 2, 80, 10)

    def test_scale_to_content__tree_view(self):
        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.scale_to_content(tree_view, 1, 2, 80, 10, "monospace")

    def test_scale_to_size(self):
        gaupol.util.scale_to_size(gtk.TextView(), 40, 5)
        gaupol.util.scale_to_size(gtk.TreeView(), 40, 5, "monospace")

    def test_separate_combo(self):
        combo_box = gtk.ComboBox()
        combo_box.set_row_separator_func(gaupol.util.separate_combo)

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

    def test_show_uri(self):
        gaupol.util.show_uri(gaupol.HOMEPAGE_URL)

    def test_text_field_to_document(self):
        field2doc = gaupol.util.text_field_to_document
        doc = field2doc(gaupol.fields.MAIN_TEXT)
        assert doc == aeidon.documents.MAIN
        doc = field2doc(gaupol.fields.TRAN_TEXT)
        assert doc == aeidon.documents.TRAN
