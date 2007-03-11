# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Closing projects and quitting Gaupol."""


import gtk
import os
from gettext import gettext as _

from gaupol.base import Delegate
from gaupol.gtk import conf, cons, util
from gaupol.gtk.dialogs import MultiCloseDialog, WarningDialog
from gaupol.gtk.errors import Default


class CloseAgent(Delegate):

    """Closing projects and quitting Gaupol."""

    # pylint: disable-msg=E0203,W0201

    def _close_all_pages(self):
        """Close all pages after confirmation.

        Raise Default to abort.
        """
        count = 0
        unsaved = None
        for page in self.pages:
            sub_count = len(self._need_confirmation(page))
            if sub_count > 0:
                count += sub_count
                unsaved = page
        if count == 1:
            self._confirm_page(unsaved)
        elif count > 1:
            self._confirm_multiple(self.pages)
        while self.pages:
            self.close(self.pages[-1], False)

    def _confirm_main(self, page):
        """Confirm closing main document.

        Raise Default to abort.
        """
        doc = cons.DOCUMENT.MAIN
        basename = page.get_main_basename()
        response = self._show_close_warning_dialog(doc, basename)
        if response == gtk.RESPONSE_YES:
            self.save_main(page)
        elif response != gtk.RESPONSE_NO:
            raise Default

    def _confirm_multiple(self, pages):
        """Confirm closing pages.

        Raise Default to abort.
        """
        dialog = MultiCloseDialog(self.application, pages)
        response = self.flash_dialog(dialog)
        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise Default

    def _confirm_page(self, page):
        """Confirm closing page.

        Raise Default to abort.
        """
        docs = self._need_confirmation(page)
        if len(docs) == 2:
            return self._confirm_multiple([page])
        if cons.DOCUMENT.MAIN in docs:
            return self._confirm_main(page)
        if cons.DOCUMENT.TRAN in docs:
            return self._confirm_translation(page)

    def _confirm_translation(self, page):
        """Confirm closing translation document.

        Raise Default to abort.
        """
        doc = cons.DOCUMENT.TRAN
        basename = page.get_translation_basename()
        response = self._show_close_warning_dialog(doc, basename)
        if response == gtk.RESPONSE_YES:
            self.save_translation(page)
        elif response != gtk.RESPONSE_NO:
            raise Default

    def _need_confirmation(self, page):
        """Return the documents in page that require confirmation."""

        docs = []
        if page.project.main_changed:
            docs.append(cons.DOCUMENT.MAIN)
        elif page.project.main_file is not None:
            if not os.path.isfile(page.project.main_file.path):
                docs.append(cons.DOCUMENT.MAIN)
        if page.project.tran_active and page.project.tran_changed:
            docs.append(cons.DOCUMENT.TRAN)
        elif page.project.tran_file is not None:
            if not os.path.isfile(page.project.tran_file.path):
                docs.append(cons.DOCUMENT.TRAN)
        return docs

    def _save_window_geometry(self):
        """Save the geometry of main and output windows."""

        if not conf.application_window.maximized:
            domain = conf.application_window
            domain.size = self.window.get_size()
            domain.position = self.window.get_position()
        if not conf.output_window.maximized:
            domain = conf.output_window
            domain.size = self.output_window.get_size()
            domain.position = self.output_window.get_position()

    def _show_close_warning_dialog(self, doc, basename):
        """Show a warning dialog when trying to close a project.

        Return response.
        """
        if doc == cons.DOCUMENT.MAIN:
            title = _('Save changes to main document "%s" before closing?') \
                % basename
        elif doc == cons.DOCUMENT.TRAN:
            title = _('Save changes to translation document "%s" before '
                'closing?') % basename
        message = _("If you don't save, changes will be permanently lost.")
        dialog = WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        return self.flash_dialog(dialog)

    def close(self, page, confirm=True):
        """Close page (without confirmation)."""

        if confirm:
            self._confirm_page(page)
        index = self.pages.index(page)
        if self.notebook.get_current_page() == index:
            self.notebook.next_page()
        self.notebook.remove_page(index)
        self.pages.remove(page)
        self.emit("page-closed", page)

    @util.ignore_exceptions(Default)
    def on_close_all_projects_activate(self, *args):
        """Close all open projects."""

        self._close_all_pages()

    @util.ignore_exceptions(Default)
    def on_close_project_activate(self, *args):
        """Close project."""

        self.close(self.get_current_page())

    @util.ignore_exceptions(Default)
    def on_page_close_request(self, page, *args):
        """Close project."""

        self.close(page)

    @util.ignore_exceptions(Default)
    def on_quit_activate(self, *args):
        """Quit Gaupol."""

        self._close_all_pages()
        self._save_window_geometry()
        try:
            gtk.main_quit()
        except RuntimeError:
            raise SystemExit(1)

    def on_window_delete_event(self, *args):
        """Quit Gaupol."""

        self.on_quit_activate()
        return True
