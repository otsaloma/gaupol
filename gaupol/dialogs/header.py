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

"""Dialog for editing subtitle file headers."""

import gaupol
import gtk
_ = aeidon.i18n._

__all__ = ("HeaderDialog",)


class HeaderDialog(gaupol.GladeDialog):

    """Dialog for editing subtitle file headers."""

    __metaclass__ = aeidon.Contractual

    def __init___require(self, parent, application):
        page = application.get_current_page()
        has_header_count = 0
        if page.project.main_file is not None:
            if page.project.main_file.format.has_header:
                has_header_count += 1
        if page.project.tran_file is not None:
            if page.project.tran_file.format.has_header:
                has_header_count += 1
        assert has_header_count > 0

    def __init__(self, parent, application):
        """Initialize an HeaderDialog object."""

        gaupol.GladeDialog.__init__(self, "header.glade")
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
        self.application = application

        self._init_signal_handlers()
        self._init_values()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    @property
    def _main_file(self):
        """Return the main file of the current page's project."""

        page = self.application.get_current_page()
        return page.project.main_file

    @property
    def _tran_file(self):
        """Return the translation file of the current page's project."""

        page = self.application.get_current_page()
        return page.project.tran_file

    def _get_main_header(self):
        """Return main header from the text view."""

        text_buffer = self._main_text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def _get_translation_header(self):
        """Return translation header from the text view."""

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

        aeidon.util.connect(self, "_copy_down_button", "clicked")
        aeidon.util.connect(self, "_copy_up_button", "clicked")
        aeidon.util.connect(self, "_main_clear_button", "clicked")
        aeidon.util.connect(self, "_main_revert_button", "clicked")
        aeidon.util.connect(self, "_main_template_button", "clicked")
        aeidon.util.connect(self, "_tran_clear_button", "clicked")
        aeidon.util.connect(self, "_tran_revert_button", "clicked")
        aeidon.util.connect(self, "_tran_template_button", "clicked")
        aeidon.util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label(("m" * 40 + "\n") * 12)
        width, height = label.size_request()
        width = width + 166 + gaupol.EXTRA
        if self._main_vbox.props.visible and self._tran_vbox.props.visible:
            height = 2 * height + 205 + gaupol.EXTRA
        elif self._main_vbox.props.visible or self._tran_vbox.props.visible:
            height = height + 90 + gaupol.EXTRA
        # TODO: FIX!
        # gaupol.util.resize_dialog(self, width, height)

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

        format = self._main_file.format
        self._set_main_header(aeidon.util.get_template_header(format))

    def _on_main_revert_button_clicked(self, *args):
        """Restore the original main header."""

        self._set_main_header(self._main_file.header)

    def _on_response(self, dialog, response):
        """Save the subtitle file headers."""

        if response == gtk.RESPONSE_OK:
            self._save_headers()

    def _on_tran_clear_button_clicked(self, *args):
        """Set a blank string as the translation header."""

        self._set_translation_header("")

    def _on_tran_template_button_clicked(self, *args):
        """Set translation header to the template of its format."""

        format = self._tran_file.format
        self._set_translation_header(aeidon.util.get_template_header(format))

    def _on_tran_revert_button_clicked(self, *args):
        """Restore the original translation header."""

        self._set_translation_header(self._tran_file.header)

    def _save_header(self, file, header):
        """Save the subtitle file header."""

        if file.format == aeidon.formats.MPSUB:
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

    def _save_mpsub_header(self, file, header):
        """Save the MPsub subtitle file header."""

        try: # Fails if bad FORMAT line.
            file.set_header(unicode(header))
        except ValueError:
            return self._show_mpsub_error_dialog()
        if file.framerate is None: return
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
        message = _('MPsub header must contain a line of form "FORMAT=VALUE", '
            'where VALUE is any of "TIME", "23.98", "25.00" or "29.97".')
        dialog = gaupol.ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        gaupol.util.flash_dialog(dialog)
