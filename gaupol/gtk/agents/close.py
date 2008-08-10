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

"""Closing projects and quitting Gaupol."""

import gaupol.gtk
import gtk
import os
_ = gaupol.i18n._


class CloseAgent(gaupol.Delegate):

    """Closing projects and quitting Gaupol."""

    # pylint: disable-msg=E0203,W0201

    def _close_all_pages(self):
        """Close all pages after seeking confirmation.

        Raise Default if cancelled and (all) pages were not closed.
        """
        if sum((len(self._need_confirmation(x)) for x in self.pages)) > 1:
            return self._confirm_and_close_pages(self.pages)
        while self.pages:
            self.close_page(self.pages[-1])

    def _confirm_and_close_page(self, page):
        """Close page after possibly saving its documents.

        Raise Default if cancelled and page was not closed.
        """
        docs = self._need_confirmation(page)
        if len(docs) == 2:
            return self._confirm_and_close_pages((page,))
        if gaupol.documents.MAIN in docs:
            return self._confirm_and_close_page_main(page)
        if gaupol.documents.TRAN in docs:
            return self._confirm_and_close_page_translation(page)
        self.close_page(page, False)

    def _confirm_and_close_pages(self, pages):
        """Close pages after possibly saving their documents.

        Raise Default if cancelled and (all) pages were not closed.
        """
        dialog = gaupol.gtk.MultiCloseDialog(self.window, self, pages)
        response = self.flash_dialog(dialog)
        if not response in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise gaupol.gtk.Default

    def _confirm_and_close_page_main(self, page):
        """Close page after possibly saving the main document.

        Raise Default if cancelled and page was not closed.
        """
        title = _('Save changes to main document "%s" before closing?')
        title = title % page.get_main_basename()
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.gtk.WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if not response in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise gaupol.gtk.Default
        if response == gtk.RESPONSE_YES:
            self.save_main_document(page)
        self.close_page(page, False)

    def _confirm_and_close_page_translation(self, page):
        """Close page after possibly saving the translation document.

        Raise Default if cancelled and page was not closed.
        """
        title = _('Save changes to translation document "%s" before closing?')
        title = title % page.get_translation_basename()
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.gtk.WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), gtk.RESPONSE_NO)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        dialog.set_default_response(gtk.RESPONSE_YES)
        response = self.flash_dialog(dialog)
        if not response in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise gaupol.gtk.Default
        if response == gtk.RESPONSE_YES:
            self.save_translation_document(page)
        self.close_page(page, False)

    def _need_confirmation(self, page):
        """Return the documents in page that require confirmation."""

        docs = []
        if page.project.main_changed:
            docs.append(gaupol.documents.MAIN)
        elif page.project.main_file is not None:
            if not os.path.isfile(page.project.main_file.path):
                docs.append(gaupol.documents.MAIN)
        if page.project.tran_changed:
            docs.append(gaupol.documents.TRAN)
        elif page.project.tran_file is not None:
            if not os.path.isfile(page.project.tran_file.path):
                docs.append(gaupol.documents.TRAN)
        return tuple(docs)

    def _save_window_geometry(self):
        """Save the geometry of the application and output windows."""

        if not gaupol.gtk.conf.application_window.maximized:
            conf = gaupol.gtk.conf.application_window
            conf.size = self.window.get_size()
            conf.position = self.window.get_position()
        if not gaupol.gtk.conf.output_window.maximized:
            conf = gaupol.gtk.conf.output_window
            conf.size = self.output_window.get_size()
            conf.position = self.output_window.get_position()

    def close_page(self, page, confirm=True):
        """Close page seeking confirmation if confirm is True.

        Raise Default if cancelled and page was not closed.
        """
        if confirm:
            return self._confirm_and_close_page(page)
        index = self.pages.index(page)
        if self.notebook.get_current_page() == index:
            self.notebook.next_page()
        self.notebook.remove_page(index)
        self.pages.remove(page)
        self.update_gui()
        self.emit("page-closed", page)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_close_all_projects_activate(self, *args):
        """Close all open projects."""

        self._close_all_pages()

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_close_project_activate(self, *args):
        """Close project."""

        self.close_page(self.get_current_page())

    @gaupol.deco.silent(gaupol.gtk.Default)
    def on_page_close_request(self, page, *args):
        """Close project."""

        self.close_page(page)

    @gaupol.deco.silent(gaupol.gtk.Default)
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

        self.get_action("quit").activate()
        return True
