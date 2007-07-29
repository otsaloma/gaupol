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

"""Assistants to guide through complicated tasks."""

import gaupol.gtk
import gobject
import gtk
import pango
_ = gaupol.i18n._

__all__ = ["TextAssistantPage", "TextAssistant"]


class TextAssistantPage(gtk.VBox):

    """One task and one page in the text correction assisstant.

    Instence variables:
     * description: One-line description used in the introduction page listing
     * page_title: Short string used as the configuration page title
     * page_type: A GTK assistant page type constant
     * title: Short string used in the introduction page listing
    """

    def __init__(self):

        gtk.VBox.__init__(self)
        self.description = None
        self.page_title = None
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = None
        self.set_border_width(12)


class ConfirmationPage(TextAssistantPage):

    """Page to confirm changes made after performing all tasks."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.page_type = gtk.ASSISTANT_PAGE_CONFIRM
        self.page_title = _("Confirm Changes")

        name = "text-assistant-confirmation-page"
        glade_xml = gaupol.gtk.util.get_glade_xml(name)
        self._tree_view = glade_xml.get_widget("tree_view")
        glade_xml.get_widget("vbox").reparent(self)
        self.show_all()


class HearingImpairedPage(TextAssistantPage):

    """Task and page for removing hearing impaired parts from subtitles."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.description = _("Remove explanatory texts meant "
            "for the hearing impaired")
        self.title = _("Remove hearing impaired texts")
        self.page_title = _("Define Hearing Impaired Patterns")

        name = "text-assistant-hearing-impaired-page"
        glade_xml = gaupol.gtk.util.get_glade_xml(name)
        self._country_combo = glade_xml.get_widget("country_combo")
        self._language_combo = glade_xml.get_widget("language_combo")
        self._script_combo = glade_xml.get_widget("script_combo")
        self._tree_view = glade_xml.get_widget("tree_view")
        glade_xml.get_widget("vbox").reparent(self)
        self.show_all()


class IntroductionPage(TextAssistantPage):

    """Page for listing all text correction tasks."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.page_type = gtk.ASSISTANT_PAGE_INTRO
        self.page_title = _("Select Tasks and Target")

        name = "text-assistant-introduction-page"
        glade_xml = gaupol.gtk.util.get_glade_xml(name)
        self._all_radio = glade_xml.get_widget("all_radio")
        self._current_radio = glade_xml.get_widget("current_radio")
        self._main_radio = glade_xml.get_widget("main_radio")
        self._selected_radio = glade_xml.get_widget("selected_radio")
        self._tran_radio = glade_xml.get_widget("tran_radio")
        self._tree_view = glade_xml.get_widget("tree_view")
        glade_xml.get_widget("vbox").reparent(self)

        self._init_tree_view()
        self.show_all()

    def _init_tree_view(self):
        """Initialize the tree view."""

        cols = (object, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        store = gtk.ListStore(*cols)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback, store)
        column = gtk.TreeViewColumn("", renderer, active=1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        column = gtk.TreeViewColumn("", renderer, markup=2)
        self._tree_view.append_column(column)

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle the check button value."""

        store[row][1] = not store[row][1]

    def populate_tree_view(self, pages):
        """Populate the tree view with a list of tasks defined by pages."""

        store = self._tree_view.get_model()
        for page in pages:
            markup = "<b>%s</b>\n%s" % (page.title, page.description)
            store.append([page, True, markup])


class TextAssistant(gtk.Assistant):

    """Assistant to guide through multiple text correction tasks."""

    def __init__(self, parent, application):

        gtk.Assistant.__init__(self)
        self.application = application

        self.set_border_width(12)
        self.set_title(_("Correct Texts"))
        self.add_page(IntroductionPage())
        self.add_page(HearingImpairedPage())
        self.application.emit("text-assistant-request-pages", self)
        self.add_page(ConfirmationPage())

        count = self.get_n_pages()
        pages = [self.get_nth_page(x) for x in range(1, count - 1)]
        self.get_nth_page(0).populate_tree_view(pages)

        self._init_size()
        self.set_transient_for(parent)

    def _init_size(self):
        """Initialize the window size."""

        label = gtk.Label("\n".join(["M" * 66] * 32))
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        gaupol.gtk.util.resize_dialog(self, width, height, 0.8)

    def add_page(self, page):
        """Add page and configure its properties."""

        self.append_page(page)
        self.set_page_type(page, page.page_type)
        self.set_page_title(page, page.page_title)
        self.set_page_complete(page, True)
