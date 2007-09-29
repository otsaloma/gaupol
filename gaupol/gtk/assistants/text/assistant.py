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
import gobject
import gtk
_ = gaupol.i18n._
ngettext = gaupol.i18n.ngettext

from .capitalization import CapitalizationPage
from .confirmation import ConfirmationPage
from .error import CommonErrorPage
from .hearing import HearingImpairedPage
from .introduction import IntroductionPage
from .line import LineBreakPage
from .line import LineBreakOptionsPage
from .progress import ProgressPage


class TextAssistant(gtk.Assistant):

    """Assistant to guide through multiple text correction tasks."""

    def __init__(self, parent, application):

        gtk.Assistant.__init__(self)
        self._confirmation_page = ConfirmationPage()
        self._introduction_page = IntroductionPage()
        self._previous_page = None
        self._progress_page = ProgressPage()
        self.application = application

        self._init_properties()
        self._init_size()
        self._init_signal_handlers()
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_transient_for(parent)

    def _correct_texts(self, assistant_pages):
        """Correct texts by all pages and present changes."""

        changes = []
        @gaupol.gtk.util.asserted_return
        def register_changes(page, index, old_text, new_text):
            assert old_text != new_text
            changes.append((page, index, old_text, new_text))
        target = self._introduction_page.get_target()
        col = self._introduction_page.get_column()
        doc = gaupol.gtk.util.text_column_to_document(col)
        rows = self.application.get_target_rows(target)
        application_pages = self.application.get_target_pages(target)
        total = len(application_pages) * len(assistant_pages)
        self._progress_page.reset(total)
        for application_page in application_pages:
            name = application_page.get_main_basename()
            self._progress_page.set_project_name(name)
            project = application_page.project
            dummy = self._get_project_copy(project)
            static_subtitles = dummy.subtitles[:]
            for page in assistant_pages:
                self._progress_page.set_task_name(page.title)
                page.correct_texts(dummy, rows, doc)
                self._progress_page.bump_progress()
            for i in range(len(static_subtitles)):
                old = project.subtitles[i].get_text(doc)
                new = static_subtitles[i].get_text(doc)
                register_changes(application_page, i, old, new)
        self._prepare_confirmation_page(doc, changes)
        index = self.get_current_page()
        self.set_current_page(index + 1)
        return False

    def _get_project_copy(self, project):
        """Get a copy of project with some same properties."""

        copy = gaupol.Project(project.framerate)
        copy.main_file = project.main_file
        copy.subtitles = [x.copy() for x in project.subtitles]
        copy.tran_file = project.tran_file
        return copy

    def _init_properties(self):
        """Initialize assistant properties."""

        self.set_border_width(12)
        self.set_title(_("Correct Texts"))
        self.add_page(self._introduction_page)
        self.add_page(HearingImpairedPage())
        self.add_page(CommonErrorPage())
        self.add_page(CapitalizationPage())
        self.application.emit("text-assistant-request-pages", self)
        self.add_pages((LineBreakPage(), LineBreakOptionsPage()))
        self.add_page(self._progress_page)
        self.add_page(self._confirmation_page)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, self, "apply")
        gaupol.gtk.util.connect(self, self, "cancel")
        gaupol.gtk.util.connect(self, self, "close")
        gaupol.gtk.util.connect(self, self, "prepare")

    def _init_size(self):
        """Initialize the window size."""

        label = gtk.Label("\n".join(["M" * 64] * 30))
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        gaupol.gtk.util.resize_dialog(self, width, height, 0.8)

    def _on_apply(self, *args):
        """Apply all confirmed changes."""

        gaupol.gtk.util.set_cursor_busy(self)
        edits = removals = 0
        changes = self._confirmation_page.get_confirmed_changes()
        target = self._introduction_page.get_target()
        application_pages = self.application.get_target_pages(target)
        col = self._introduction_page.get_column()
        doc = gaupol.gtk.util.text_column_to_document(col)
        description = _("Correcting texts")
        register = gaupol.gtk.REGISTER.DO
        for page in application_pages:
            indexes = [x[1] for x in changes if x[0] is page]
            texts = [x[3] for x in changes if x[0] is page]
            if indexes and texts:
                page.project.replace_texts(indexes, doc, texts)
                page.project.set_action_description(register, description)
                edits += (len(indexes))
            edit_indexes = set(indexes)
            indexes = [x for i, x in enumerate(indexes) if not texts[i]]
            if indexes and gaupol.gtk.conf.text_assistant.remove_blank:
                page.project.remove_subtitles(indexes)
                page.project.group_actions(register, 2, description)
                removals += len(set(indexes))
        edits = edits - removals
        message = _("Edited %(edits)d and removed %(removals)d subtitles")
        self.application.flash_message(message % locals())
        gaupol.gtk.util.set_cursor_normal(self)

    def _on_cancel(self, *args):
        """Destroy the assistant."""

        self.destroy()

    def _on_close(self, *args):
        """Destroy the assistant."""

        self.destroy()

    def _on_prepare(self, assistant, page):
        """Prepare the page to be shown next."""

        previous_page = self._previous_page
        self._previous_page = page
        if page is self._introduction_page:
            return self._prepare_introduction_page()
        pages = self._introduction_page.get_selected_pages()
        if page is self._progress_page:
            if previous_page is not self._confirmation_page:
                return self._prepare_progress_page(pages)

    def _prepare_confirmation_page(self, doc, changes):
        """Present changes and activate the confirmation page."""

        count = len(changes)
        title = ngettext("Confirm %d Change", "Confirm %d Changes", count)
        self.set_page_title(self._confirmation_page, title % count)
        self._confirmation_page.application = self.application
        self._confirmation_page.doc = doc
        self._confirmation_page.populate_tree_view(changes)
        self.set_page_complete(self._progress_page, True)

    def _prepare_introduction_page(self):
        """Prepare the introduction page content."""

        count = self.get_n_pages()
        pages = [self.get_nth_page(x) for x in range(count)]
        pages.remove(self._introduction_page)
        pages.remove(self._progress_page)
        pages.remove(self._confirmation_page)
        pages = [x for x in pages if hasattr(x, "correct_texts")]
        self._introduction_page.populate_tree_view(pages)

    def _prepare_progress_page(self, pages):
        """Prepare to show the progress page."""

        self._progress_page.reset(0, True)
        self.set_page_complete(self._progress_page, False)
        gobject.timeout_add(10, self._correct_texts, pages)

    @gaupol.gtk.util.asserted_return
    def add_page(self, page):
        """Add page and configure its properties."""

        page.show_all()
        self.append_page(page)
        self.set_page_type(page, page.page_type)
        self.set_page_title(page, page.page_title)
        assert page.page_type != gtk.ASSISTANT_PAGE_PROGRESS
        self.set_page_complete(page, True)

    def add_pages(self, pages):
        """Add associated pages and configure their properties.

        The first one of the pages must have a 'correct_texts' attribute.
        The visibilities of other pages are synced with the first page.
        """
        for page in pages:
            self.add_page(page)
        def on_notify_visible(*args):
            for page in pages[1:]:
                page.props.visible = pages[0].props.visible
        pages[0].connect("notify::visible", on_notify_visible)
