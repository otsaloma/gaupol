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


"""Closing projects and quitting Gaupol."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.constants              import Document
from gaupol.gtk.delegates          import Delegate, UIMAction
from gaupol.gtk.dialogs.message    import WarningDialog
from gaupol.gtk.dialogs.multiclose import MultiCloseWarningDialog
from gaupol.gtk.error              import Cancelled
from gaupol.gtk.util               import config, gtklib


class CloseAllProjectsAction(UIMAction):

    """Closing all projects."""

    uim_action_item = (
        'close_all_projects',
        gtk.STOCK_CLOSE,
        _('_Close All'),
        '<shift><control>W',
        _('Close all open projects'),
        'on_close_all_projects_activated'
    )

    uim_paths = ['/ui/menubar/projects/close_all']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class CloseProjectAction(UIMAction):

    """Closing a project."""

    uim_action_item = (
        'close_project',
        gtk.STOCK_CLOSE,
        _('_Close'),
        '<control>W',
        _('Close the current project'),
        'on_close_project_activated'
    )

    uim_paths = ['/ui/menubar/file/close']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class QuitAction(UIMAction):

    """Quitting Gaupol."""

    uim_action_item = (
        'quit',
        gtk.STOCK_QUIT,
        _('_Quit'),
        '<control>Q',
        _('Quit Gaupol'),
        'on_quit_activated'
    )

    uim_paths = ['/ui/menubar/file/quit']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class CloseWarningDialog(WarningDialog):

    """Dialog for warning when closing a document."""

    def __init__(self, parent, document, basename):

        if document == Document.MAIN:
            title = _('Save changes to main document "%s" before closing?') \
                    % basename
        elif document == Document.TRAN:
            title = _('Save changes to translation document "%s" before '
                      'closing?') % basename

        message = _('If you don\'t save, changes will be permanently lost.')

        WarningDialog.__init__(self, parent, title, message)

        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL          , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE            , gtk.RESPONSE_YES   )
        self.set_default_response(gtk.RESPONSE_YES)


class FileCloseDelegate(Delegate):

    """Closing projects and quitting Gaupol."""

    def _close_all_pages(self):
        """
        Close all pages.

        Raise Cancelled if cancelled.
        """
        unsaved_count = 0

        # Get amount of unsaved documents.
        for page in self.pages:

            if page.project.main_changed:
                unsaved_page = page
                unsaved_count += 1
            if page.project.tran_changed and page.project.tran_active:
                unsaved_page = page
                unsaved_count += 1

            if unsaved_count > 1:
                break

        if unsaved_count == 1:
            self._confirm_closing_page(unsaved_page)
        elif unsaved_count > 1:
            self._confirm_closing_multiple_documents(self.pages)

        for i in reversed(range(len(self.pages))):
            page = self.pages.pop(i)
            gtklib.destroy_gobject(page)

        while self.notebook.get_current_page() > -1:
            self.notebook.remove_page(0)

    def _close_page(self, page):
        """
        Close page.

        Raise Cancelled if cancelled.
        """
        self._confirm_closing_page(page)

        # The notebook widget does not seem to be able to handle post
        # page-close page-switching smoothly. So, as a workaround, we'll switch
        # to the next page if we're closing the current page.
        current_page_index = self.notebook.get_current_page()
        this_page_index    = self.pages.index(page)

        if current_page_index == this_page_index:
            self.notebook.next_page()

        self.pages.remove(page)
        gtklib.destroy_gobject(page)
        self.notebook.remove_page(this_page_index)

    def _confirm_closing_main_document(self, page):
        """
        Confirm closing main document.

        Raise Cancelled is cancelled.
        """
        basename = page.get_main_basename()
        dialog = CloseWarningDialog(self.window, Document.MAIN, basename)
        response = dialog.run()
        dialog.destroy()

        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise Cancelled

        # Save document.
        if response == gtk.RESPONSE_YES:
            success = self.save_main_document(page)
            if not success:
                raise Cancelled

    def _confirm_closing_multiple_documents(self, pages):
        """
        Confirm closing all documents of pages.

        Raise Cancelled if cancelled.
        """
        dialog = MultiCloseWarningDialog(self.window, pages)
        response = dialog.run()

        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            dialog.destroy()
            raise Cancelled
        if response == gtk.RESPONSE_NO:
            dialog.destroy()
            return

        # Save documents.
        main_pages = dialog.get_main_pages_to_save()
        tran_pages = dialog.get_translation_pages_to_save()
        dialog.destroy()

        gtklib.set_cursor_busy(self.window)

        for page in main_pages:
            success = self.save_main_document(page)
            if not success:
                raise Cancelled
        for page in tran_pages:
            success = self.save_translation_document(page)
            if not success:
                raise Cancelled

        gtklib.set_cursor_normal(self.window)

    def _confirm_closing_page(self, page):
        """
        Confirm closing page.

        Raise Cancelled if cancelled.
        """
        confirm_main = page.project.main_changed
        confirm_tran = page.project.tran_changed and page.project.tran_active

        if confirm_main and not confirm_tran:
            self._confirm_closing_main_document(page)
        elif not confirm_main and confirm_tran:
            self._confirm_closing_translation_document(page)
        elif confirm_main and confirm_tran:
            self._confirm_closing_multiple_documents([page])

    def _confirm_closing_translation_document(self, page):
        """
        Confirm closing translation document.

        Raise Cancelled is cancelled.
        """
        basename = page.get_translation_basename()
        dialog = CloseWarningDialog(self.window, Document.TRAN, basename)
        response = dialog.run()
        dialog.destroy()

        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise Cancelled

        # Save document.
        if response == gtk.RESPONSE_YES:
            success = self.save_translation_document(page)
            if not success:
                raise Cancelled

    def on_close_all_projects_activated(self, *args):
        """Close all pages."""

        try:
            self._close_all_pages()
            self.set_sensitivities()
        except Cancelled:
            return

    def on_close_button_clicked(self, page):
        """Close page."""

        try:
            self._close_page(page)
            self.set_sensitivities()
        except Cancelled:
            return

    def on_close_project_activated(self, *args):
        """Close the current page."""

        page = self.get_current_page()

        try:
            self._close_page(page)
            self.set_sensitivities()
        except Cancelled:
            return

    def on_quit_activated(self, *args):
        """Quit Gaupol."""

        try:
            self._close_all_pages()
        except Cancelled:
            return

        # Save window geometry.
        if not config.application_window.maximized:
            config.application_window.size     = self.window.get_size()
            config.application_window.position = self.window.get_position()

        config.write()

        try:
            gtk.main_quit()
        except RuntimeError:
            raise SystemExit(1)

    def on_window_delete_event(self, *args):
        """Quit Gaupol."""

        self.on_quit_activated()

        # Return True to stop other handlers.
        return True
