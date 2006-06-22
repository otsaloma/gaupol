# Copyright (C) 2005-2006 Osmo Salomaa
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


from gettext import gettext as _

import gtk

from gaupol.gtk.colcons           import *
from gaupol.gtk.delegate          import Delegate, UIMAction
from gaupol.gtk.dialog.message    import WarningDialog
from gaupol.gtk.dialog.multiclose import MultiCloseWarningDialog
from gaupol.gtk.error             import Default
from gaupol.gtk.util              import config, gtklib


class CloseAllProjectsAction(UIMAction):

    """Closing all projects."""

    action_item = (
        'close_all_projects',
        gtk.STOCK_CLOSE,
        _('_Close All'),
        '<shift><control>W',
        _('Close all open projects'),
        'on_close_all_projects_activate'
    )

    paths = ['/ui/menubar/projects/close_all']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class CloseProjectAction(UIMAction):

    """Closing a project."""

    action_item = (
        'close_project',
        gtk.STOCK_CLOSE,
        _('_Close'),
        '<control>W',
        _('Close the current project'),
        'on_close_project_activate'
    )

    paths = ['/ui/menubar/file/close']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class QuitAction(UIMAction):

    """Quitting Gaupol."""

    action_item = (
        'quit',
        gtk.STOCK_QUIT,
        _('_Quit'),
        '<control>Q',
        _('Quit Gaupol'),
        'on_quit_activate'
    )

    paths = ['/ui/menubar/file/quit']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class _CloseWarningDialog(WarningDialog):

    """Dialog for warning when closing a document."""

    def __init__(self, parent, doc, basename):

        if doc == MAIN:
            title = _('Save changes to main document "%s" before closing?') \
                    % basename
        elif doc == TRAN:
            title = _('Save changes to translation document "%s" before '
                      'closing?') % basename
        message = _('If you don\'t save, changes will be permanently lost.')
        WarningDialog.__init__(self, parent, title, message)
        self.add_button(_('Close _Without Saving'), gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_YES)


class FileCloseDelegate(Delegate):

    """Closing projects and quitting Gaupol."""

    def _close_all_pages(self):
        """
        Close all pages.

        Raise Default if cancelled.
        """
        unsaved_count = 0
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
            self._confirm_page(unsaved_page)
        elif unsaved_count > 1:
            self._confirm_multiple(self.pages)

        for i in reversed(range(len(self.pages))):
            page = self.pages.pop(i)
            gtklib.destroy_gobject(page)
        while self._notebook.get_current_page() > -1:
            self._notebook.remove_page(0)

    def _close_page(self, page):
        """
        Close page.

        Raise Default if cancelled.
        """
        self._confirm_page(page)
        current_index = self._notebook.get_current_page()
        close_index = self.pages.index(page)
        if current_index == close_index:
            self._notebook.next_page()

        self.pages.remove(page)
        gtklib.destroy_gobject(page)
        self._notebook.remove_page(close_index)

    def _confirm_main(self, page):
        """
        Confirm closing main document.

        Raise Default if cancelled.
        """
        basename = page.get_main_basename()
        dialog = _CloseWarningDialog(self._window, MAIN, basename)
        response = dialog.run()
        dialog.destroy()
        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise Default
        if response == gtk.RESPONSE_YES:
            self.save_main(page)

    def _confirm_multiple(self, pages):
        """
        Confirm closing all documents of pages.

        Raise Default if cancelled.
        """
        dialog = MultiCloseWarningDialog(self._window, pages)
        response = dialog.run()
        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            dialog.destroy()
            raise Default
        if response == gtk.RESPONSE_NO:
            dialog.destroy()
            return

        main_pages = dialog.get_main_pages()
        tran_pages = dialog.get_translation_pages()
        dialog.destroy()
        gtklib.set_cursor_busy(self._window)
        for page in main_pages:
            self.save_main(page)
        for page in tran_pages:
            self.save_translation(page)
        gtklib.set_cursor_normal(self._window)

    def _confirm_page(self, page):
        """
        Confirm closing page.

        Raise Default if cancelled.
        """
        confirm_main = page.project.main_changed
        confirm_tran = page.project.tran_changed and page.project.tran_active
        if confirm_main and not confirm_tran:
            self._confirm_main(page)
        elif not confirm_main and confirm_tran:
            self._confirm_translation(page)
        elif confirm_main and confirm_tran:
            self._confirm_multiple([page])

    def _confirm_translation(self, page):
        """
        Confirm closing translation document.

        Raise Default is cancelled.
        """
        basename = page.get_translation_basename()
        dialog = _CloseWarningDialog(self._window, TRAN, basename)
        response = dialog.run()
        dialog.destroy()
        if response not in (gtk.RESPONSE_YES, gtk.RESPONSE_NO):
            raise Default
        if response == gtk.RESPONSE_YES:
            self.save_translation(page)

    def on_close_all_projects_activate(self, *args):
        """Close all pages."""

        try:
            self._close_all_pages()
            self.set_sensitivities()
        except Default:
            return

    def on_close_project_activate(self, *args):
        """Close the current page."""

        page = self.get_current_page()
        try:
            self._close_page(page)
            self.set_sensitivities()
        except Default:
            return

    def on_page_closed(self, page):
        """Close page."""

        try:
            self._close_page(page)
            self.set_sensitivities()
        except Default:
            return

    def on_quit_activate(self, *args):
        """Quit Gaupol."""

        try:
            self._close_all_pages()
        except Default:
            return

        if not config.application_window.maximized:
            domain = config.application_window
            domain.size = list(self._window.get_size())
            domain.position = list(self._window.get_position())
        if not config.output_window.maximized:
            domain = config.output_window
            domain.size = list(self._output_window.get_size())
            domain.position = list(self._output_window.get_position())

        config.write()

        try:
            gtk.main_quit()
        except RuntimeError:
            raise SystemExit(1)

    def on_window_delete_event(self, *args):
        """Quit Gaupol."""

        self.on_quit_activate()
        return True
