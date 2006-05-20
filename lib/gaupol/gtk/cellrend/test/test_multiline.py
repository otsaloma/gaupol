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


from gaupol.gtk.cellrend.multiline import TextViewCell
from gaupol.gtk.cellrend.multiline import CellRendererMultilineText
from gaupol.test                   import Test


class TestTextViewCell(Test):

    def setup_method(self, method):

        self.text_view = TextViewCell()

    def test_editing_done(self):

        self.text_view.editing_done()

    def test_get_and_set_text(self):

        self.text_view.set_text('test')
        text = self.text_view.get_text()
        assert text == 'test'


class TestCellRendererMultilineText(Test):

    def test_init(self):

        CellRendererMultilineText()


if __name__ == '__main__':

    import gobject
    import gtk

    tree_view = gtk.TreeView()
    tree_view.set_headers_visible(False)
    store = gtk.ListStore(gobject.TYPE_STRING)
    store.append(['test\ntest'])
    tree_view.set_model(store)

    cell_renderer = CellRendererMultilineText()
    cell_renderer.set_editable(True)
    tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
    tree_view.append_column(tree_view_column)

    window = gtk.Window()
    window.connect('delete-event', gtk.main_quit)
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_default_size(240, 70)
    window.add(tree_view)
    window.show_all()
    gtk.main()
