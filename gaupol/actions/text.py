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

"""Text formatting actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

class ClearTextsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "clear-texts")
        self.accelerators = ["C"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class CopyTextsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "copy-texts")
        self.accelerators = ["<Control>C"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class CutTextsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "cut-texts")
        self.accelerators = ["<Control>X"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class FindAndReplaceAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "find-and-replace")
        self.accelerators = ["<Control>F", "<Control>H"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class FindNextAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "find-next")
        self.accelerators = ["<Control>G"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pattern)

class FindPreviousAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "find-previous")
        self.accelerators = ["<Shift><Control>G"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pattern)

class PasteTextsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "paste-texts")
        self.accelerators = ["<Control>V"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class ToggleDialogDashesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "toggle-dialogue-dashes")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class ToggleItalicizationAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "toggle-italicization")
        self.accelerators = ["<Control>I"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))
        doc = page.text_column_to_document(col)
        markup = page.project.get_markup(doc)
        aeidon.util.affirm(markup is not None)
        aeidon.util.affirm(markup.italic_tag is not None)

class UseLowerCaseAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "use-lower-case")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class UseSentenceCaseAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "use-sentence-case")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class UseTitleCaseAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "use-title-case")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

class UseUpperCaseAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "use-upper-case")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)
        col = page.view.get_focus()[1]
        aeidon.util.affirm(col is not None)
        aeidon.util.affirm(page.view.is_text_column(col))

__all__ = tuple(x for x in dir() if x.endswith("Action"))
