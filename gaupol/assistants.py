# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Assistant to guide through multiple text correction tasks."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _, n_
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("TextAssistant", "TextAssistantPage")


class TextAssistantPage(Gtk.Box):

    """
    Baseclass for pages of :class:`TextAssistant`.

   :ivar description: One-line description used in the introduction page
   :ivar handle: Unique unlocalized name for internal references
   :ivar page_title: Short string used as configuration page title
   :ivar page_type: A :class:`Gtk.AssistantPageType` constant
   :ivar title: Short title used in the introduction page

    Of these attributes, :attr:`description`, :attr:`handle` and :attr:`title`
    are only required for pages of type :attr:`Gtk.AssistantPageType.CONTENT`.
    """

    def __init__(self, assistant):
        """Initialize a :class:`TextAssistantPage` instance."""
        GObject.GObject.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.assistant = assistant
        self.description = None
        self.handle = None
        self.page_title = None
        self.page_type = None
        self.title = None


class BuilderPage(TextAssistantPage):

    """Baseclass for pages of :class:`TextAssistant` built with GtkBuilder."""

    _widgets = []

    def __init__(self, assistant, basename):
        """Initialize a :class:`BuilderPage` instance."""
        TextAssistantPage.__init__(self, assistant)
        self._builder = Gtk.Builder()
        self._builder.set_translation_domain("gaupol")
        self._builder.add_from_file(os.path.join(
            aeidon.DATA_DIR, "ui", "text-assistant", basename))
        self._builder.connect_signals(self)
        self._set_attributes(self._widgets)
        container = self._builder.get_object("main_container")
        window = container.get_parent()
        window.remove(container)
        self.add(container)
        gaupol.util.idle_add(window.destroy)

    def _set_attributes(self, widgets):
        """Assign all names in `widgets` as attributes of `self`."""
        for name in widgets:
            widget = self._builder.get_object(name)
            setattr(self, "_{}".format(name), widget)


