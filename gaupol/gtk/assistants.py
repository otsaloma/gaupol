# Copyright (C) 2007-2008 Osmo Salomaa
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

"""Assistant to guide through multiple text correction tasks."""

from __future__ import division

import gaupol.gtk
import gobject
import gtk
import pango
import sys
_ = gaupol.i18n._
ngettext = gaupol.i18n.ngettext

__all__ = ("TextAssistant", "TextAssistantPage")


class TextAssistantPage(gtk.VBox):

    """Baseclass for pages in the text correction assistant.

    Instance variables:
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
        self.set_border_width(12)


class _GladePage(TextAssistantPage):

    """Baseclass for Glade pages in the text correction assistant."""

    def __init__(self, glade_basename):

        TextAssistantPage.__init__(self)
        parts = ("assistants", "text", glade_basename)
        self._glade_xml = gaupol.gtk.util.get_glade_xml(*parts)
        self._glade_xml.get_widget("vbox").reparent(self)


class _IntroductionPage(_GladePage):

    """Page for listing all text correction tasks."""

    def __init__(self):

        _GladePage.__init__(self, "introduction.glade")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._main_radio = get_widget("main_radio")
        self._selected_radio = get_widget("selected_radio")
        self._tran_radio = get_widget("tran_radio")
        self._tree_view = get_widget("tree_view")

        self.conf = gaupol.gtk.conf.text_assistant
        self.page_title = _("Select Tasks and Target")
        self.page_type = gtk.ASSISTANT_PAGE_INTRO

        self._init_tree_view()
        self._init_values()
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        def save_field(radio_button, self):
            self.conf.field = self.get_field()
        self._main_radio.connect("toggled", save_field, self)
        self._tran_radio.connect("toggled", save_field, self)

        def save_target(radio_button, self):
            self.conf.target = self.get_target()
        self._all_radio.connect("toggled", save_target, self)
        self._current_radio.connect("toggled", save_target, self)
        self._selected_radio.connect("toggled", save_target, self)

    def _init_tree_view(self):
        """Initialize the tree view."""

        store = gtk.ListStore(object, bool, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback)
        column = gtk.TreeViewColumn("", renderer, active=1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        column = gtk.TreeViewColumn("", renderer, markup=2)
        self._tree_view.append_column(column)

    def _on_tree_view_cell_toggled(self, renderer, row):
        """Toggle and save the check button value."""

        store = self._tree_view.get_model()
        store[row][1] = not store[row][1]
        store[row][0].props.visible = store[row][1]
        pages = [x.handle for x in self.get_selected_pages()]
        self.conf.pages = pages

    def _init_values(self):
        """Initialize default values for widgets."""

        fields = gaupol.gtk.fields
        self._main_radio.set_active(self.conf.field == fields.MAIN_TEXT)
        self._tran_radio.set_active(self.conf.field == fields.TRAN_TEXT)
        targets = gaupol.gtk.targets
        self._all_radio.set_active(self.conf.target == targets.ALL)
        self._current_radio.set_active(self.conf.target == targets.CURRENT)
        self._selected_radio.set_active(self.conf.target == targets.SELECTED)

    def get_field(self):
        """Return the selected field."""

        if self._main_radio.get_active():
            return gaupol.gtk.fields.MAIN_TEXT
        if self._tran_radio.get_active():
            return gaupol.gtk.fields.TRAN_TEXT
        raise ValueError

    def get_selected_pages(self):
        """Return the selected content pages."""

        store = self._tree_view.get_model()
        return [x[0] for x in store if x[1]]

    def get_target(self):
        """Return the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.gtk.targets.ALL
        raise ValueError

    def populate_tree_view(self, content_pages):
        """Populate the tree view with content pages."""

        self._tree_view.get_model().clear()
        store = self._tree_view.get_model()
        for page in content_pages:
            title = gobject.markup_escape_text(page.title)
            description = gobject.markup_escape_text(page.description)
            markup = "<b>%s</b>\n%s" % (title, description)
            page.props.visible = (page.handle in self.conf.pages)
            store.append((page, page.handle in self.conf.pages, markup))
        self._tree_view.get_selection().unselect_all()


