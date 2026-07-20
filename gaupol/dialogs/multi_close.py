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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialog for warning when closing multiple documents."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

class MultiCloseDialog(Gtk.MessageDialog):

    """Dialog for warning when closing multiple documents."""

    def __init__(self, parent, application, pages):
        """Initialize a :class:`MultiCloseDialog` instance."""
        GObject.GObject.__init__(self,
                                 message_type=Gtk.MessageType.WARNING,
                                 text=_("Save changes to documents before closing?"),
                                 secondary_text=_("If you don't save, changes will be permanently lost."))

        self.application = application
        self.pages = tuple(pages)
        self._document_list = Gtk.ListBox()
        self._init_dialog(parent)
        self._init_document_list()

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("Close _Without Saving"), Gtk.ResponseType.NO)
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Save"), Gtk.ResponseType.YES)
        self.set_default_response(Gtk.ResponseType.YES)
        self.set_transient_for(parent)
        self.set_modal(True)
        aeidon.util.connect(self, self, "response")

    def _init_document_list(self):
        """Initialize the list of unsaved documents."""
        self._document_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self._document_list.set_show_separators(True)
        self._document_list.add_css_class("rich-list")
        for page in self.pages:
            if page.project.main_changed:
                self._append_document(page, aeidon.documents.MAIN)
            if page.project.tran_changed:
                self._append_document(page, aeidon.documents.TRAN)
        frame = Gtk.Frame(child=self._document_list)
        scroller = Gtk.ScrolledWindow(
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            propagate_natural_width=True,
            propagate_natural_height=True)
        scroller.set_max_content_height(gaupol.util.lines_to_px(12))
        scroller.set_child(frame)
        scroller.set_visible(bool(self._get_check_buttons()))
        gaupol.util.pack_start_expand(self.get_message_area(), scroller)

    def _append_document(self, page, doc):
        """Append a check button row for `doc` of `page`."""
        check = Gtk.CheckButton(label=page.get_basename(doc),
                                active=True,
                                hexpand=True,
                                focusable=True)

        check.connect("toggled", self._on_check_button_toggled)
        check.gaupol_page = page
        check.gaupol_document = doc
        row = Gtk.ListBoxRow(activatable=False, selectable=False)
        row.set_child(check)
        self._document_list.append(row)

    @aeidon.deco.listify
    def _get_check_buttons(self):
        """Return all check buttons in the document list."""
        for i in range(1_000_000):
            row = self._document_list.get_row_at_index(i)
            if not row: break
            yield row.get_child()

    def _on_check_button_toggled(self, check_button):
        """Update save button sensitivity."""
        sensitive = any(x.get_active() for x in self._get_check_buttons())
        self.set_response_sensitive(Gtk.ResponseType.YES, sensitive)

    def _on_response(self, dialog, response):
        """Save the selected documents and close pages."""
        if response == Gtk.ResponseType.YES:
            for page in self.pages:
                self._save_and_close_page(page)
        if response == Gtk.ResponseType.NO:
            for page in self.pages:
                self.application.close(page, confirm=False)

    @aeidon.deco.silent(gaupol.Default)
    def _save_and_close_page(self, page):
        """Save the selected documents and close `page`."""
        for check in self._get_check_buttons():
            if check.gaupol_page is page and check.get_active():
                self.application.save(page, check.gaupol_document)
        self.application.close(page, confirm=False)