class IntroductionPage(BuilderPage):

    """Page for listing all text correction tasks."""

    _widgets = ["columns_combo", "subtitles_combo", "tree_view"]

    def __init__(self, assistant):
        """Initialize a :class:`IntroductionPage` instance."""
        BuilderPage.__init__(self, assistant, "introduction-page.ui")
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Tasks and Target")
        self.page_type = Gtk.AssistantPageType.INTRO
        self._init_columns_combo()
        self._init_subtitles_combo()
        self._init_tree_view()
        self._init_values()

    def get_field(self):
        """Return the selected field."""
        index = self._columns_combo.get_active()
        return [gaupol.fields.MAIN_TEXT,
                gaupol.fields.TRAN_TEXT][index]

    def get_selected_pages(self):
        """Return selected content pages."""
        store = self._tree_view.get_model()
        return [x[0] for x in store if x[1]]

    def get_target(self):
        """Return the selected target."""
        index = self._subtitles_combo.get_active()
        return [gaupol.targets.SELECTED,
                gaupol.targets.CURRENT,
                gaupol.targets.ALL][index]

    def _init_columns_combo(self):
        """Initalize the columns target combo box."""
        store = Gtk.ListStore(str)
        self._columns_combo.set_model(store)
        store.append((_("Correct texts in the text column"),))
        store.append((_("Correct texts in the translation column"),))
        renderer = Gtk.CellRendererText()
        self._columns_combo.pack_start(renderer, expand=True)
        self._columns_combo.add_attribute(renderer, "text", 0)

    def _init_subtitles_combo(self):
        """Initalize the subtitles target combo box."""
        store = Gtk.ListStore(str)
        self._subtitles_combo.set_model(store)
        store.append((_("Correct texts in selected subtitles"),))
        store.append((_("Correct texts in current project"),))
        store.append((_("Correct texts in all open projects"),))
        renderer = Gtk.CellRendererText()
        self._subtitles_combo.pack_start(renderer, expand=True)
        self._subtitles_combo.add_attribute(renderer, "text", 0)

    def _init_tree_view(self):
        """Initialize the tree view of tasks."""
        store = Gtk.ListStore(object, bool, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        renderer = Gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        renderer.connect("toggled", self._on_tree_view_cell_toggled)
        column = Gtk.TreeViewColumn("", renderer, active=1)
        self._tree_view.append_column(column)
        renderer = Gtk.CellRendererText()
        renderer.props.ellipsize = Pango.EllipsizeMode.END
        column = Gtk.TreeViewColumn("", renderer, markup=2)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._columns_combo.set_active({
            gaupol.fields.MAIN_TEXT: 0,
            gaupol.fields.TRAN_TEXT: 1,
        }[gaupol.conf.text_assistant.field])
        self._subtitles_combo.set_active({
            gaupol.targets.SELECTED: 0,
            gaupol.targets.CURRENT: 1,
            gaupol.targets.ALL: 2,
        }[gaupol.conf.text_assistant.target])

    def _on_columns_combo_changed(self, *args):
        """Save the selected field."""
        gaupol.conf.text_assistant.field = self.get_field()

    def _on_subtitles_combo_changed(self, *args):
        """Save the selected target."""
        gaupol.conf.text_assistant.target = self.get_target()

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle and save task check button value."""
        store = self._tree_view.get_model()
        store[path][1] = not store[path][1]
        store[path][0].set_visible(store[path][1])
        pages = [x.handle for x in self.get_selected_pages()]
        gaupol.conf.text_assistant.pages = pages

    def populate_tree_view(self, content_pages):
        """Populate the tree view with tasks from `content_pages`."""
        self._tree_view.get_model().clear()
        store = self._tree_view.get_model()
        pages = gaupol.conf.text_assistant.pages
        for page in content_pages:
            title = GLib.markup_escape_text(page.title)
            description = GLib.markup_escape_text(page.description)
            markup = "<b>{}</b>\n{}".format(title, description)
            page.set_visible(page.handle in pages)
            store.append((page, page.handle in pages, markup))
        self._tree_view.get_selection().unselect_all()


class LocalePage(BuilderPage):

    """Page with script, language and coutry based pattern selection."""

    _ui_file_basename = NotImplementedError

    _widgets = [
        "country_combo",
        "country_label",
        "language_combo",
        "language_label",
        "script_combo",
        "script_label",
        "tree_view",
    ]

    def __init__(self, assistant):
        """Initialize a :class:`LocalePage` instance."""
        BuilderPage.__init__(self, assistant, self._ui_file_basename)
        self.conf = None
        self._init_attributes()
        self._init_tree_view()
        self._init_combo_boxes()
        self._init_values()

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        raise NotImplementedError

    def _filter_patterns(self, patterns):
        """Return a subset of `patterns` to show."""
        return patterns

    def _get_country(self):
        """Return the selected country or ``None``."""
        if not self._country_combo.get_sensitive(): return None
        index = self._country_combo.get_active()
        if index < 0: return None
        store = self._country_combo.get_model()
        value = store[index][0]
        return None if value == "other" else value

    def _get_language(self):
        """Return the selected language or ``None``."""
        if not self._language_combo.get_sensitive(): return None
        index = self._language_combo.get_active()
        if index < 0: return None
        store = self._language_combo.get_model()
        value = store[index][0]
        return None if value == "other" else value

    def _get_script(self):
        """Return the selected script or ``None``."""
        if not self._script_combo.get_sensitive(): return None
        index = self._script_combo.get_active()
        if index < 0: return None
        store = self._script_combo.get_model()
        value = store[index][0]
        return None if value == "other" else value

    def _init_attributes(self):
        """Initialize values of page attributes."""
        raise NotImplementedError

    def _init_combo(self, combo_box):
        """Initialize `combo_box` and populate with `items`."""
        store = Gtk.ListStore(str, str)
        combo_box.set_model(store)
        renderer = Gtk.CellRendererText()
        combo_box.pack_start(renderer, expand=True)
        combo_box.add_attribute(renderer, "text", 1)
        func = gaupol.util.separate_combo
        combo_box.set_row_separator_func(func, None)

    def _init_combo_boxes(self):
        """Initialize and populate combo boxes."""
        self._init_combo(self._script_combo)
        self._init_combo(self._language_combo)
        self._init_combo(self._country_combo)
        self._populate_script_combo()
        self._populate_language_combo()
        self._populate_country_combo()

    def _init_tree_view(self):
        """Initialize the tree view of individual corrections."""
        store = Gtk.ListStore(object, bool, bool, str)
        store_filter = store.filter_new()
        store_filter.set_visible_column(1)
        self._tree_view.set_model(store_filter)
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        renderer = Gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        renderer.connect("toggled", self._on_tree_view_cell_toggled)
        column = Gtk.TreeViewColumn("", renderer, active=2)
        self._tree_view.append_column(column)
        renderer = Gtk.CellRendererText()
        renderer.props.ellipsize = Pango.EllipsizeMode.END
        column = Gtk.TreeViewColumn("", renderer, markup=3)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""
        pass

    def _on_country_combo_changed(self, combo_box):
        """Populate the tree view with a subset patterns."""
        self.conf.country = self._get_country() or ""
        self._populate_tree_view()

    def _on_language_combo_changed(self, combo_box):
        """Populate the tree view with a subset patterns."""
        language = self._get_language()
        sensitive = language is not None
        self._populate_country_combo()
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        self.conf.language = language or ""
        self._populate_tree_view()

    def _on_script_combo_changed(self, combo_box):
        """Populate the tree view with a subset patterns."""
        script = self._get_script()
        sensitive = script is not None
        self._populate_language_combo()
        self._language_combo.set_sensitive(sensitive)
        self._language_label.set_sensitive(sensitive)
        language = self._get_language()
        sensitive = sensitive and language is not None
        self._populate_country_combo()
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        self.conf.script = script or ""
        self._populate_tree_view()

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle the check button value."""
        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        path = Gtk.TreePath.new_from_string(path)
        path = store_filter.convert_path_to_child_path(path)
        name = store[path][0].get_name(False)
        enabled = not store[path][2]
        for i in range(len(store)):
            # Toggle all patterns with the same name.
            if store[i][0].get_name(False) == name:
                store[i][0].enabled = enabled
                store[i][2] = enabled

    def _populate_combo(self, combo_box, items, active):
        """Populate `combo_box` with `items`."""
        store = combo_box.get_model()
        combo_box.set_model(None)
        store.clear()
        for code, name in items:
            store.append((code, name))
        if len(store) > 0:
            store.append((gaupol.COMBO_SEPARATOR, ""))
        store.append(("other", _("Other")))
        combo_box.set_active(len(store) - 1)
        for i in range(len(store)):
            if store[i][0] == active and active:
                combo_box.set_active(i)
        combo_box.set_model(store)

    def _populate_country_combo(self):
        """Populate the country combo box."""
        script = self._get_script()
        language = self._get_language()
        codes = self._manager.get_countries(script, language)
        names = list(map(aeidon.countries.code_to_name, codes))
        items = [(codes[i], names[i]) for i in range(len(codes))]
        items.sort(key=lambda x: x[1])
        self._populate_combo(self._country_combo, items, self.conf.country)

    def _populate_language_combo(self):
        """Populate the language combo box."""
        script = self._get_script()
        codes = self._manager.get_languages(script)
        names = list(map(aeidon.languages.code_to_name, codes))
        items = [(codes[i], names[i]) for i in range(len(codes))]
        items.sort(key=lambda x: x[1])
        self._populate_combo(self._language_combo, items, self.conf.language)

    def _populate_script_combo(self):
        """Populate the script combo box."""
        codes = self._manager.get_scripts()
        names = list(map(aeidon.scripts.code_to_name, codes))
        items = [(codes[i], names[i]) for i in range(len(codes))]
        items.sort(key=lambda x: x[1])
        self._populate_combo(self._script_combo, items, self.conf.script)

    def _populate_tree_view(self):
        """Populate the tree view with a subset patterns."""
        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        store.clear()
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        patterns = self._manager.get_patterns(script, language, country)
        patterns = self._filter_patterns(patterns)
        names_entered = set(())
        for pattern in patterns:
            name = pattern.get_name()
            visible = not name in names_entered
            names_entered.add(name)
            name = GLib.markup_escape_text(name)
            description = pattern.get_description()
            description = GLib.markup_escape_text(description)
            markup = "<b>{}</b>\n{}".format(name, description)
            store.append((pattern, visible, pattern.enabled, markup))
        self._tree_view.get_selection().unselect_all()


class CapitalizationPage(LocalePage):

    """Page for capitalizing texts in subtitles."""

    _ui_file_basename = "capitalization-page.ui"

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        self._manager.save_config(script, language, country)
        patterns = self._manager.get_patterns(script, language, country)
        project.capitalize(indices, doc, patterns)

    def _init_attributes(self):
        """Initialize values of page attributes."""
        self._manager = aeidon.PatternManager("capitalization")
        self.conf = gaupol.conf.capitalization
        self.description = _("Capitalize texts written in lower case")
        self.handle = "capitalization"
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Capitalization Patterns")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self.title = _("Capitalize texts")


class CommonErrorPage(LocalePage):

    """Page for correcting common human and OCR errors."""

    _ui_file_basename = "common-error-page.ui"
    _widgets = ["human_check", "ocr_check"] + LocalePage._widgets

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        self._manager.save_config(script, language, country)
        patterns = self._manager.get_patterns(script, language, country)
        project.correct_common_errors(indices, doc, patterns)

    def _init_attributes(self):
        """Initialize values of page attributes."""
        self._manager = aeidon.PatternManager("common-error")
        self.conf = gaupol.conf.common_error
        self.description = _("Correct common errors made by humans or image recognition software")
        self.handle = "common-error"
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Common Error Patterns")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self.title = _("Correct common errors")

    def _filter_patterns(self, patterns):
        """Return a subset of `patterns` to show."""
        def use_pattern(pattern):
            classes = set(pattern.get_field_list("Classes"))
            return(bool(classes & set(self.conf.classes)))
        return list(filter(use_pattern, patterns))

    def _init_values(self):
        """Initialize default values for widgets."""
        self._human_check.set_active("Human" in self.conf.classes)
        self._ocr_check.set_active("OCR" in self.conf.classes)

    def _on_human_check_toggled(self, check_button):
        """Populate the tree view with a subset patterns."""
        if check_button.get_active():
            self.conf.classes.append("Human")
            self.conf.classes = sorted(set(self.conf.classes))
        elif "Human" in self.conf.classes:
            self.conf.classes.remove("Human")
        self._populate_tree_view()

    def _on_ocr_check_toggled(self, check_button):
        """Populate the tree view with a subset patterns."""
        if check_button.get_active():
            self.conf.classes.append("OCR")
            self.conf.classes = sorted(set(self.conf.classes))
        elif "OCR" in self.conf.classes:
            self.conf.classes.remove("OCR")
        self._populate_tree_view()


class HearingImpairedPage(LocalePage):

    """Page for removing hearing impaired parts from subtitles."""

    _ui_file_basename = "hearing-impaired-page.ui"

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        self._manager.save_config(script, language, country)
        patterns = self._manager.get_patterns(script, language, country)
        project.remove_hearing_impaired(indices, doc, patterns)

    def _init_attributes(self):
        """Initialize values of page attributes."""
        self._manager = aeidon.PatternManager("hearing-impaired")
        self.conf = gaupol.conf.hearing_impaired
        self.description = _("Remove explanatory texts meant for the hearing impaired")
        self.handle = "hearing-impaired"
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Hearing Impaired Patterns")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self.title = _("Remove hearing impaired texts")


class JoinSplitWordsPage(BuilderPage):

    """Page for joining or splitting words based on spell-check suggestions."""

    _widgets = ["language_button", "join_check", "split_check"]

    def __init__(self, assistant):
        """Initialize a :class:`JoinSplitWordsPage` instance."""
        BuilderPage.__init__(self, assistant, "join-split-page.ui")
        self.description = _("Use spell-check suggestions to fix whitespace detection errors of image recognition software")
        self.handle = "join-split-words"
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Joining and Splitting Words")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self.title = _("Join or Split Words")
        self._init_values()

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        language = gaupol.conf.spell_check.language
        if gaupol.conf.join_split_words.join:
            try:
                # Can fail if the spell-check backend or dictionary is missing.
                project.spell_check_join_words(indices, doc, language)
            except Exception as error:
                return self._show_error_dialog(str(error))
        if gaupol.conf.join_split_words.split:
            try:
                # Can fail if the spell-check backend or dictionary is missing.
                project.spell_check_split_words(indices, doc, language)
            except Exception as error:
                return self._show_error_dialog(str(error))

    def _init_values(self):
        """Initialize default values for widgets."""
        language = gaupol.conf.spell_check.language
        language = aeidon.locales.code_to_name(language)
        self._language_button.set_label(language)
        self._join_check.set_active(gaupol.conf.join_split_words.join)
        self._split_check.set_active(gaupol.conf.join_split_words.split)

    def _on_join_check_toggled(self, check_button, *args):
        """Save value of join option."""
        gaupol.conf.join_split_words.join = check_button.get_active()

    def _on_language_button_clicked(self, button, *args):
        """Show a language dialog and update `button` label."""
        gaupol.util.set_cursor_busy(self.assistant)
        dialog = gaupol.LanguageDialog(self.assistant, False)
        gaupol.util.set_cursor_normal(self.assistant)
        gaupol.util.flash_dialog(dialog)
        language = gaupol.conf.spell_check.language
        language = aeidon.locales.code_to_name(language)
        self._language_button.set_label(language)

    def _on_split_check_toggled(self, check_button, *args):
        """Save value of split option."""
        gaupol.conf.join_split_words.split = check_button.get_active()

    def _show_error_dialog(self, message):
        """Show an error dialog after failing to load dictionary."""
        name = gaupol.conf.spell_check.language
        name = aeidon.locales.code_to_name(name)
        title = _('Failed to load dictionary for language "{}"').format(name)
        dialog = gaupol.ErrorDialog(self.get_ancestor(Gtk.Window), title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)


class LineBreakPage(LocalePage):

    """Page for breaking text into lines."""

    _ui_file_basename = "line-break-page.ui"

    def correct_texts(self, project, indices, doc):
        """Correct texts in `project`."""
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        self._manager.save_config(script, language, country)
        patterns = self._manager.get_patterns(script, language, country)
        length_func = gaupol.ruler.get_length_function(self.conf.length_unit)
        skip = self.conf.use_skip_max_length or self.conf.use_skip_max_lines
        project.break_lines(indices=indices,
                            doc=doc,
                            patterns=patterns,
                            length_func=length_func,
                            max_length=self.conf.max_length,
                            max_lines=self.conf.max_lines,
                            skip=skip,
                            max_skip_length=self._max_skip_length,
                            max_skip_lines=self._max_skip_lines)

    def _init_attributes(self):
        """Initialize values of page attributes."""
        self._manager = aeidon.PatternManager("line-break")
        self.conf = gaupol.conf.line_break
        self.description = _("Break text into lines of defined length")
        self.handle = "line-break"
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Line-Break Patterns")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self.title = _("Break lines")

    @property
    def _max_skip_length(self):
        """Return the maximum line length to skip."""
        if self.conf.use_skip_max_length:
            return self.conf.skip_max_length
        return 32768

    @property
    def _max_skip_lines(self):
        """Return the maximum amount of lines to skip."""
        if self.conf.use_skip_max_lines:
            return self.conf.skip_max_lines
        return 32768


class LineBreakOptionsPage(BuilderPage):

    """Page for editing line-break options."""

    _widgets = [
        "max_length_spin",
        "max_lines_spin",
        "max_skip_length_spin",
        "max_skip_lines_spin",
        "skip_length_check",
        "skip_lines_check",
        "skip_unit_combo",
        "unit_combo",
    ]

    def __init__(self, assistant):
        """Initialize a :class:`LineBreakOptionsPage` instance."""
        BuilderPage.__init__(self, assistant, "line-break-options-page.ui")
        self.conf = gaupol.conf.line_break
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Line-Break Options")
        self.page_type = Gtk.AssistantPageType.CONTENT
        self._init_unit_combo(self._unit_combo)
        self._init_unit_combo(self._skip_unit_combo)
        self._init_values()

    def _init_unit_combo(self, combo_box):
        """Initialize line length unit `combo_box`."""
        store = Gtk.ListStore(str)
        combo_box.set_model(store)
        for label in (x.label for x in gaupol.length_units):
            store.append((label,))
        renderer = Gtk.CellRendererText()
        combo_box.pack_start(renderer, expand=True)
        combo_box.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._max_length_spin.set_value(self.conf.max_length)
        self._max_lines_spin.set_value(self.conf.max_lines)
        self._max_skip_length_spin.set_value(self.conf.skip_max_length)
        self._max_skip_lines_spin.set_value(self.conf.skip_max_lines)
        self._skip_length_check.set_active(self.conf.use_skip_max_length)
        self._skip_lines_check.set_active(self.conf.use_skip_max_lines)
        self._skip_unit_combo.set_active(self.conf.length_unit)
        self._unit_combo.set_active(self.conf.length_unit)

    def _on_max_length_spin_value_changed(self, spin_button):
        """Save maximum line length value."""
        self.conf.max_length = spin_button.get_value_as_int()

    def _on_max_lines_spin_value_changed(self, spin_button):
        """Save maximum line amount value."""
        self.conf.max_lines = spin_button.get_value_as_int()

    def _on_max_skip_length_spin_value_changed(self, spin_button):
        """Save maximum line length to skip value."""
        self.conf.skip_max_length = spin_button.get_value_as_int()

    def _on_max_skip_lines_spin_value_changed(self, spin_button):
        """Save maximum line amount to skip value."""
        self.conf.skip_max_lines = spin_button.get_value_as_int()

    def _on_skip_length_check_toggled(self, check_button):
        """Save skip by line length value."""
        use_skip = check_button.get_active()
        self.conf.use_skip_max_length = use_skip
        self._max_skip_length_spin.set_sensitive(use_skip)
        self._skip_unit_combo.set_sensitive(use_skip)

    def _on_skip_lines_check_toggled(self, check_button):
        """Save skip by line amount value."""
        use_skip = check_button.get_active()
        self.conf.use_skip_max_lines = use_skip
        self._max_skip_lines_spin.set_sensitive(use_skip)

    def _on_skip_unit_combo_changed(self, combo_box):
        """Save and sync length unit value of `combo_box."""
        index = combo_box.get_active()
        length_unit = gaupol.length_units[index]
        self.conf.length_unit = length_unit
        self._unit_combo.set_active(index)

    def _on_unit_combo_changed(self, combo_box):
        """Save and sync length unit value of `combo_box."""
        index = combo_box.get_active()
        length_unit = gaupol.length_units[index]
        self.conf.length_unit = length_unit
        self._skip_unit_combo.set_active(index)


class ProgressPage(BuilderPage):

    """Page for showing progress of text corrections."""

    _widgets = ["message_label", "progress_bar", "status_label", "task_label"]

    def __init__(self, assistant):
        """Initialize a :class:`ProgressPage` instance."""
        BuilderPage.__init__(self, assistant, "progress-page.ui")
        self._current_task = None
        self._total_tasks = None
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Correcting Texts")
        self.page_type = Gtk.AssistantPageType.PROGRESS
        self._init_values()

    def _init_values(self):
        """Initalize default values for widgets."""
        message = _("Each task is now being run on each project.")
        self._message_label.set_text(message)
        self.reset(100)

    def bump_progress(self, n=1):
        """Bump the current progress by `n`."""
        self.set_progress(self._current_task + n)

    def reset(self, total, clear_text=False):
        """Set `total` as the amount of tasks to be run."""
        self._current_task = 0
        self._total_tasks = total
        self.set_progress(0, total)
        self.set_project_name("")
        self.set_task_name("")
        if clear_text:
            self._progress_bar.set_text("")
        gaupol.util.iterate_main()

    def set_progress(self, current, total=None):
        """Set current as the task progress status."""
        total = total or self._total_tasks
        fraction = current / total if total > 0 else 0
        self._progress_bar.set_fraction(fraction)
        text = _("{current:d} of {total:d} tasks complete")
        self._progress_bar.set_text(text.format(**locals()))
        self._current_task = current
        self._total_tasks = total
        gaupol.util.iterate_main()

    def set_project_name(self, name):
        """Set `name` as the currently checked project."""
        text = _("Project: {}").format(name)
        self._status_label.set_text(text)
        gaupol.util.iterate_main()

    def set_task_name(self, name):
        """Set `name` as the currently performed task."""
        text = _("Task: {}").format(name)
        self._task_label.set_text(text)
        gaupol.util.iterate_main()


class ConfirmationPage(BuilderPage):

    """Page to confirm changes made after performing all tasks."""

    _widgets = [
        "mark_all_button",
        "preview_button",
        "remove_check",
        "tree_view",
        "unmark_all_button",
    ]

    def __init__(self, assistant):
        """Initialize a :class:`ConfirmationPage` instance."""
        BuilderPage.__init__(self, assistant, "confirmation-page.ui")
        self.application = None
        self.conf = gaupol.conf.text_assistant
        self.doc = None
        # TRANSLATORS: Keep these page titles short, since they
        # affect the width of the text correction assistant sidebar.
        self.page_title = _("Confirm Changes")
        self.page_type = Gtk.AssistantPageType.CONFIRM
        self._init_tree_view()
        self._init_values()

    def _add_text_column(self, index, ref_index, title):
        """Add a multiline text column to the tree view."""
        renderer = gaupol.MultilineDiffCellRenderer()
        renderer.set_show_lengths(True)
        renderer.props.editable = (index == 4)
        renderer.props.ellipsize = Pango.EllipsizeMode.END
        renderer.props.font = gaupol.util.get_font()
        renderer.props.ref_type = ref_index - index
        renderer.props.yalign = 0
        renderer.props.xpad = 4
        renderer.props.ypad = 4
        column = Gtk.TreeViewColumn(
            title, renderer, text=index, ref_text=ref_index)
        column.set_resizable(True)
        column.set_expand(True)
        self._tree_view.append_column(column)

    def _can_preview(self):
        """Return ``True`` if preview is possible."""
        row = self._get_selected_row()
        if row is None: return False
        store = self._tree_view.get_model()
        page = store[row][0]
        if page is None: return False
        return bool(page.project.video_path and page.project.main_file)

    def get_confirmed_changes(self):
        """Return a sequence of changes marked as accepted."""
        changes = []
        store = self._tree_view.get_model()
        for row in (x for x in store if x[2]):
            page, index, accept, orig, new = row
            changes.append((page, index, orig, new))
        return tuple(changes)

    def _get_selected_row(self):
        """Return the selected row in the tree view or ``None``."""
        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        path = store.get_path(itr)
        return gaupol.util.tree_path_to_row(path)

    def _init_tree_view(self):
        """Initialize the tree view of corrections."""
        # page, index, accept, original text, new text
        store = Gtk.ListStore(object, int, bool, str, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        renderer = Gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        renderer.connect("toggled", self._on_tree_view_cell_toggled)
        column = Gtk.TreeViewColumn(_("Accept"), renderer, active=2)
        column.set_resizable(True)
        self._tree_view.append_column(column)
        if gaupol.conf.editor.use_zebra_stripes:
            callback = self._on_renderer_set_background
            column.set_cell_data_func(renderer, callback, None)
        self._add_text_column(3, 4, _("Original Text"))
        self._add_text_column(4, 3, _("Corrected Text"))
        column = self._tree_view.get_column(2)
        renderer = column.get_cells()[0]
        renderer.connect("edited", self._on_tree_view_cell_edited)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._remove_check.set_active(self.conf.remove_blank)
        self._preview_button.set_sensitive(False)

    def _on_mark_all_button_clicked(self, *args):
        """Set all accept column values to ``True``."""
        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = True

    def _on_preview_button_clicked(self, *args):
        """Preview original text in a video player."""
        row = self._get_selected_row()
        store = self._tree_view.get_model()
        page = store[row][0]
        index = store[row][1]
        position = page.project.subtitles[index].start
        self.application.preview(page, position, self.doc)

    def _on_remove_check_toggled(self, check_button):
        """Save remove blank subtitles value."""
        self.conf.remove_blank = check_button.get_active()

    def _on_renderer_set_background(self, column, renderer, store, itr, data):
        """Set zerba-striped backgrounds for all columns."""
        path = self._tree_view.get_model().get_path(itr)
        row = gaupol.util.tree_path_to_row(path)
        color = (gaupol.util.get_zebra_color(self._tree_view)
                 if row % 2 == 0 else None)

        for column in self._tree_view.get_columns():
            for renderer in column.get_cells():
                renderer.props.cell_background_rgba = color

    def _on_tree_view_cell_edited(self, renderer, path, text):
        """Edit text in the corrected text column."""
        store = self._tree_view.get_model()
        store[path][4] = text

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle accept column value."""
        store = self._tree_view.get_model()
        store[path][2] = not store[path][2]

    def _on_tree_view_selection_changed(self, *args):
        """Update preview button sensitivity."""
        self._preview_button.set_sensitive(self._can_preview())

    def _on_unmark_all_button_clicked(self, *args):
        """Set all accept column values to ``False``."""
        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = False

    def populate_tree_view(self, changes):
        """Populate the tree view of changes to texts."""
        self._tree_view.get_model().clear()
        store = self._tree_view.get_model()
        for page, index, orig, new in changes:
            store.append((page, index, True, orig, new))
        self._tree_view.get_selection().unselect_all()


class TextAssistant(Gtk.Assistant):

    """Assistant to guide through multiple text correction tasks."""

    def __init__(self, parent, application):
        """Initialize a :class:`TextAssistant` instance."""
        GObject.GObject.__init__(self)
        self._confirmation_page = ConfirmationPage(self)
        self._introduction_page = IntroductionPage(self)
        self._previous_page = None
        self._progress_page = ProgressPage(self)
        self.application = application
        self._init_properties()
        self._init_signal_handlers()
        self.resize(*gaupol.conf.text_assistant.size)
        if gaupol.conf.text_assistant.maximized:
            self.maximize()
        self.set_modal(True)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_transient_for(parent)

    def add_page(self, page):
        """Add `page` and configure its properties."""
        page.show_all()
        self.append_page(page)
        self.set_page_type(page, page.page_type)
        self.set_page_title(page, page.page_title)
        if page.page_type != Gtk.AssistantPageType.PROGRESS:
            self.set_page_complete(page, True)

    def add_pages(self, pages):
        """Add associated `pages` and configure their properties."""
        for page in pages:
            self.add_page(page)
        def on_notify_visible(page, prop, pages):
            for page in pages[1:]:
                page.set_visible(pages[0].get_visible())
        pages[0].connect("notify::visible", on_notify_visible, pages)

    def _copy_project(self, project):
        """Return a copy of `project` with some same properties."""
        copy = aeidon.Project(project.framerate)
        copy.main_file = project.main_file
        copy.tran_file = project.tran_file
        copy.subtitles = [x.copy() for x in project.subtitles]
        return copy

    def _correct_texts(self, assistant_pages):
        """Correct texts by all pages and present changes."""
        changes = []
        target = self._introduction_page.get_target()
        field = self._introduction_page.get_field()
        doc = gaupol.util.text_field_to_document(field)
        rows = self.application.get_target_rows(target)
        application_pages = self.application.get_target_pages(target)
        total = len(application_pages) * len(assistant_pages)
        self._progress_page.reset(total)
        for application_page in application_pages:
            name = application_page.get_main_basename()
            self._progress_page.set_project_name(name)
            project = application_page.project
            # Initialize a dummy project to apply corrections in
            # to be able to present those corrections for approval and
            # to finally be able to apply only approved corrections.
            dummy = self._copy_project(project)
            static_subtitles = dummy.subtitles[:]
            for page in assistant_pages:
                self._progress_page.set_task_name(page.title)
                page.correct_texts(dummy, rows, doc)
                self._progress_page.bump_progress()
            for i in range(len(static_subtitles)):
                orig = project.subtitles[i].get_text(doc)
                new = static_subtitles[i].get_text(doc)
                if orig == new: continue
                changes.append((application_page, i, orig, new))
        self._prepare_confirmation_page(doc, changes)
        self.set_current_page(self.get_current_page() + 1)

    def _init_properties(self):
        """Initialize assistant properties."""
        self.set_title(_("Correct Texts"))
        self.add_page(self._introduction_page)
        self.add_page(HearingImpairedPage(self))
        if (aeidon.SpellChecker.available() and
            aeidon.SpellChecker.list_languages()):
            self.add_page(JoinSplitWordsPage(self))
        self.add_page(CommonErrorPage(self))
        self.add_page(CapitalizationPage(self))
        self.add_pages((LineBreakPage(self), LineBreakOptionsPage(self)))
        self.add_page(self._progress_page)
        self.add_page(self._confirmation_page)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "apply")
        aeidon.util.connect(self, self, "cancel")
        aeidon.util.connect(self, self, "close")
        aeidon.util.connect(self, self, "prepare")
        aeidon.util.connect(self, self, "window-state-event")

    def _on_apply(self, *args):
        """Apply accepted changes to projects."""
        gaupol.util.set_cursor_busy(self)
        edits = removals = 0
        changes = self._confirmation_page.get_confirmed_changes()
        changed_pages = aeidon.util.get_unique([x[0] for x in changes])
        field = self._introduction_page.get_field()
        doc = gaupol.util.text_field_to_document(field)
        description = _("Correcting texts")
        register = aeidon.registers.DO
        for page in changed_pages:
            indices = [x[1] for x in changes if x[0] is page]
            texts = [x[3] for x in changes if x[0] is page]
            if indices and texts:
                page.project.replace_texts(indices, doc, texts)
                page.project.set_action_description(register, description)
                edits += len(indices)
            indices = [x for i, x in enumerate(indices) if not texts[i]]
            if indices and gaupol.conf.text_assistant.remove_blank:
                page.project.remove_subtitles(indices)
                page.project.group_actions(register, 2, description)
                removals += len(indices)
            page.view.columns_autosize()
        edits = edits - removals
        message = _("Edited {edits:d} and removed {removals:d} subtitles")
        self.application.flash_message(message.format(**locals()))
        gaupol.util.set_cursor_normal(self)

    def _on_cancel(self, *args):
        """Destroy assistant."""
        self._save_window_geometry()
        self.destroy()

    def _on_close(self, *args):
        """Destroy assistant."""
        self._save_window_geometry()
        self.destroy()

    def _on_prepare(self, assistant, page):
        """Prepare `page` to be shown next."""
        previous_page = self._previous_page
        self._previous_page = page
        if page is self._introduction_page:
            return self._prepare_introduction_page()
        pages = self._introduction_page.get_selected_pages()
        if page is self._progress_page:
            if previous_page is not self._confirmation_page:
                return self._prepare_progress_page(pages)

    def _on_window_state_event(self, window, event):
        """Save window maximization."""
        state = event.new_window_state
        maximized = bool(state & Gdk.WindowState.MAXIMIZED)
        gaupol.conf.text_assistant.maximized = maximized

    def _prepare_confirmation_page(self, doc, changes):
        """Present `changes` and activate confirmation page."""
        count = len(changes)
        title = n_("Confirm {:d} Change",
                   "Confirm {:d} Changes",
                   count).format(count)

        self.set_page_title(self._confirmation_page, title)
        self._confirmation_page.application = self.application
        self._confirmation_page.doc = doc
        self._confirmation_page.populate_tree_view(changes)
        self.set_page_complete(self._progress_page, True)

    def _prepare_introduction_page(self):
        """Prepare introduction page content."""
        n = self.get_n_pages()
        pages = list(map(self.get_nth_page, range(n)))
        pages.remove(self._introduction_page)
        pages.remove(self._progress_page)
        pages.remove(self._confirmation_page)
        pages = [x for x in pages if hasattr(x, "correct_texts")]
        self._introduction_page.populate_tree_view(pages)

    def _prepare_progress_page(self, pages):
        """Prepare progress page for `pages`."""
        self._progress_page.reset(0, True)
        self.set_page_complete(self._progress_page, False)
        gaupol.util.delay_add(10, self._correct_texts, pages)

    def _save_window_geometry(self):
        """Save the geometry of the assistant window."""
        if not gaupol.conf.text_assistant.maximized:
            gaupol.conf.text_assistant.size = list(self.get_size())
