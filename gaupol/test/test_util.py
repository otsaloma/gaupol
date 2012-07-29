# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2012 Osmo Salomaa
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
import imp
import sys

from gi.repository import Gtk


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

    def test_get_content_size__text_view(self):
        gaupol.util.get_content_size(Gtk.TextView())

    def test_get_content_size__tree_view(self):
        tree_view = Gtk.TreeView()
        scroller = Gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.get_content_size(tree_view)

    def test_get_content_size__value_error(self):
        self.assert_raises(ValueError,
                           gaupol.util.get_content_size,
                           None)

    def test_get_font__none(self):
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = None
        assert gaupol.util.get_font() == ""

    def test_get_font__set(self):
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "Serif 12"
        assert gaupol.util.get_font() == "Serif 12"

    def test_get_font__unset(self):
        gaupol.conf.editor.use_custom_font = False
        assert gaupol.util.get_font() == ""

    def test_get_gst_version(self):
        imp.reload(gaupol.util)
        assert gaupol.util.get_gst_version()

    def test_get_preview_command__custom(self):
        gaupol.conf.preview.use_custom_command = True
        gaupol.util.get_preview_command()

    def test_get_preview_command__default(self):
        gaupol.conf.preview.use_custom_command = False
        gaupol.conf.preview.force_utf_8 = False
        gaupol.util.get_preview_command()

    def test_get_preview_command__utf_8(self):
        gaupol.conf.preview.use_custom_command = False
        gaupol.conf.preview.force_utf_8 = True
        gaupol.util.get_preview_command()

    def test_get_text_view_size(self):
        text_view = Gtk.TextView()
        gaupol.util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):
        tree_view = Gtk.TreeView()
        scroller = Gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.get_tree_view_size(tree_view)

    def test_gst_available(self):
        imp.reload(gaupol.util)
        assert gaupol.util.gst_available()

    def test_gtkspell_available(self):
        imp.reload(gaupol.util)
        # XXX: GtkSpell not yet available for PyGI.
        # assert gaupol.util.gtkspell_available()
        gaupol.util.gtkspell_available()

    def test_lines_to_px(self):
        assert gaupol.util.lines_to_px(1) > 0

    def test_pocketsphinx_available(self):
        gaupol.util.pocketsphinx_available()

    def test_prepare_text_view__hide_lengths(self):
        gaupol.util.prepare_text_view(Gtk.TextView())
        gaupol.conf.editor.show_lengths_edit = False
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "Serif 12"

    def test_prepare_text_view__show_lengths(self):
        gaupol.util.prepare_text_view(Gtk.TextView())
        gaupol.conf.editor.show_lengths_edit = True
        gaupol.conf.editor.use_custom_font = False
        gaupol.conf.editor.custom_font = ""

    def test_raise_default(self):
        self.assert_raises(gaupol.Default, gaupol.util.raise_default, True)
        gaupol.util.raise_default(False)

    def test_scale_to_content__text_view(self):
        text_view = Gtk.TextView()
        scroller = Gtk.ScrolledWindow()
        scroller.add(text_view)
        gaupol.util.scale_to_content(text_view,
                                     min_nchar=1,
                                     max_nchar=80,
                                     min_nlines=2,
                                     max_nlines=10)

    def test_scale_to_content__tree_view(self):
        tree_view = Gtk.TreeView()
        scroller = Gtk.ScrolledWindow()
        scroller.add(tree_view)
        gaupol.util.scale_to_content(tree_view,
                                     min_nchar=1,
                                     max_nchar=80,
                                     min_nlines=2,
                                     max_nlines=10,
                                     font="monospace")

    def test_scale_to_size__text_view(self):
        gaupol.util.scale_to_size(Gtk.TextView(),
                                  nchar=40,
                                  nlines=5)

    def test_scale_to_size__tree_view(self):
        gaupol.util.scale_to_size(Gtk.TreeView(),
                                  nchar=40,
                                  nlines=5,
                                  font="monospace")

    def test_separate_combo(self):
        combo_box = Gtk.ComboBox()
        func = gaupol.util.separate_combo
        combo_box.set_row_separator_func(func, None)

    def test_set_cursor_busy(self):
        window = Gtk.Window()
        window.show_all()
        gaupol.util.set_cursor_normal(window)
        gaupol.util.set_cursor_busy(window)
        window.destroy()

    def test_set_cursor_normal(self):
        window = Gtk.Window()
        window.show_all()
        gaupol.util.set_cursor_busy(window)
        gaupol.util.set_cursor_normal(window)
        window.destroy()

    def test_set_widget_font(self):
        label = Gtk.Label(label="testing...")
        gaupol.util.set_widget_font(label, "Serif 12")

    def test_show_uri(self):
        gaupol.util.show_uri(gaupol.HOMEPAGE_URL)

    @aeidon.deco.monkey_patch(sys, "platform")
    def test_show_uri__windows(self):
        sys.platform = "win32"
        gaupol.util.show_uri(gaupol.HOMEPAGE_URL)

    def test_text_field_to_document(self):
        field2doc = gaupol.util.text_field_to_document
        doc = field2doc(gaupol.fields.MAIN_TEXT)
        assert doc == aeidon.documents.MAIN
        doc = field2doc(gaupol.fields.TRAN_TEXT)
        assert doc == aeidon.documents.TRAN

    def test_tree_path_to_row(self):
        path = gaupol.util.tree_row_to_path(1)
        assert gaupol.util.tree_path_to_row(path) == 1
        assert gaupol.util.tree_path_to_row("1") == 1

    def test_tree_row_to_path(self):
        path = gaupol.util.tree_row_to_path(1)
        assert gaupol.util.tree_path_to_row(path) == 1
