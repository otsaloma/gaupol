# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for editing subtitle file headers."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk

__all__ = ("HeaderDialog",)


class HeaderDialog(gaupol.BuilderDialog):

    """Dialog for editing subtitle file headers."""

    _widgets = ("main_clear_button",
                "main_revert_button",
                "main_template_button",
                "main_text_view",
                "main_vbox",
                "tran_clear_button",
                "tran_revert_button",
                "tran_template_button",
                "tran_text_view",
                "tran_vbox")

    def __init__(self, parent, application):
        """Initialize a :class:`HeaderDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "header-dialog.ui")
        self.application = application
        gaupol.util.set_widget_font(self._main_text_view, "monospace")
        gaupol.util.set_widget_font(self._tran_text_view, "monospace")
        self._init_values()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.OK)

    def _get_main_header(self):
        """Return main header from text view."""
        text_buffer = self._main_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _get_translation_header(self):
        """Return translation header from text view."""
        text_buffer = self._tran_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _init_sizes(self):
        """Initialize widget sizes."""
        main = bool(self._main_file and self._main_file.format.has_header)
        tran = bool(self._tran_file and self._tran_file.format.has_header)
        nlines = (10 if main and tran else 15)
        if self._main_vbox.props.visible:
            gaupol.util.scale_to_size(self._main_text_view,
                                      nchar=60,
                                      nlines=nlines,
                                      font="monospace")

        if self._tran_vbox.props.visible:
            gaupol.util.scale_to_size(self._tran_text_view,
                                      nchar=60,
                                      nlines=nlines,
                                      font="monospace")

    def _init_values(self):
        """Initialize default values for widgets."""
        main = bool(self._main_file and self._main_file.format.has_header)
        tran = bool(self._tran_file and self._tran_file.format.has_header)
        self._main_vbox.props.visible = main
        self._tran_vbox.props.visible = tran
        self._set_main_header(self._main_file.header if main else "")
        self._set_translation_header(self._tran_file.header if tran else "")

    @property
    def _main_file(self):
        """Return the main file of the current page's project."""
        page = self.application.get_current_page()
        return page.project.main_file

    def _on_main_clear_button_clicked(self, *args):
        """Set a blank string as main header."""
        self._set_main_header("")

    def _on_main_template_button_clicked(self, *args):
        """Set main header to the template of its format."""
        format = self._main_file.format
        self._set_main_header(aeidon.util.get_template_header(format))

    def _on_main_revert_button_clicked(self, *args):
        """Restore original main header."""
        self._set_main_header(self._main_file.header)

    def _on_response(self, dialog, response):
        """Save headers."""
        if response == Gtk.ResponseType.OK:
            self._save_headers()

    def _on_tran_clear_button_clicked(self, *args):
        """Set a blank string as translation header."""
        self._set_translation_header("")

    def _on_tran_template_button_clicked(self, *args):
        """Set translation header to the template of its format."""
        format = self._tran_file.format
        self._set_translation_header(aeidon.util.get_template_header(format))

    def _on_tran_revert_button_clicked(self, *args):
        """Restore original translation header."""
        self._set_translation_header(self._tran_file.header)

    def _save_header(self, file, header):
        """Save `header` for `file`."""
        file.header = header

    def _save_headers(self):
        """Save headers."""
        if self._main_vbox.props.visible:
            self._save_header(self._main_file,
                              self._get_main_header())

        if self._tran_vbox.props.visible:
            self._save_header(self._tran_file,
                              self._get_translation_header())

        self.application.update_gui()

    def _set_main_header(self, header):
        """Set main `header` to text view."""
        self._main_text_view.get_buffer().set_text(header)

    def _set_translation_header(self, header):
        """Set translation `header` to text view."""
        self._tran_text_view.get_buffer().set_text(header)

    @property
    def _tran_file(self):
        """Return the translation file of the current page's project."""
        page = self.application.get_current_page()
        return page.project.tran_file
