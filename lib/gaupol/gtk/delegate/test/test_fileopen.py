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

from gaupol.gtk.app               import Application
from gaupol.gtk.delegate.fileopen import FileOpenDelegate
from gaupol.gtk.delegate.fileopen import _BigFileWarningDialog
from gaupol.gtk.delegate.fileopen import _FormatErrorDialog
from gaupol.gtk.delegate.fileopen import _IOErrorDialog
from gaupol.gtk.delegate.fileopen import _SSAWarningDialog
from gaupol.gtk.delegate.fileopen import _SortWarningDialog
from gaupol.gtk.delegate.fileopen import _TranslateWarningDialog
from gaupol.gtk.delegate.fileopen import _UnicodeErrorDialog
from gaupol.gtk.util              import conf, gtklib
from gaupol.test                  import Test


class TestBigFileWarningDialog(Test):

    def test_run(self):

        gtklib.run(_BigFileWarningDialog(gtk.Window(), 'test', 333.3))


class TestFileFormatErrorDialog(Test):

    def test_run(self):

        gtklib.run(_FormatErrorDialog(gtk.Window(), 'test'))


class TestIOErrorDialog(Test):

    def test_run(self):

        gtklib.run(_IOErrorDialog(gtk.Window(), 'test', 'test'))


class TestSortWarningDialog(Test):

    def test_run(self):

        gtklib.run(_SortWarningDialog(gtk.Window(), 333))


class TestSSAWarningDialog(Test):

    def test_run(self):

        gtklib.run(_SSAWarningDialog(gtk.Window()))


class TestTranslateWarningDialog(Test):

    def test_run(self):

        gtklib.run(_TranslateWarningDialog(gtk.Window(), 'test'))


class TestUnicodeErrorDialog(Test):

    def test_init(self):

        gtklib.run(_UnicodeErrorDialog(gtk.Window(), 'test'))


class TestFileOpenDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.delegate = FileOpenDelegate(self.app)
        self.app.open_main_files([self.get_subrip_path()])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_check_file_open(self):

        is_open = self.delegate._check_file_open('/open')
        assert not is_open

        path = self.get_subrip_path()
        self.app.open_main_files([path])
        is_open = self.delegate._check_file_open(path)
        assert is_open

    def test_get_encodings(self):

        encodings = self.delegate._get_encodings()
        assert len(encodings) > 0
        for encoding in encodings:
            assert isinstance(encoding, basestring)

        encodings = self.delegate._get_encodings('johab')
        assert encodings[0] == 'johab'
        assert len(encodings) > 0
        for encoding in encodings:
            assert isinstance(encoding, basestring)

    def test_add_to_recent_files(self):

        path = self.get_subrip_path()
        self.app.add_to_recent_files(path)
        assert path in conf.file.recents

    def test_on_append_file_activate(self):

        self.app.on_append_file_activate()

    def test_on_new_project_activate(self):

        self.app.on_new_project_activate()

    def test_on_open_button_clicked(self):

        self.app.on_open_button_clicked()

    def test_on_open_main_file_activate(self):

        self.app.on_open_main_file_activate()

    def test_on_open_translation_file_activate(self):

        self.app.on_open_translation_file_activate()

    def test_on_select_video_file_activate(self):

        self.app.on_select_video_file_activate()

    def test_on_split_project_activate(self):

        self.app.on_split_project_activate()

    def test_on_video_button_clicked(self):

        self.app.on_video_button_clicked()

    def test_validate_recent(self):

        self.app.validate_recent()
