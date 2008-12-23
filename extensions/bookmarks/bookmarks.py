# Copyright (C) 2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Marking subtitles for easy navigation."""

import gaupol.gtk
import gtk
import os
_ = gaupol.i18n._


class BookmarksExtension(gaupol.gtk.Extension):

    """Marking subtitles for easy navigation."""

    _directory = os.path.dirname(__file__)
    _spec_file = os.path.join(_directory, "bookmarks.conf.spec")

    def __init__(self):
        """Initialize a BookmarksExtension object."""

        self._action_group = None
        self._conf = None
        self._uim_id = None
        self.application = None

    def _on_add_bookmark_activate(self, *args):
        """Add a bookmark for the current subtitle."""

        pass

    def _on_edit_bookmarks_activate(self, *args):
        """Show the bookmarks side pane."""

        pass

    def _on_next_bookmark_activate(self, *args):
        """Go to the next bookmarked subtitle."""

        pass

    def _on_previous_bookmark_activate(self, *args):
        """Go to the previous bookmarked subtitle."""

        pass

    def _on_toggle_bookmark_column_toggled(self, action, *args):
        """Show or hide the bookmark column."""

        self._conf.show_column = action.get_active()

    def setup(self, application):
        """Setup extension for use with application."""

        self.application = application
        self._conf = gaupol.gtk.conf.extensions.bookmarks
        self._action_group = gtk.ActionGroup(self.__class__.__name__)
        self._action_group.add_actions((
            ("show_bookmarks_menu", None, "_Bookmarks"),
            ("add_bookmark", gtk.STOCK_ADD, "_Add\342\200\246", "<Control>D",
             "Add a bookmark for the current subtitle",
             self._on_add_bookmark_activate),
            ("edit_bookmarks", None, "_Edit Bookmarks", "<Control>B",
             "Show the bookmarks side pane",
             self._on_edit_bookmarks_activate),
            ("next_bookmark", None, "_Next", None,
             "Go to the next bookmarked subtitle",
             self._on_next_bookmark_activate),
            ("previous_bookmark", None, "_Previous", None,
             "Go to the previous bookmarked subtitle",
             self._on_previous_bookmark_activate),))
        self._action_group.add_toggle_actions((
            ("toggle_bookmark_column", None, "_Bookmark", None,
             _("Show or hide the bookmark column"),
             self._on_toggle_bookmark_column_toggled,
             self._conf.show_column),))
        application.uim.insert_action_group(self._action_group, -1)
        ui_file = os.path.join(self._directory, "bookmarks.ui.xml")
        self._uim_id = application.uim.add_ui_from_file(ui_file)

    def teardown(self, application):
        """End use of extension with application."""

        self.application.uim.remove_ui(self._uim_id)
        self.application.uim.remove_action_group(self._action_group)
        self.application.uim.ensure_update()

    def update(self, application, page):
        """Update state of extension for application and active page."""

        pass