class _LocalePage(_GladePage):

    """Page with script, language and coutry based pattern selection."""

    __metaclass__ = gaupol.gtk.ContractualGObject
    _glade_basename = None

    def __init__(self):

        _GladePage.__init__(self, self._glade_basename)
        get_widget = self._glade_xml.get_widget
        self._country_combo = get_widget("country_combo")
        self._country_label = get_widget("country_label")
        self._language_combo = get_widget("language_combo")
        self._language_label = get_widget("language_label")
        self._script_combo = get_widget("script_combo")
        self._script_label = get_widget("script_label")
        self._tree_view = get_widget("tree_view")
        self.conf = None

        self._init_attributes()
        self._init_signal_handlers()
        self._init_tree_view()
        self._init_script_combo()
        self._init_language_combo()
        self._init_country_combo()

    def _filter_patterns(self, patterns):
        """Return a subset of patterns to show."""

        return patterns

    def _get_country_ensure(self, value):
        if value is not None:
            assert gaupol.countries.is_valid(value)

    def _get_country(self):
        """Return the selected country or None."""

        index = self._country_combo.get_active()
        store = self._country_combo.get_model()
        if not self._country_combo.props.sensitive: return None
        if index >= (len(store) - 1): return None
        return store[index][0]

    def _get_language_ensure(self, value):
        if value is not None:
            assert gaupol.languages.is_valid(value)

    def _get_language(self):
        """Return the selected language or None."""

        index = self._language_combo.get_active()
        store = self._language_combo.get_model()
        if not self._language_combo.props.sensitive: return None
        if index >= (len(store) - 1): return None
        return store[index][0]

    def _get_script_ensure(self, value):
        if value is not None:
            assert gaupol.scripts.is_valid(value)

    def _get_script(self):
        """Return the selected script or None."""

        index = self._script_combo.get_active()
        store = self._script_combo.get_model()
        if not self._script_combo.props.sensitive: return None
        if index >= (len(store) - 1): return None
        return store[index][0]

    def _init_attributes(self):
        """Initialize values of page attributes."""

        raise NotImplementedError

    def _init_combo(self, combo_box, items, active):
        """Initialize combo box and its values."""

        store = gtk.ListStore(str, str)
        combo_box.set_model(store)
        for code, name in items:
            store.append((code, name))
        if len(store) > 0:
            store.append((gaupol.gtk.COMBO_SEPARATOR, ""))
        store.append(("", _("Other")))
        view = combo_box.get_child()
        view.set_displayed_row(0)
        renderer = view.get_cell_renderers()[0]
        combo_box.set_attributes(renderer, text=1)
        function = gaupol.gtk.util.separate_combo
        combo_box.set_row_separator_func(function)
        for i in range(len(store)):
            if (store[i][0] == active) and active:
                return combo_box.set_active(i)
        combo_box.set_active(len(store) - 1)

    def _init_country_combo(self):
        """Initialize the country combo box."""

        combo_box = self._country_combo
        script = self._get_script()
        language = self._get_language()
        codes = self._manager.get_countries(script, language)
        items = [(x, gaupol.countries.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        self._init_combo(combo_box, items, self.conf.country)

    def _init_language_combo(self):
        """Initialize the language combo box."""

        combo_box = self._language_combo
        script = self._get_script()
        codes = self._manager.get_languages(script)
        items = [(x, gaupol.languages.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        self._init_combo(combo_box, items, self.conf.language)

    def _init_script_combo(self):
        """Initialize the script combo box."""

        combo_box = self._script_combo
        codes = self._manager.get_scripts()
        items = [(x, gaupol.scripts.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        self._init_combo(combo_box, items, self.conf.script)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_country_combo", "changed")
        gaupol.util.connect(self, "_language_combo", "changed")
        gaupol.util.connect(self, "_script_combo", "changed")

    def _init_tree_view(self):
        """Initialize the tree view."""

        store = gtk.ListStore(object, bool, bool, str)
        store_filter = store.filter_new()
        store_filter.set_visible_column(1)
        self._tree_view.set_model(store_filter)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback)
        column = gtk.TreeViewColumn("", renderer, active=2)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        column = gtk.TreeViewColumn("", renderer, markup=3)
        self._tree_view.append_column(column)

    def _invariant(self):
        if self.conf is not None:
            assert hasattr(self.conf, "script")
            assert hasattr(self.conf, "language")
            assert hasattr(self.conf, "country")

    def _on_country_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        self.conf.country = self._get_country() or ""
        self._populate_tree_view()

    def _on_language_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        language = self._get_language()
        sensitive = (language is not None)
        self._init_country_combo()
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        self.conf.language = language or ""
        self._populate_tree_view()

    def _on_script_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        script = self._get_script()
        sensitive = (script is not None)
        self._init_language_combo()
        self._language_combo.set_sensitive(sensitive)
        self._language_label.set_sensitive(sensitive)
        language = self._get_language()
        sensitive = (sensitive and (language is not None))
        self._init_country_combo()
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        self.conf.script = script or ""
        self._populate_tree_view()

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle the check button value."""

        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        row = store_filter.convert_path_to_child_path(path)[0]
        name = store[row][0].get_name(False)
        enabled = not store[row][2]
        for i in range(len(store)):
            # Toggle all patterns with the same name.
            if store[i][0].get_name(False) == name:
                store[i][0].enabled = enabled
                store[i][2] = enabled

    def _populate_tree_view(self):
        """Populate the tree view with the correct patterns."""

        store_filter = self._tree_view.get_model()
        store = store_filter.get_model()
        store.clear()
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        patterns = self._manager.get_patterns(*codes)
        patterns = self._filter_patterns(patterns)
        names_entered = set(())
        for pattern in patterns:
            name = pattern.get_name()
            visible = not (name in names_entered)
            names_entered.add(name)
            name = gobject.markup_escape_text(name)
            description = pattern.get_description()
            description = gobject.markup_escape_text(description)
            markup = "<b>%s</b>\n%s" % (name, description)
            store.append((pattern, visible, pattern.enabled, markup))
        self._tree_view.get_selection().unselect_all()

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        raise NotImplementedError


class _CapitalizationPage(_LocalePage):

    """Page for capitalizing texts in subtitles."""

    _glade_basename = "capitalization.glade"

    def _init_attributes(self):
        """Initialize values of page attributes."""

        self._manager = gaupol.PatternManager("capitalization")
        self.conf = gaupol.gtk.conf.capitalization
        self.description = _("Capitalize texts written in lower case")
        self.handle = "capitalization"
        self.page_title = _("Select Capitalization Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Capitalize texts")

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save_config(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.capitalize(indices, doc, patterns)


class _CommonErrorPage(_LocalePage):

    """Page for correcting common human and OCR errors."""

    _glade_basename = "common-error.glade"

    def _init_attributes(self):
        """Initialize values of page attributes."""

        self._manager = gaupol.PatternManager("common-error")
        self.conf = gaupol.gtk.conf.common_error
        self.description = _("Correct common errors "
            "made by humans or image recognition software")
        self.handle = "common-error"
        self.page_title = _("Select Common Error Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Correct common errors")

        get_widget = self._glade_xml.get_widget
        self._human_check = get_widget("human_check")
        self._ocr_check = get_widget("ocr_check")
        self._init_values()

    def _filter_patterns(self, patterns):
        """Return a subset of patterns to show."""

        check_human = self._human_check.get_active()
        check_ocr = self._ocr_check.get_active()
        def use_pattern(pattern):
            classes = pattern.get_field_list("Classes")
            human = check_human and ("Human" in classes)
            ocr = check_ocr and ("OCR" in classes)
            return bool(human or ocr)
        return filter(use_pattern, patterns)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        _LocalePage._init_signal_handlers(self)
        gaupol.util.connect(self, "_human_check", "toggled")
        gaupol.util.connect(self, "_ocr_check", "toggled")

    def _init_values(self):
        """Initialize default values for widgets."""

        self._human_check.set_active(self.conf.check_human)
        self._ocr_check.set_active(self.conf.check_ocr)

    def _on_human_check_toggled(self, check_button):
        """Populate the tree view with the correct patterns."""

        self.conf.check_human = check_button.get_active()
        self._populate_tree_view()

    def _on_ocr_check_toggled(self, check_button):
        """Populate the tree view with the correct patterns."""

        self.conf.check_ocr = check_button.get_active()
        self._populate_tree_view()

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save_config(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.correct_common_errors(indices, doc, patterns)


class _HearingImpairedPage(_LocalePage):

    """Page for removing hearing impaired parts from subtitles."""

    _glade_basename = "hearing-impaired.glade"

    def _init_attributes(self):
        """Initialize values of page attributes."""

        self._manager = gaupol.PatternManager("hearing-impaired")
        self.conf = gaupol.gtk.conf.hearing_impaired
        self.description = _("Remove explanatory "
            "texts meant for the hearing impaired")
        self.handle = "hearing-impaired"
        self.page_title = _("Select Hearing Impaired Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Remove hearing impaired texts")

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save_config(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.remove_hearing_impaired(indices, doc, patterns)


class _LineBreakPage(_LocalePage):

    """Page for breaking text into lines."""

    _glade_basename = "line-break.glade"

    def _init_attributes(self):
        """Initialize values of page attributes."""

        self._manager = gaupol.PatternManager("line-break")
        self.conf = gaupol.gtk.conf.line_break
        self.description = _("Break text into lines of defined length")
        self.handle = "line-break"
        self.page_title = _("Select Line-Break Patterns")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT
        self.title = _("Break lines")

    @property
    def _max_skip_length(self):
        """Return the maximum line length to skip."""

        if self.conf.skip_length:
            return self.conf.max_skip_length
        return sys.maxint

    @property
    def _max_skip_lines(self):
        """Return the maximum amount of lines to skip."""

        if self.conf.skip_lines:
            return self.conf.max_skip_lines
        return sys.maxint

    def correct_texts(self, project, indices, doc):
        """Correct texts in project."""

        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        self._manager.save_config(*codes)
        patterns = self._manager.get_patterns(*codes)
        project.break_lines(
            indices, doc, patterns,
            gaupol.gtk.ruler.get_length_function(self.conf.length_unit),
            self.conf.max_length, self.conf.max_lines,
            self.conf.max_deviation,
            (self.conf.skip_length or self.conf.skip_lines),
            self._max_skip_length, self._max_skip_lines)


class _LineBreakOptionsPage(_GladePage):

    """Page for editing line-break options."""

    def __init__(self):

        _GladePage.__init__(self, "line-break-options.glade")
        get_widget = self._glade_xml.get_widget
        self._max_length_spin = get_widget("max_length_spin")
        self._max_lines_spin = get_widget("max_lines_spin")
        self._max_skip_length_spin = get_widget("max_skip_length_spin")
        self._max_skip_lines_spin = get_widget("max_skip_lines_spin")
        self._skip_length_check = get_widget("skip_length_check")
        self._skip_lines_check = get_widget("skip_lines_check")
        self._skip_unit_combo = get_widget("skip_unit_combo")
        self._unit_combo = get_widget("unit_combo")

        self.conf = gaupol.gtk.conf.line_break
        self.page_title = _("Set Line-Break Options")
        self.page_type = gtk.ASSISTANT_PAGE_CONTENT

        self._init_unit_combos()
        self._init_signal_handlers()
        self._init_values()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_max_length_spin", "value-changed")
        gaupol.util.connect(self, "_max_lines_spin", "value-changed")
        gaupol.util.connect(self, "_max_skip_length_spin", "value-changed")
        gaupol.util.connect(self, "_max_skip_lines_spin", "value-changed")
        gaupol.util.connect(self, "_skip_length_check", "toggled")
        gaupol.util.connect(self, "_skip_lines_check", "toggled")
        gaupol.util.connect(self, "_skip_unit_combo", "changed")
        gaupol.util.connect(self, "_unit_combo", "changed")

    def _init_unit_combos(self):
        """Initialize the line length unit combo boxes."""

        store = self._unit_combo.get_model()
        for label in (x.label for x in gaupol.gtk.length_units):
            store.append((label,))
        store = self._skip_unit_combo.get_model()
        for label in (x.label for x in gaupol.gtk.length_units):
            store.append((label,))

    def _init_values(self):
        """Initialize default values for widgets."""

        self._max_length_spin.set_value(self.conf.max_length)
        self._max_lines_spin.set_value(self.conf.max_lines)
        self._max_skip_length_spin.set_value(self.conf.max_skip_length)
        self._max_skip_lines_spin.set_value(self.conf.max_skip_lines)
        self._skip_length_check.set_active(self.conf.skip_length)
        self._skip_lines_check.set_active(self.conf.skip_lines)
        self._skip_unit_combo.set_active(self.conf.length_unit)
        self._unit_combo.set_active(self.conf.length_unit)

    def _on_max_length_spin_value_changed(self, spin_button):
        """Save the maximum line length value."""

        self.conf.max_length = spin_button.get_value_as_int()

    def _on_max_lines_spin_value_changed(self, spin_button):
        """Save the maximum line amount value."""

        self.conf.max_lines = spin_button.get_value_as_int()

    def _on_max_skip_length_spin_value_changed(self, spin_button):
        """Save the maximum line length to skip value."""

        self.conf.max_skip_length = spin_button.get_value_as_int()

    def _on_max_skip_lines_spin_value_changed(self, spin_button):
        """Save the maximum line amount to skip value."""

        self.conf.max_skip_lines = spin_button.get_value_as_int()

    def _on_skip_length_check_toggled(self, check_button):
        """Save the skip by line length value."""

        self.conf.skip_length = check_button.get_active()

    def _on_skip_lines_check_toggled(self, check_button):
        """Save the skip by line amount value."""

        self.conf.skip_lines = check_button.get_active()

    def _on_skip_unit_combo_changed(self, combo_box):
        """Save and sync the length unit value."""

        index = combo_box.get_active()
        length_unit = gaupol.gtk.length_units[index]
        self.conf.length_unit = length_unit
        self._unit_combo.set_active(index)

    def _on_unit_combo_changed(self, combo_box):
        """Save and sync the length unit value."""

        index = combo_box.get_active()
        length_unit = gaupol.gtk.length_units[index]
        self.conf.length_unit = length_unit
        self._skip_unit_combo.set_active(index)


class _ProgressPage(_GladePage):

    """Page for showing progress of text corrections."""

    def __init__(self):

        _GladePage.__init__(self, "progress.glade")
        get_widget = self._glade_xml.get_widget
        self._message_label = get_widget("message_label")
        self._progress_bar = get_widget("progress_bar")
        self._status_label = get_widget("status_label")
        self._task_label = get_widget("task_label")

        self._current_task = None
        self._total_tasks = None
        self.page_title = _("Correcting Texts")
        self.page_type = gtk.ASSISTANT_PAGE_PROGRESS
        self._init_values()

    def _init_values(self):
        """Initalize default values for widgets."""

        message = _("Each task is now being run on each project.")
        self._message_label.set_text(message)
        self.reset(100)

    def bump_progress(self, value=1):
        """Bump the current progress by value amount of tasks."""

        self.set_progress(self._current_task + value)

    def reset(self, total, clear_text=False):
        """Set the total amount of tasks to be run."""

        self._current_task = 0
        self._total_tasks = total
        self.set_progress(0, total)
        self.set_project_name("")
        self.set_task_name("")
        if clear_text:
            self._progress_bar.set_text("")
        gaupol.gtk.util.iterate_main()

    def set_progress(self, current, total=None):
        """Set the current task progress status."""

        total = total or self._total_tasks
        fraction = (current / total if total > 0 else 0)
        self._progress_bar.set_fraction(fraction)
        text = _("%(current)d of %(total)d tasks complete")
        self._progress_bar.set_text(text % locals())
        self._current_task = current
        self._total_tasks = total
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


class _ConfirmationPage(_GladePage):

    """Page to confirm changes made after performing all tasks."""

    def __init__(self):

        _GladePage.__init__(self, "confirmation.glade")
        get_widget = self._glade_xml.get_widget
        self._mark_all_button = get_widget("mark_all_button")
        self._preview_button = get_widget("preview_button")
        self._remove_check = get_widget("remove_check")
        self._tree_view = get_widget("tree_view")
        self._unmark_all_button = get_widget("unmark_all_button")

        self.application = None
        self.conf = gaupol.gtk.conf.text_assistant
        self.doc = None
        self.page_title = _("Confirm Changes")
        self.page_type = gtk.ASSISTANT_PAGE_CONFIRM

        self._init_tree_view()
        self._init_signal_handlers()
        self._init_values()

    def _add_text_column(self, index, title):
        """Add a multiline text column to the tree view."""

        renderer = gaupol.gtk.MultilineCellRenderer()
        renderer.set_show_lengths(False)
        renderer.props.editable = (index == 4)
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        renderer.props.font = gaupol.gtk.util.get_font()
        renderer.props.yalign = 0
        column = gtk.TreeViewColumn(title, renderer, text=index)
        column.set_resizable(True)
        column.props.expand = True
        self._tree_view.append_column(column)

    def _can_preview(self):
        """Return True if preview is possible."""

        row = self._get_selected_row()
        if row is None: return False
        page = self._tree_view.get_model()[row][0]
        if page is None: return False
        return all((page.project.video_path, page.project.main_file))

    def _get_selected_row(self):
        """Return the selected row in the tree view or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return None
        return store.get_path(itr)[0]

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_mark_all_button", "clicked")
        gaupol.util.connect(self, "_preview_button", "clicked")
        gaupol.util.connect(self, "_remove_check", "toggled")
        gaupol.util.connect(self, "_unmark_all_button", "clicked")

        selection = self._tree_view.get_selection()
        callback = self._on_tree_view_selection_changed
        selection.connect("changed", callback)

    def _init_tree_view(self):
        """Initialize the tree view."""

        store = gtk.ListStore(object, int, bool, str, str)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback)
        column = gtk.TreeViewColumn(_("Accept"), renderer, active=2)
        column.set_resizable(True)
        self._tree_view.append_column(column)

        self._add_text_column(3, _("Original Text"))
        self._add_text_column(4, _("Corrected Text"))
        column = self._tree_view.get_column(2)
        renderer = column.get_cell_renderers()[0]
        callback = self._on_tree_view_cell_edited
        renderer.connect("edited", callback)

    def _init_values(self):
        """Initialize default values for widgets."""

        self._remove_check.set_active(self.conf.remove_blank)
        self._preview_button.set_sensitive(False)

    def _on_mark_all_button_clicked(self, *args):
        """Set all 'Accept' column values to True."""

        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = True

    def _on_preview_button_clicked(self, *args):
        """Preview the original text in a video player."""

        row = self._get_selected_row()
        page = self._tree_view.get_model()[row][0]
        index = self._tree_view.get_model()[row][1]
        time = page.project.subtitles[index].start_time
        self.application.preview(page, time, self.doc)

    def _on_remove_check_toggled(self, check_button):
        """Save the remove check button value."""

        self.conf.remove_blank = check_button.get_active()

    def _on_tree_view_cell_edited(self, renderer, row, text):
        """Edit the text in the 'Correct Text' column."""

        store = self._tree_view.get_model()
        store[row][4] = unicode(text)

    def _on_tree_view_cell_toggled(self, renderer, row):
        """Toggle the 'Accept' column value."""

        store = self._tree_view.get_model()
        store[row][2] = not store[row][2]

    def _on_tree_view_selection_changed(self, *args):
        """Update the preview button sensitivity."""

        sensitive = self._can_preview()
        self._preview_button.set_sensitive(sensitive)

    def _on_unmark_all_button_clicked(self, *args):
        """Set all 'Accept' column values to False."""

        store = self._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = False

    def get_confirmed_changes(self):
        """Return a sequence of changes marked as accepted."""

        changes = []
        store = self._tree_view.get_model()
        for row in (x for x in store if x[2]):
            page, index, accept, orig, new = row
            changes.append((page, index, orig, new))
        return tuple(changes)

    def populate_tree_view(self, changes):
        """Populate the list of changes to texts."""

        self._tree_view.get_model().clear()
        store = self._tree_view.get_model()
        for page, index, orig, new in changes:
            store.append((page, index, True, orig, new))
        self._tree_view.get_selection().unselect_all()


class TextAssistant(gtk.Assistant):

    """Assistant to guide through multiple text correction tasks."""

    def __init__(self, parent, application):

        gtk.Assistant.__init__(self)
        self._confirmation_page = _ConfirmationPage()
        self._introduction_page = _IntroductionPage()
        self._previous_page = None
        self._progress_page = _ProgressPage()
        self.application = application
        self.conf = gaupol.gtk.conf.text_assistant

        self._init_properties()
        self._init_size()
        self._init_signal_handlers()
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.set_transient_for(parent)

    def _correct_texts(self, assistant_pages):
        """Correct texts by all pages and present changes."""

        changes = []
        target = self._introduction_page.get_target()
        field = self._introduction_page.get_field()
        doc = gaupol.gtk.util.text_field_to_document(field)
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
                orig = project.subtitles[i].get_text(doc)
                new = static_subtitles[i].get_text(doc)
                if orig == new: continue
                changes.append((application_page, i, orig, new))
        self._prepare_confirmation_page(doc, changes)
        index = self.get_current_page()
        self.set_current_page(index + 1)

    def _get_project_copy(self, project):
        """Return a copy of project with some same properties."""

        copy = gaupol.Project(project.framerate)
        copy.main_file = project.main_file
        copy.tran_file = project.tran_file
        copy.subtitles = [x.copy() for x in project.subtitles]
        return copy

    def _init_properties(self):
        """Initialize assistant properties."""

        self.set_border_width(12)
        self.set_title(_("Correct Texts"))
        self.add_page(self._introduction_page)
        self.add_page(_HearingImpairedPage())
        self.add_page(_CommonErrorPage())
        self.add_page(_CapitalizationPage())
        self.application.emit("text-assistant-request-pages", self)
        self.add_pages((_LineBreakPage(), _LineBreakOptionsPage()))
        self.add_page(self._progress_page)
        self.add_page(self._confirmation_page)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, self, "apply")
        gaupol.util.connect(self, self, "cancel")
        gaupol.util.connect(self, self, "close")
        gaupol.util.connect(self, self, "prepare")

    def _init_size(self):
        """Initialize the window size."""

        label = gtk.Label("\n".join(["m" * 54] * 32))
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
        field = self._introduction_page.get_field()
        doc = gaupol.gtk.util.text_field_to_document(field)
        description = _("Correcting texts")
        register = gaupol.registers.DO
        for page in application_pages:
            indices = [x[1] for x in changes if x[0] is page]
            texts = [x[3] for x in changes if x[0] is page]
            if indices and texts:
                page.project.replace_texts(indices, doc, texts)
                page.project.set_action_description(register, description)
                edits += (len(indices))
            edit_indices = set(indices)
            indices = [x for i, x in enumerate(indices) if not texts[i]]
            if indices and self.conf.remove_blank:
                page.project.remove_subtitles(indices)
                page.project.group_actions(register, 2, description)
                removals += len(set(indices))
            page.view.columns_autosize()
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
        title = gaupol.i18n.ngettext(
            "Confirm %d Change",
            "Confirm %d Changes", count) % count
        self.set_page_title(self._confirmation_page, title)
        self._confirmation_page.application = self.application
        self._confirmation_page.doc = doc
        self._confirmation_page.populate_tree_view(changes)
        self.set_page_complete(self._progress_page, True)

    def _prepare_introduction_page(self):
        """Prepare the introduction page content."""

        n = self.get_n_pages()
        pages = [self.get_nth_page(x) for x in range(n)]
        pages.remove(self._introduction_page)
        pages.remove(self._progress_page)
        pages.remove(self._confirmation_page)
        pages = [x for x in pages if hasattr(x, "correct_texts")]
        self._introduction_page.populate_tree_view(pages)

    def _prepare_progress_page(self, pages):
        """Prepare to show the progress page."""

        self._progress_page.reset(0, True)
        self.set_page_complete(self._progress_page, False)
        gaupol.gtk.util.delay_add(10, self._correct_texts, pages)

    def add_page(self, page):
        """Add page and configure its properties."""

        page.show_all()
        self.append_page(page)
        self.set_page_type(page, page.page_type)
        self.set_page_title(page, page.page_title)
        if page.page_type != gtk.ASSISTANT_PAGE_PROGRESS:
            self.set_page_complete(page, True)

    def add_pages(self, pages):
        """Add associated pages and configure their properties.

        The first one of the pages must have a 'correct_texts' attribute.
        The visibilities of other pages are synced with the first page.
        """
        for page in pages:
            self.add_page(page)
        def on_notify_visible(page, prop, pages):
            for page in pages[1:]:
                page.props.visible = pages[0].props.visible
        pages[0].connect("notify::visible", on_notify_visible, pages)
