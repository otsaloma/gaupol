# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Dialog for editing subtitle file headers."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .glade import GladeDialog
from .message import ErrorDialog


class HeaderDialog(GladeDialog):

    """Dialog for editing subtitle file headers."""

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "header-dialog")
        get_widget = self._glade_xml.get_widget
        self._copy_down_button = get_widget("copy_down_button")
        self._copy_hbox = get_widget("copy_hbox")
        self._copy_up_button = get_widget("copy_up_button")
        self._main_clear_button = get_widget("main_clear_button")
        self._main_revert_button = get_widget("main_revert_button")
        self._main_template_button = get_widget("main_template_button")
        self._main_text_view = get_widget("main_text_view")
        self._main_vbox = get_widget("main_vbox")
        self._tran_clear_button = get_widget("tran_clear_button")
        self._tran_revert_button = get_widget("tran_revert_button")
        self._tran_template_button = get_widget("tran_template_button")
        self._tran_text_view = get_widget("tran_text_view")
        self._tran_vbox = get_widget("tran_vbox")

        page = application.get_current_page()
        self._main_file = page.project.main_file
        self._tran_file = page.project.tran_file
        self.application = application

        self._init_signal_handlers()
        self._init_values()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_main_header(self):
        """Get main header from the text view."""

        text_buffer = self._main_text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def _get_translation_header(self):
        """Get translation header from the text view."""

        text_buffer = self._tran_text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def _init_values(self):
        """Initialize the values of the headers."""

        main = bool(self._main_file and self._main_file.format.has_header)
        tran = bool(self._tran_file and self._tran_file.format.has_header)
        self._main_vbox.props.visible = main
        self._tran_vbox.props.visible = tran
        self._copy_hbox.props.visible = (main and tran)

        header = (self._main_file.header if main else "")
        self._set_main_header(header)
        header = (self._tran_file.header if tran else "")
        self._set_translation_header(header)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, "_copy_down_button", "clicked")
        gaupol.gtk.util.connect(self, "_copy_up_button", "clicked")
        gaupol.gtk.util.connect(self, "_main_clear_button", "clicked")
        gaupol.gtk.util.connect(self, "_main_revert_button", "clicked")
        gaupol.gtk.util.connect(self, "_main_template_button", "clicked")
        gaupol.gtk.util.connect(self, "_tran_clear_button", "clicked")
        gaupol.gtk.util.connect(self, "_tran_revert_button", "clicked")
        gaupol.gtk.util.connect(self, "_tran_template_button", "clicked")
        gaupol.gtk.util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label(("M" * 42 + "\n") * 12)
        width, height = label.size_request()
        width = width + 166 + gaupol.gtk.EXTRA
        if self._main_vbox.props.visible and self._tran_vbox.props.visible:
            height = 2 * height + 205 + gaupol.gtk.EXTRA
        elif self._main_vbox.props.visible or self._tran_vbox.props.visible:
            height = height + 90 + gaupol.gtk.EXTRA
        gaupol.gtk.util.resize_dialog(self, width, height)

    def _on_copy_down_button_clicked(self, *args):
        """Copy the main header to the translation header."""

        self._set_translation_header(self._get_main_header())

    def _on_copy_up_button_clicked(self, *args):
        """Copy the translation header to the main header."""

        self._set_main_header(self._get_translation_header())

    def _on_main_clear_button_clicked(self, *args):
        """Set a blank string as the main header."""

        self._set_main_header("")

    def _on_main_template_button_clicked(self, *args):
        """Set main header to the template of its format."""

        self._set_main_header(self._main_file.get_template_header())

    def _on_main_revert_button_clicked(self, *args):
        """Restore the original main header."""

        self._set_main_header(self._main_file.header)

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Save the subtitle file headers."""

        assert response == gtk.RESPONSE_OK
        self._save_headers()

    def _on_tran_clear_button_clicked(self, *args):
        """Set a blank string as the translation header."""

        self._set_translation_header("")

    def _on_tran_template_button_clicked(self, *args):
        """Set translation header to the template of its format."""

        self._set_translation_header(self._tran_file.get_template_header())

    def _on_tran_revert_button_clicked(self, *args):
        """Restore the original translation header."""

        self._set_translation_header(self._tran_file.header)

    def _save_header(self, file, header):
        """Save the subtitle file header."""

        if file.format == gaupol.gtk.FORMAT.MPSUB:
            return self._save_mpsub_header(file, header)
        file.header = unicode(header)

    def _save_headers(self):
        """Save the subtitle file headers."""

        if self._main_vbox.props.visible:
            header = self._get_main_header()
            self._save_header(self._main_file, header)
        if self._tran_vbox.props.visible:
            header = self._get_translation_header()
            self._save_header(self._tran_file, header)
        self.application.update_gui()

    @gaupol.gtk.util.asserted_return
    def _save_mpsub_header(self, file, header):
        """Save the MPsub subtitle file header."""

        try:
            file.set_header(unicode(header))
        except ValueError:
            return self._show_mpsub_error_dialog()
        assert file.framerate is not None
        page = self.application.get_current_page()
        page.project.set_framerate(file.framerate, register=None)

    def _set_main_header(self, header):
        """Set the value of the main header."""

        self._main_text_view.get_buffer().set_text(header)

    def _set_translation_header(self, header):
        """Set the value of the translation header."""

        self._tran_text_view.get_buffer().set_text(header)

    def _show_mpsub_error_dialog(self):
        """Show an error dialog if MPsub header is invalid."""

        title = _("Invalid header")
        message = _('MPsub header must contain a "FORMAT" line '
            'with a value of "TIME", "23.98", "25.00" or "29.97".')
        dialog = ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)
