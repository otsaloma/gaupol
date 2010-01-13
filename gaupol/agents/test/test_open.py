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

import functools
import gaupol
import gtk
import os


def adds_pages(count):

    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            application = args[0].application
            orig_length = len(application.pages)
            value = function(*args, **kwargs)
            final_length = len(application.pages)
            assert final_length == (orig_length + count)
            return value
        return inner_wrapper

    return outer_wrapper


class TestOpenAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_encoding_error_dialog("test")

    def run__show_format_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_format_error_dialog("test")

    def run__show_io_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_io_error_dialog("test", "test")

    def run__show_parse_error_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        format = aeidon.formats.SUBRIP
        self.delegate._show_parse_error_dialog("test", format)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_size_warning_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_size_warning_dialog("test", 2)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_sort_warning_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_translation_warning_dialog(self):

        flash_dialog = gaupol.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.open_main_files.im_self
        respond = lambda *args: gtk.RESPONSE_OK
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond
        get_filenames = lambda *args: [self.new_subrip_file()]
        gaupol.FileDialog.get_filenames = get_filenames

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog("test")

    def test__show_format_error_dialog(self):

        self.delegate._show_format_error_dialog("test")

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test", "test")

    def test__show_parse_error_dialog(self):

        format = aeidon.formats.SUBRIP
        self.delegate._show_parse_error_dialog("test", format)

    @aeidon.deco.silent(gaupol.Default)
    def test__show_size_warning_dialog(self):

        self.delegate._show_size_warning_dialog("test", 2)

    @aeidon.deco.silent(gaupol.Default)
    def test__show_sort_warning_dialog(self):

        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.silent(gaupol.Default)
    def test__show_translation_warning_dialog(self):

        page = self.application.get_current_page()
        respond = lambda *args: gtk.RESPONSE_YES
        self.delegate.flash_dialog = respond
        self.delegate._show_translation_warning_dialog(page)
        respond = lambda *args: gtk.RESPONSE_NO
        self.delegate.flash_dialog = respond
        self.delegate._show_translation_warning_dialog(page)

    @adds_pages(1)
    def test_add_new_page(self):

        self.application.add_new_page(self.get_page())

    def test_add_to_recent_files(self):

        add = self.delegate.add_to_recent_files
        format = aeidon.formats.SUBRIP
        add(self.new_subrip_file(), format, aeidon.documents.MAIN)
        add(self.new_subrip_file(), format, aeidon.documents.TRAN)

    @adds_pages(0)
    def test_append_file(self):

        self.application.append_file(self.new_subrip_file())
        self.application.append_file(self.new_subrip_file(), "ascii")

    def test_connect_to_view_signals(self):

        view = self.application.pages[0].view
        self.application.connect_to_view_signals(view)

    @adds_pages(0)
    def test_on_append_file_activate(self):

        self.application.get_action("append_file").activate()

    @adds_pages(1)
    def test_on_new_project_activate(self):

        self.application.get_action("new_project").activate()

    @adds_pages(1)
    def test_on_open_main_files_activate(self):

        self.application.get_action("open_main_files").activate()

    def test_on_open_translation_file_activate(self):

        page = self.application.get_current_page()
        self.application.get_action("open_translation_file").activate()
        page.project.set_text(0, aeidon.documents.TRAN, "")
        self.application.get_action("open_translation_file").activate()

    def test_on_select_video_file_activate(self):

        page = self.application.get_current_page()
        page.project.video_path = self.new_subrip_file()
        self.application.get_action("select_video_file").activate()

    def test_on_split_project_activate(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        flash_dialog = lambda *args: responder.next()
        self.delegate.flash_dialog = flash_dialog
        self.application.get_current_page().view.select_rows((3,))
        self.application.get_action("split_project").activate()
        self.application.get_current_page().view.select_rows((3,))
        self.application.get_action("split_project").activate()

    def test_on_video_button_clicked(self):

        self.application.video_button.emit("clicked")

    @adds_pages(0)
    def test__open_file(self):

        function = self.delegate._open_file
        path = self.new_subrip_file()
        doc = aeidon.documents.MAIN
        self.raises(gaupol.Default, function, path, (), doc)

    @adds_pages(3)
    def test_open_main_file(self):

        self.application.open_main_file(self.new_subrip_file())
        self.application.open_main_file(self.new_subrip_file(), "ascii")
        self.application.open_main_file(self.new_subrip_file(), "auto")

    @adds_pages(0)
    def test_open_main_file__format_error(self):

        path = self.new_subrip_file()
        open(path, "w").write("xxx\n")
        self.application.open_main_file(path)

    @adds_pages(0)
    def test_open_main_file__io_error(self):

        path = self.new_subrip_file()
        os.chmod(path, 0000)
        self.application.open_main_file(path)
        os.chmod(path, 0777)

    @adds_pages(0)
    def test_open_main_file__parse_error(self):

        read = lambda *args: 1 / 0
        real_read = aeidon.files.SubRip.read
        aeidon.files.SubRip.read = read
        path = self.new_subrip_file()
        self.application.open_main_file(path)
        aeidon.files.SubRip.read = real_read

    @adds_pages(0)
    def test_open_main_file__size(self):

        path = self.new_microdvd_file()
        fobj = open(path, "w")
        fobj.write("{30}{40}Testing...\n")
        fobj.write("{40}{50}Testing...\n")
        fobj.write("{10}{20}Testing...\n")
        fobj.write("{20}{30}Testing...\n")
        fobj.close()
        self.application.open_main_file(path)

    @adds_pages(4)
    def test_open_main_files(self):

        paths = (self.new_subrip_file(), self.new_microdvd_file())
        self.application.open_main_files(paths)
        paths = (self.new_subrip_file(), self.new_microdvd_file())
        self.application.open_main_files(paths, "ascii")
        self.application.open_main_files(paths)

    def test_open_translation_file(self):

        path = self.new_subrip_file()
        self.application.open_translation_file(path)
        path = self.new_subrip_file()
        self.application.open_translation_file(path, "ascii")
