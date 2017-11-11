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

"""Closing pages and quitting Gaupol."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gtk


class CloseAgent(aeidon.Delegate):

    """Closing pages and quitting Gaupol."""

    @aeidon.deco.export
    def close(self, page, confirm=True):
        """Close `page` after asking to save its documents."""
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
        """Close all pages after asking to save their documents."""
        if confirm and sum(len(self._need_confirmation(
                x)) for x in self.pages) > 1:
            return self._confirm_close_multiple(tuple(self.pages))
        while self.pages:
            self.close(self.pages[-1], confirm=confirm)

    def _confirm_close(self, page):
        """Close `page` after asking to save its documents."""
        docs = self._need_confirmation(page)
        if len(docs) == 0: return
        if len(docs) == 1:
            self._confirm_close_document(page, docs[0])
        if len(docs) > 1:
            self._confirm_close_multiple((page,))

    def _confirm_close_document(self, page, doc):
        """Close `page` after asking to save `doc`."""
        title = _('Save changes to document "{}" before closing?')
        title = title.format(page.get_basename(doc))
        message = _("If you don't save, changes will be permanently lost.")
        dialog = gaupol.WarningDialog(self.window, title, message)
        dialog.add_button(_("Close _Without Saving"), Gtk.ResponseType.NO)
        dialog.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        dialog.add_button(_("_Save"), Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(not response in (
            Gtk.ResponseType.YES, Gtk.ResponseType.NO))
        if response == Gtk.ResponseType.YES:
            self.save(page, doc)

    def _confirm_close_multiple(self, pages):
        """Close `pages` after asking to save their documents."""
        dialog = gaupol.MultiCloseDialog(self.window, self, pages)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(not response in (
            Gtk.ResponseType.YES, Gtk.ResponseType.NO))

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
    def _on_window_delete_event(self, *args):
        """Quit Gaupol."""
        try:
            self.quit()
        except gaupol.Default:
            pass
        # Let appman destroy the window if confirmation given
        # and once any events being processed have completed.
        # https://github.com/otsaloma/gaupol/issues/54
        return True

    @aeidon.deco.export
    def quit(self, confirm=True):
        """Quit Gaupol."""
        self.emit("quit")
        if confirm and sum(len(self._need_confirmation(
                x)) for x in self.pages) > 1:
            self._confirm_close_multiple(tuple(self.pages))
        elif confirm:
            for page in self.pages:
                if self._need_confirmation(page):
                    self._confirm_close(page)
        self.extension_manager.teardown_extensions()
        if not gaupol.conf.application_window.maximized:
            conf = gaupol.conf.application_window
            conf.size = list(self.window.get_size())
            conf.position = list(self.window.get_position())
        if hasattr(gaupol, "appman"):
            gaupol.appman.remove_window(self.window)
