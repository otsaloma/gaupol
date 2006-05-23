# Copyright (C) 2005 Osmo Salomaa
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


"""Dialog for editing subtitle file headers."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.base.files.classes import *
from gaupol.base.cons          import Format
from gaupol.gtk.util           import config, gtklib


class HeaderDialog(object):

    """Dialog for editing subtitle file headers."""

    def __init__(self, parent, page):

        glade_xml = gtklib.get_glade_xml('header-dialog')
        get_widget = glade_xml.get_widget

        self._copy_down_button     = get_widget('copy_down_button')
        self._copy_hbox            = get_widget('copy_hbox')
        self._copy_up_button       = get_widget('copy_up_button')
        self._dialog               = get_widget('dialog')
        self._main_clear_button    = get_widget('main_clear_button')
        self._main_label           = get_widget('main_label')
        self._main_revert_button   = get_widget('main_revert_button')
        self._main_template_button = get_widget('main_template_button')
        self._main_text_view       = get_widget('main_text_view')
        self._main_vbox            = get_widget('main_vbox')
        self._tran_clear_button    = get_widget('translation_clear_button')
        self._tran_label           = get_widget('translation_label')
        self._tran_revert_button   = get_widget('translation_revert_button')
        self._tran_template_button = get_widget('translation_template_button')
        self._tran_text_view       = get_widget('translation_text_view')
        self._tran_vbox            = get_widget('translation_vbox')

        self.page = page

        # Original headers.
        self.main_header_orig = None
        self.tran_header_orig = None

        # Template headers.
        self.main_header_tmpl = None
        self.tran_header_tmpl = None

        self._init_signals()
        self._init_data()
        self._init_sizes(parent)

    def _init_data(self):
        """Initialize header data."""

        main_file = self.page.project.main_file
        tran_file = self.page.project.tran_file

        # Main header
        if main_file is not None and main_file.has_header:
            self.main_header_orig = main_file.header
            self._set_main_header(self.main_header_orig)
            class_name = Format.class_names[main_file.format]
            self.main_header_tmpl = eval(class_name).HEADER_TEMPLATE
        else:
            self._main_label.props.visible = False
            self._main_vbox.props.visible  = False
            self._copy_hbox.props.visible  = False

        # Translation header
        if tran_file is not None and tran_file.has_header:
            self.tran_header_orig = tran_file.header
            self._set_translation_header(self.tran_header_orig)
            class_name = Format.class_names[tran_file.format]
            self.tran_header_tmpl = eval(class_name).HEADER_TEMPLATE
        else:
            self._tran_label.props.visible = False
            self._tran_vbox.props.visible  = False
            self._copy_hbox.props.visible  = False

    def _init_signals(self):
        """Initialize signals."""

        buttons = (
            '_copy_down_button',
            '_copy_up_button',
            '_main_clear_button',
            '_main_template_button',
            '_main_revert_button',
            '_tran_clear_button',
            '_tran_template_button',
            '_tran_revert_button',
        )
        for button in buttons:
            method = eval('self._on%s_clicked' % button)
            getattr(self, button).connect('clicked', method)

    def _init_sizes(self, parent):
        """Initialize widget sizes."""

        # Request 66 ex for text view widths.
        label = gtk.Label('x' * 66)
        width = label.size_request()[0] + 166 + gtklib.EXTRA

        # Request heights depending on header height(s).
        if self._main_vbox.props.visible and self._tran_vbox.props.visible:
            main_height = gtk.Label(self.main_header_orig).size_request()[1]
            tran_height = gtk.Label(self.tran_header_orig).size_request()[1]
            height = max(main_height, tran_height) + 205 + gtklib.EXTRA
        elif self._main_vbox.props.visible:
            height = gtk.Label(self.main_header_orig).size_request()[1]
            height = height + 90 + gtklib.EXTRA
        elif self._tran_vbox.props.visible:
            height = gtk.Label(self.tran_header_orig).size_request()[1]
            height = height + 90 + gtklib.EXTRA

        gtklib.resize_dialog(self._dialog, width, height)
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_main_header(self):
        """Get main header."""

        text_buffer = self._main_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end)

    def get_translation_header(self):
        """Get translation header."""

        text_buffer = self._tran_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end)

    def _on_copy_down_button_clicked(self, button):
        """Copy main header to translation header."""

        header = self.get_main_header()
        self._set_translation_header(header)

    def _on_copy_up_button_clicked(self, button):
        """Copy translation header to main header."""

        header = self.get_translation_header()
        self._set_main_header(header)

    def _on_main_clear_button_clicked(self, button):
        """Clear main header."""

        self._set_main_header(u'')

    def _on_main_template_button_clicked(self, button):
        """Set main header to a template."""

        self._set_main_header(self.main_header_tmpl)

    def _on_main_revert_button_clicked(self, button):
        """Revert main header."""

        self._set_main_header(self.main_header_orig)

    def _on_tran_clear_button_clicked(self, button):
        """Clear translation header."""

        self._set_translation_header(u'')

    def _on_tran_template_button_clicked(self, button):
        """Set translation header to a template."""

        self._set_translation_header(self.tran_header_tmpl)

    def _on_tran_revert_button_clicked(self, button):
        """Revert translation header."""

        self._set_translation_header(self.tran_header_orig)

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def _set_main_header(self, header):
        """Set main header."""

        text_buffer = self._main_text_view.get_buffer()
        text_buffer.set_text(header)

    def _set_translation_header(self, header):
        """Set translation header."""

        text_buffer = self._tran_text_view.get_buffer()
        text_buffer.set_text(header)


if __name__ == '__main__':

    from gaupol.gtk.page import Page
    from gaupol.test     import Test

    class TestHeaderDialog(Test):

        def __init__(self):

            Test.__init__(self)

            page = Page()
            page.project = self.get_project()

            properties = [
                page.project.main_file.path,
                Format.SUBVIEWER2,
                'utf_8',
                page.project.main_file.newlines
            ]
            page.project.save_main_file(True, properties)
            properties[0] = page.project.tran_file.path
            page.project.save_translation_file(True, properties)

            self.dialog = HeaderDialog(gtk.Window(), page)
            self.main_header = page.project.main_file.header
            self.tran_header = page.project.main_file.header

        def test_get_headers(self):

            get_main = self.dialog.get_main_header
            get_tran = self.dialog.get_translation_header

            assert get_main() == self.main_header
            assert get_tran() == self.tran_header

        def test_signals(self):

            get_main = self.dialog.get_main_header
            get_tran = self.dialog.get_translation_header

            self.dialog._main_clear_button.emit('clicked')
            self.dialog._copy_down_button.emit('clicked')
            assert get_tran() == ''
            assert get_main() == get_tran()

            self.dialog._tran_template_button.emit('clicked')
            self.dialog._copy_up_button.emit('clicked')
            assert get_main() != ''
            assert get_main() == get_tran()

            self.dialog._main_clear_button.emit('clicked')
            assert get_main() == ''

            self.dialog._main_template_button.emit('clicked')
            assert get_main() != ''

            self.dialog._main_clear_button.emit('clicked')
            self.dialog._main_revert_button.emit('clicked')
            assert get_main() == self.main_header

            self.dialog._tran_clear_button.emit('clicked')
            assert get_tran() == ''

            self.dialog._tran_template_button.emit('clicked')
            assert get_tran() != ''

            self.dialog._tran_clear_button.emit('clicked')
            self.dialog._tran_revert_button.emit('clicked')
            assert get_tran() == self.tran_header

    TestHeaderDialog().run()
