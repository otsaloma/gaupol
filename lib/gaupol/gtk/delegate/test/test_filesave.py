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

from gaupol.gtk                   import cons
from gaupol.gtk.app               import Application
from gaupol.gtk.delegate.filesave import FileSaveDelegate
from gaupol.gtk.delegate.filesave import _IOErrorDialog
from gaupol.gtk.delegate.filesave import _UnicodeErrorDialog
from gaupol.gtk.util              import gtklib
from gaupol.test                  import Test


class TestIOErrorDialog(Test):

    def test_run(self):

        gtklib.run(_IOErrorDialog(gtk.Window(), 'test', 'test'))


class TestUnicodeErrorDialog(Test):

    def test_run(self):

        gtklib.run(_UnicodeErrorDialog(gtk.Window(), 'test', 'utf_8'))


class TestFileSaveDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.delegate = FileSaveDelegate(self.app)

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_get_props(self):

        self.app.on_new_project_activate()
        page = self.app.get_current_page()
        props = self.delegate._get_main_props(page)
        assert props == (None, None, None, None)
        props = self.delegate._get_translation_props(page)
        assert props == (None, None, None, None)

        self.app.open_main_files([self.get_subrip_path()])
        page = self.app.get_current_page()
        props = self.delegate._get_main_props(page)
        assert props == (
            page.project.main_file.path,
            page.project.main_file.format,
            page.project.main_file.encoding,
            page.project.main_file.newlines
        )
        props = self.delegate._get_translation_props(page)
        assert props == (
            page.project.main_file.path,
            page.project.main_file.format,
            page.project.main_file.encoding,
            page.project.main_file.newlines
        )

        page.project = self.get_project()
        props = self.delegate._get_translation_props(page)
        assert props == (
            page.project.tran_file.path,
            page.project.tran_file.format,
            page.project.tran_file.encoding,
            page.project.tran_file.newlines
        )

    def test_actions(self):

        for i in range(2):
            self.app.open_main_files([self.get_subrip_path()])
            page = self.app.get_current_page()
            props = list(self.delegate._get_main_props(page))
            props[0] = self.get_subrip_path()
            page.project.save_translation_file(props)

        self.app.on_save_all_documents_activate()
        self.app.on_save_main_document_activate()
        self.app.on_save_main_document_as_activate()
        self.app.on_save_translation_document_activate()
        self.app.on_save_translation_document_as_activate()

    def test_on_edit_headers_activate(self):

        self.app.open_main_files([self.get_subrip_path()])
        page = self.app.get_current_page()
        props = (
            page.project.main_file.path,
            cons.Format.SUBVIEWER2,
            page.project.main_file.encoding,
            page.project.main_file.newlines
        )
        page.project.save_main_file(props)
        self.app.on_edit_headers_activate()
