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

"""Page for showing progress of text corrections."""

from __future__ import division

import gaupol.gtk
import gobject
import gtk
_ = gaupol.i18n._

from .page import TextAssistantPage


class ProgressPage(TextAssistantPage):

    """Page for showing progress of text corrections."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self._current = None
        self._total = None
        self.page_title = _("Correcting Texts")
        self.page_type = gtk.ASSISTANT_PAGE_PROGRESS

        name = "text-assistant-progress-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._message_label = get_widget("message_label")
        self._progress_bar = get_widget("progress_bar")
        self._status_label = get_widget("status_label")
        self._task_label = get_widget("task_label")
        get_widget("vbox").reparent(self)
        self._init_values()

    def _init_values(self):
        """Initalize default values for widgets."""

        message = _("Each task is now being run on each project.")
        self._message_label.set_text(message)
        self.reset(100)

    def bump_progress(self, value=1):
        """Bump the current progress by value operations."""

        self.set_progress(self._current + value)

    def reset(self, total, blank_text=False):
        """Set the total amount of operations."""

        self.set_progress(0, total)
        self.set_project_name("")
        self.set_task_name("")
        if blank_text:
            self._progress_bar.set_text("")
        gaupol.gtk.util.iterate_main()

    def set_progress(self, current, total=None):
        """Set the current progress status."""

        total = total or self._total
        self._progress_bar.set_fraction(current / total)
        text = _("%(current)d of %(total)d operations complete")
        self._progress_bar.set_text(text % locals())
        self._current = current
        self._total = total
        gaupol.gtk.util.iterate_main()

    def set_project_name(self, name):
        """Set the name of the currently checked project."""

        text = _("Project: %s") % name
        text = gobject.markup_escape_text(text)
        self._status_label.set_markup("<i>%s</i>" % text)
        gaupol.gtk.util.iterate_main()

    def set_task_name(self, name):
        """Set the name of the currently performed task."""

        text = _("Task: %s") % name
        text = gobject.markup_escape_text(text)
        self._task_label.set_markup("<i>%s</i>" % text)
        gaupol.gtk.util.iterate_main()
