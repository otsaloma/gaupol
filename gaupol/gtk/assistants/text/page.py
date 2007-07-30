# Copyright (C) 2007 Osmo Salomaa
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

"""One task and one page in the text correction assistant."""

import gtk


class TextAssistantPage(gtk.VBox):

    """One task and one page in the text correction assistant.

    Instence variables:
     * description: One-line description used in the introduction page listing
     * handle: Unique unlocalized name for internal references
     * page_title: Short string used as the configuration page title
     * page_type: A GTK assistant page type constant
     * title: Short string used in the introduction page listing

    'description', 'handle' and 'title' are only required for content pages.
    """

    def __init__(self):

        gtk.VBox.__init__(self)
        self.description = None
        self.handle = None
        self.page_title = None
        self.page_type = None
        self.title = None

    def _init_properties(self):
        """Initialize the vertical box properties."""

        self.set_border_width(12)
        self.show_all()
