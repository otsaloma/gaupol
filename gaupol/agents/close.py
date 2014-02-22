# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Closing pages and quitting Gaupol."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import Gtk


class CloseAgent(aeidon.Delegate):

    """Closing pages and quitting Gaupol."""

    def _confirm_close(self, page):
        """
        Close `page` after asking to save its documents.

        Raise :exc:`gaupol.Default` if cancelled and `page` not closed.
        """
        docs = self._need_confirmation(page)
        if len(docs) > 1:
            return self._confirm_close_multiple((page,))
        if aeidon.documents.MAIN in docs:
            return self._confirm_close_main(page)
        if aeidon.documents.TRAN in docs:
            return self._confirm_close_translation(page)

    def _confirm_close_main(self, page):
        """
        Close `page` after asking to save its main document.

        Raise :exc:`gaupol.Default` if cancelled and page not closed.
        """
        title = _('Save changes to main document "{}" before closing?')
        title = title.format(page.get_main_basename())
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        if not response in (Gtk.ResponseType.YES, Gtk.ResponseType.NO):
            raise gaupol.Default
        if response == Gtk.ResponseType.YES:
            self.save_main(page)

    def _confirm_close_multiple(self, pages):
        """
        Close `pages` after asking to save their documents.

        Raise :exc:`gaupol.Default` if cancelled and `pages` not closed.
        """
        dialog = gaupol.MultiCloseDialog(self.window, self, pages)
        response = gaupol.util.flash_dialog(dialog)
        if not response in (Gtk.ResponseType.YES, Gtk.ResponseType.NO):
            raise gaupol.Default

    def _confirm_close_translation(self, page):
        """
        Close `page` after asking to save its translation document.

        Raise :exc:`gaupol.Default` if cancelled and page not closed.
        """
        title = _('Save changes to translation document "{}" before closing?')
        title = title.format(page.get_translation_basename())
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), Gtk.ResponseType.NO)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        if not response in (Gtk.ResponseType.YES, Gtk.ResponseType.NO):
            raise gaupol.Default
        if response == Gtk.ResponseType.YES:
            self.save_translation(page)

    def _need_confirmation(self, page):
        """Return documents in `page` with unsaved changes."""
        docs = []
        if page.project.main_changed:
            docs.append(aeidon.documents.MAIN)
        elif page.project.main_file is not None:
            if not os.path.isfile(page.project.main_file.path):
                docs.append(aeidon.documents.MAIN)
        if page.project.tran_changed:
            docs.append(aeidon.documents.TRAN)
        elif page.project.tran_file is not None:
            if not os.path.isfile(page.project.tran_file.path):
                docs.append(aeidon.documents.TRAN)
        return tuple(docs)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_close_all_projects_activate(self, *args):
        """Close all open projects."""
        self.close_all()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_close_project_activate(self, *args):
        """Close project."""
        self.close(self.get_current_page())

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_page_close_request(self, page, *args):
        """Close project."""
        self.close(page)

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_quit_activate(self, *args):
        """Quit Gaupol."""
        self.quit()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_window_delete_event(self, *args):
        """Quit Gaupol."""
        self.quit()
        return True

    def _save_window_geometry(self):
        """Save the geometry of application and output windows."""
        if not gaupol.conf.application_window.maximized:
            conf = gaupol.conf.application_window
            conf.size = list(self.window.get_size())
            conf.position = list(self.window.get_position())
        if not gaupol.conf.output_window.maximized:
            conf = gaupol.conf.output_window
            conf.size = list(self.output_window.get_size())
            conf.position = list(self.output_window.get_position())

    @aeidon.deco.export
    def close(self, page, confirm=True):
        """
        Close `page` after asking to save its documents.

        If `confirm` is ``False`` do not ask to save documents.
        Raise :exc:`gaupol.Default` if asked to save, but cancelled
        and `page` was not closed.
        """
        if confirm:
            self._confirm_close(page)
        if not page in self.pages: return
        index = self.pages.index(page)
        if self.notebook.get_current_page() == index:
            self.notebook.next_page()
        self.notebook.remove_page(index)
        self.pages.remove(page)
        self.update_gui()
        self.emit("page-closed", page)

    @aeidon.deco.export
    def close_all(self, confirm=True):
        """
        Close all pages after asking to save their documents.

        If `confirm` is ``False`` do not ask to save documents.
        Raise :exc:`gaupol.Default` if asked to save, but cancelled
        and not all pages are closed.
        """
        nconfirm = sum((len(self._need_confirmation(x)) for x in self.pages))
        if confirm and nconfirm > 1:
            return self._confirm_close_multiple(tuple(self.pages))
        while self.pages:
            self.close(self.pages[-1], confirm=confirm)

    @aeidon.deco.export
    def quit(self, confirm=True):
        """
        Quit Gaupol.

        If `confirm` is ``False`` do not ask to save documents.
        Raise :exc:`gaupol.Default` if asked to save, but cancelled.
        """
        self.emit("quit")
        self.close_all(confirm=confirm)
        self.extension_manager.teardown_extensions()
        self._save_window_geometry()
        try:
            Gtk.main_quit()
        except RuntimeError:
            raise SystemExit(1)
