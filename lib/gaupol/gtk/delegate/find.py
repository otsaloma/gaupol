# Copyright (C) 2006 Osmo Salomaa
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


"""Finding and replacing text."""


from gettext import gettext as _

import gtk

from gaupol.gtk             import cons
from gaupol.gtk.delegate    import Delegate, UIMAction
from gaupol.gtk.dialog.find import FindDialog, ReplaceDialog
from gaupol.gtk.util        import conf, gtklib


class FindAction(UIMAction):

    """Finding text."""

    action_item = (
        'find',
        gtk.STOCK_FIND,
        _('_Find...'),
        '<control>F',
        _('Search for text'),
        'on_find_activate'
    )

    paths = ['/ui/menubar/search/find']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class FindNextAction(UIMAction):

    """Finding next match."""

    action_item = (
        'find_next',
        None,
        _('Find _Next'),
        '<control>G',
        _('Search forwards for same text'),
        'on_find_next_activate'
    )

    paths = ['/ui/menubar/search/next']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return bool(conf.find.pattern)


class FindPreviousAction(UIMAction):

    """Finding previous match."""

    action_item = (
        'find_previous',
        None,
        _('Find _Previous'),
        '<shift><control>G',
        _('Search backwards for same text'),
        'on_find_previous_activate'
    )

    paths = ['/ui/menubar/search/previous']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return bool(conf.find.pattern)


class ReplaceAction(UIMAction):

    """Replacing text."""

    action_item = (
        'replace',
        gtk.STOCK_FIND_AND_REPLACE,
        _('_Replace...'),
        '<control>H',
        _('Search for and replace text'),
        'on_replace_activate'
    )

    paths = ['/ui/menubar/search/replace']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class FindDelegate(Delegate):

    """Finding and replacing text."""

    def __init__(self, *args, **kwargs):

        Delegate.__init__(self, *args, **kwargs)

        self._dialog = None

    def _connect_signals(self):
        """Connect page signals."""

        gtklib.connect(self, '_dialog', 'coordinate-request')
        gtklib.connect(self, '_dialog', 'destroyed'         )
        gtklib.connect(self, '_dialog', 'message'           )
        gtklib.connect(self, '_dialog', 'next-page'         )
        gtklib.connect(self, '_dialog', 'previous-page'     )
        gtklib.connect(self, '_dialog', 'update'            )

    def _on_dialog_coordinate_request(self, dialog):
        """Return page, row, document."""

        page = self.get_current_page()
        if page is None:
            return None, None, None

        try:
            row = page.view.get_selected_rows()[0]
        except IndexError:
            row = None
        col = page.view.get_focus()[1]
        if col is not None:
            doc = page.text_column_to_document(col)
        else:
            doc = None

        return page, row, doc

    def _on_dialog_destroyed(self, dialog):
        """Destroy dialog."""

        gtklib.destroy_gobject(dialog)
        self._dialog = None

    def _on_dialog_message(self, dialog, message):
        """Set message to statusbar."""

        self.set_status_message(message)

    def _on_dialog_next_page(self, dialog):
        """Activate next page."""

        index = self.pages.index(self.get_current_page())
        try:
            index += 1
            page = self.pages[index]
        except IndexError:
            index = 0
            page = self.pages[index]

        self._notebook.set_current_page(index)
        page.view.select_rows([])
        page.view.set_focus(0, None)

        if conf.find.target == cons.Target.CURRENT:
            self.set_status_message(_('Wrapped search'))
        elif conf.find.target == cons.Target.ALL and index == 0:
            self.set_status_message(_('Wrapped search'))

    def _on_dialog_previous_page(self, dialog):
        """Activate previous page."""

        index = self.pages.index(self.get_current_page())
        index = index - 1
        page = self.pages[index]
        index = self.pages.index(page)

        self._notebook.set_current_page(index)
        page.view.select_rows([])
        page.view.set_focus(len(page.project.times) - 1, None)

        max_index = len(self.pages) - 1
        if conf.find.target == cons.Target.CURRENT:
            self.set_status_message(_('Wrapped search'))
        elif conf.find.target == cons.Target.ALL and index == max_index:
            self.set_status_message(_('Wrapped search'))

    def _on_dialog_update(self, dialog):
        """Set sensitivities."""

        self.set_sensitivities()

    def on_find_activate(self, *args):
        """Find text."""

        if self._dialog is not None:
            if isinstance(self._dialog, ReplaceDialog):
                self._dialog.close()
            else:
                self._dialog.show()
                self._dialog.present()
                return

        self._dialog = FindDialog()
        self._connect_signals()
        self._dialog.show()

    def on_find_next_activate(self, *args):
        """Find next match."""

        if self._dialog is not None:
            if isinstance(self._dialog, ReplaceDialog):
                self._dialog.close()
            else:
                self._dialog.next()
                return

        self._dialog = FindDialog()
        self._connect_signals()
        self._dialog.next()

    def on_find_previous_activate(self, *args):
        """Find previous match."""

        if self._dialog is not None:
            if isinstance(self._dialog, ReplaceDialog):
                self._dialog.close()
            else:
                self._dialog.previous()
                return

        self._dialog = FindDialog()
        self._connect_signals()
        self._dialog.previous()

    def on_replace_activate(self, *args):
        """Replace text."""

        if self._dialog is not None:
            if not isinstance(self._dialog, ReplaceDialog):
                self._dialog.close()
            else:
                self._dialog.show()
                self._dialog.present()
                return

        self._dialog = ReplaceDialog()
        self._connect_signals()
        self._dialog.show()
