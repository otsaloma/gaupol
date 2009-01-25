# Copyright (C) 2005-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Text formatting actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class ShowCaseMenuAction(gaupol.gtk.MenuAction):

    """Show the case format menu."""

    def __init__(self):
        """Initialize a ShowCaseMenuAction object."""

        gaupol.gtk.MenuAction.__init__(self, "show_case_menu")
        self.props.label = _("Ca_se")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class ToggleDialogDashesAction(gaupol.gtk.Action):

    """Toggle dialogue dashes on the selected texts."""

    def __init__(self):
        """Initialize a ToggleDialogDashesAction object."""

        gaupol.gtk.Action.__init__(self, "toggle_dialogue_dashes")
        self.props.label = _("_Dialogue")
        tooltip = _("Add or remove dialogue dashes on the selected texts")
        self.props.tooltip = tooltip
        self.accelerator = "D"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class ToggleItalicizationAction(gaupol.gtk.Action):

    """Toggle italicization of the selected texts."""

    def __init__(self):
        """Initialize a ToggleItalicizationAction object."""

        gaupol.gtk.Action.__init__(self, "toggle_italicization")
        self.props.label = _("_Italic")
        self.props.stock_id = gtk.STOCK_ITALIC
        self.props.tooltip = _("Italicize or unitalicize the selected texts")
        self.accelerator = "I"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))
        doc = page.text_column_to_document(col)
        markup = page.project.get_markup(doc)
        gaupol.util.affirm(markup is not None)
        gaupol.util.affirm(markup.italic_tag is not None)


class UseLowerCaseAction(gaupol.gtk.Action):

    """Change the selected texts to lower case."""

    def __init__(self):
        """Initialize a UseLowerCaseAction object."""

        gaupol.gtk.Action.__init__(self, "use_lower_case")
        self.props.label = _("_Lower")
        self.props.tooltip = _("Change the selected texts to lower case")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class UseSentenceCaseAction(gaupol.gtk.Action):

    """Change the selected texts to sentence case."""

    def __init__(self):
        """Initialize a UseSentenceCaseAction object."""

        gaupol.gtk.Action.__init__(self, "use_sentence_case")
        self.props.label = _("_Sentence")
        self.props.tooltip = _("Change the selected texts to sentence case")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class UseTitleCaseAction(gaupol.gtk.Action):

    """Change the selected texts to title case."""

    def __init__(self):
        """Initialize a UseTitleCaseAction object."""

        gaupol.gtk.Action.__init__(self, "use_title_case")
        self.props.label = _("_Title")
        self.props.tooltip = _("Change the selected texts to title case")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


class UseUpperCaseAction(gaupol.gtk.Action):

    def __init__(self):
        """Initialize a UseUpperCaseAction object."""

        gaupol.gtk.Action.__init__(self, "use_upper_case")
        self.props.label = _("_Upper")
        self.props.tooltip = _("Change the selected texts to upper case")
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(page.view.get_selected_rows())
        col = page.view.get_focus()[1]
        gaupol.util.affirm(page.view.is_text_column(col))


__all__ = gaupol.util.get_all(dir(), r"Action$")
