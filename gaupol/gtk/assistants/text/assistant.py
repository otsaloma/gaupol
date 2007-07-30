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

"""Assistant to guide through multiple text correction tasks."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .confirmation import ConfirmationPage
from .hearing import HearingImpairedPage
from .introduction import IntroductionPage


class TextAssistant(gtk.Assistant):

    """Assistant to guide through multiple text correction tasks."""

    def __init__(self, parent, application):

        gtk.Assistant.__init__(self)
        self._confirmation_page = ConfirmationPage()
        self._introduction_page = IntroductionPage()
        self.application = application

        self.set_border_width(12)
        self.set_title(_("Correct Texts"))
        self.add_page(self._introduction_page)
        self.add_page(HearingImpairedPage())
        self.application.emit("text-assistant-request-pages", self)
        self.add_page(self._confirmation_page)

        self._init_size()
        self._init_signal_handlers()
        self.set_transient_for(parent)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, self, "apply")
        gaupol.gtk.util.connect(self, self, "cancel")
        gaupol.gtk.util.connect(self, self, "prepare")

    def _init_size(self):
        """Initialize the window size."""

        label = gtk.Label("\n".join(["M" * 66] * 32))
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        gaupol.gtk.util.resize_dialog(self, width, height, 0.8)

    def _on_apply(self, assistant):
        """Apply all the changes that have been confirmed."""

        pass

    def _on_cancel(self, assistant):
        """Destroy the assistant."""

        pass

    def _on_prepare(self, assistant, page):
        """Prepare to show page."""

        if page is self._introduction_page:
            return self._prepare_introduction_page()
        pages = self._introduction_page.get_selected_pages()
        if page is self._confirmation_page:
            return # TODO: MAKE ALL CHANGES
        self._prepare_page_title(page, pages)

    def _prepare_introduction_page(self):
        """Prepare the introduction page content."""

        count = self.get_n_pages()
        pages = [self.get_nth_page(x) for x in range(count)]
        pages.remove(self._introduction_page)
        pages.remove(self._confirmation_page)
        self._introduction_page.populate_tree_view(pages)

    def _prepare_page_title(self, page, pages):
        """Prepare the page title to include current page number."""

        title = page.page_title
        current = pages.index(page) + 2
        total = len(pages) + 2
        new_title = _("%(title)s - (%(current)d of %(total)d)")
        self.set_page_title(page, new_title % locals())

    def add_page(self, page):
        """Add page and configure its properties."""

        self.append_page(page)
        self.set_page_type(page, page.page_type)
        self.set_page_title(page, page.page_title)
        self.set_page_complete(page, True)
