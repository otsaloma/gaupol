# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Text menu UI manager actions."""


import gtk
from gettext import gettext as _

from gaupol.gtk.index import *
from gaupol.tags import *
from ._action import UIMAction


class _FormatAction(UIMAction):

    """Base class for text formatting actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class ClearTextsAction(UIMAction):

    """Clear the selected texts."""

    action_item = (
        "clear_texts",
        gtk.STOCK_CLEAR,
        _("C_lear"),
        "C",
        _("Clear the selected texts"),)

    paths = ["/ui/menubar/text/clear"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class CopyTextsAction(UIMAction):

    """Copy the selected texts to the clipboard."""

    action_item = (
        "copy_texts",
        gtk.STOCK_COPY,
        _("_Copy"),
        "<control>C",
        _("Copy the selected texts to the clipboard"),)

    paths = ["/ui/menubar/text/copy"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class CutTextsAction(UIMAction):

    """Cut the selected texts to the clipboard."""

    action_item = (
        "cut_texts",
        gtk.STOCK_CUT,
        _("Cu_t"),
        "<control>X",
        _("Cut the selected texts to the clipboard"),)

    paths = ["/ui/menubar/text/cut"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            selection = bool(page.view.get_selected_rows())
            focus = page.view.get_focus()[1] in (MTXT, TTXT)
            return bool(selection and focus)
        return False


class FindAndReplaceAction(UIMAction):

    """Search for and replace text."""

    action_item = (
        "find_and_replace",
        gtk.STOCK_FIND_AND_REPLACE,
        _("_Find And Replace..."),
        "<control>F",
        _("Search for and replace text"),)

    paths = [
        "/ui/menubar/text/find_and_replace",
        "/ui/main_toolbar/find_and_replace"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class FindNextAction(UIMAction):

    """Search forwards for same text."""

    action_item = (
        "find_next",
        None,
        _("Find _Next"),
        "<control>G",
        _("Search forwards for same text"),)

    paths = ["/ui/menubar/text/find_next"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return bool(application.pattern)


class FindPreviousAction(UIMAction):

    """Search backwards for same text."""

    action_item = (
        "find_previous",
        None,
        _("Find _Previous"),
        "<shift><control>G",
        _("Search backwards for same text"),)

    paths = ["/ui/menubar/text/find_previous"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return bool(application.pattern)


class PasteTextsAction(UIMAction):

    """Paste texts from the clipboard."""

    action_item = (
        "paste_texts",
        gtk.STOCK_PASTE,
        _("_Paste"),
        "<control>V",
        _("Paste texts from the clipboard"),)

    paths = ["/ui/menubar/text/paste"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if (page is not None) and application.clipboard.data:
            selection = bool(page.view.get_selected_rows())
            focus = (page.view.get_focus()[1] in (MTXT, TTXT))
            return bool(selection and focus)
        return False


class ShowCaseMenuAction(_FormatAction):

    """Show the case format menu."""

    menu_item = (
        "show_case_menu",
        None,
        _("_Case"),
        None,
        None,)

    paths = ["/ui/menubar/text/case"]


class ToggleDialogLinesAction(_FormatAction):

    """Toggle dialogue lines on the selected texts."""

    action_item = (
        "toggle_dialogue_lines",
        None,
        _("_Dialogue"),
        "D",
        _("Toggle dialogue lines on the selected texts"),)

    paths = ["/ui/menubar/text/dialogue"]


class ToggleItalicizationAction(UIMAction):

    """Toggle italicization of the selected texts."""

    action_item = (
        "toggle_italicization",
        gtk.STOCK_ITALIC,
        _("_Italic"),
        "I",
        _("Toggle italicization of the selected texts"),)

    paths = ["/ui/menubar/text/italic"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        try:
            assert page.view.get_selected_rows()
            col = page.view.get_focus()[1]
            doc = page.text_column_to_document(col)
            name = page.project.get_format_class_name(doc)
            return (eval(name).italic_tag is not None)
        except Exception:
            return False


class UseLowerCaseAction(_FormatAction):

    """Change the selected texts to lower case."""

    action_item = (
        "use_lower_case",
        None,
        _("_Lower"),
        "<shift>U",
        _("Change the selected texts to lower case"),)

    paths = ["/ui/menubar/text/case/lower"]


class UseSentenceCaseAction(_FormatAction):

    """Change the selected texts to sentence case."""

    action_item = (
        "use_sentence_case",
        None,
        _("_Sentence"),
        "<shift>T",
        _("Change the selected texts to sentence case"),)

    paths = ["/ui/menubar/text/case/sentence"]


class UseTitleCaseAction(_FormatAction):

    """Change the selected texts to title case."""

    action_item = (
        "use_title_case",
        None,
        _("_Title"),
        "T",
        _("Change the selected texts to title case"),)

    paths = ["/ui/menubar/text/case/title"]


class UseUpperCaseAction(_FormatAction):

    """Change the selected texts to upper case."""

    action_item = (
        "use_upper_case",
        None,
        _("_Upper"),
        "U",
        _("Change the selected texts to upper case"),)

    paths = ["/ui/menubar/text/case/upper"]
