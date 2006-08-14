# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Changing application and project appearance."""


from gettext import gettext as _
import gtk

from gaupol.gtk          import cons
from gaupol.gtk.icons    import *
from gaupol.gtk.delegate import Delegate, UIMAction
from gaupol.gtk.util     import conf, gtklib
from gaupol.gtk.view     import View


class _ToggleColumnAction(UIMAction):

    """Toggling column visibility."""

    col = None

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        return cls.col in conf.editor.visible_cols

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class ToggleDurationColumnAction(_ToggleColumnAction):

    """Toggling duration column visibility."""

    col = DURN

    toggle_item = (
        'toggle_duration_column',
        None,
        _('_Duration'),
        None,
        _('Change the visibility of the "Duration" column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleEditModeAction(UIMAction):

    """Toggling edit mode."""

    radio_items = (
        (
            (
                'show_times',
                None,
                _('T_imes'),
                'R',
                _('Show positions as times'),
                0
            ), (
                'show_frames',
                None,
                _('F_rames'),
                '<shift>R',
                _('Show positions as frames'),
                1
            )
        ),
        0,
        'on_toggle_edit_mode_activate'
    )

    paths = cons.Mode.uim_paths

    @classmethod
    def get_radio_index(cls):
        """Get active index of radio items."""

        return conf.editor.mode

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return not page is None


class ToggleFramerateAction(UIMAction):

    """Toggling the framerate."""

    menu_item = ('show_framerate_menu', None, _('_Framerate'))

    radio_items = (
        (
            (
                'view_framerate_23_976',
                None,
                _('2_3.976 fps'),
                None,
                _('Calculate unnative units with framerate 23.976 fps'),
                0
            ), (
                'view_framerate_25',
                None,
                _('2_5 fps'),
                None,
                _('Calculate unnative units with framerate 25 fps'),
                1
            ), (
                'view_framerate_29_97',
                None,
                _('2_9.97 fps'),
                None,
                _('Calculate unnative units with framerate 29.97 fps'),
                2
            )
        ),
        0,
        'on_toggle_framerate_activate'
    )

    paths = ['/ui/menubar/view/framerate']
    widgets = ['_framerate_combo']

    @classmethod
    def get_radio_index(cls):
        """Get active index of radio items."""

        return conf.editor.framerate

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.project.main_file is None:
            return False
        return True


class ToggleHideColumnAction(_ToggleColumnAction):

    """Toggling hide column visibility."""

    col = HIDE

    toggle_item = (
        'toggle_hide_column',
        None,
        _('_Hide'),
        None,
        _('Change the visibility of the "Hide" column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleMainTextColumnAction(_ToggleColumnAction):

    """Toggling main text column visibility."""

    col = MTXT

    toggle_item = (
        'toggle_main_text_column',
        None,
        _('_Main Text'),
        None,
        _('Change the visibility of the "Main Text" column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleMainToolbarAction(UIMAction):

    """Toggling main toolbar visibility."""

    toggle_item = (
        'toggle_main_toolbar',
        None,
        _('_Main Toolbar'),
        None,
        _('Toggle the visibility of the main toolbar'),
        'on_toggle_main_toolbar_activate',
        True
    )

    paths = ['/ui/menubar/view/main_toolbar']

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        return conf.application_window.show_main_toolbar

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class ToggleNumberColumnAction(_ToggleColumnAction):

    """Toggling number column visibility."""

    col = NUMB

    toggle_item = (
        'toggle_number_column',
        None,
        _('_No.'),
        None,
        _('Change the visibility of the "No." column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleOutputWindowAction(UIMAction):

    """Toggling output window visibility."""

    toggle_item = (
        'toggle_output_window',
        None,
        _('_Output Window'),
        None,
        _('Toggle the visibility of the output window'),
        'on_toggle_output_window_activate',
        True
    )

    paths = ['/ui/menubar/view/output_window']

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        return conf.output_window.show

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class ToggleShowColumnAction(_ToggleColumnAction):

    """Toggling show column visibility."""

    col = SHOW

    toggle_item = (
        'toggle_show_column',
        None,
        _('_Show'),
        None,
        _('Change the visibility of the "Show" column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleStatusbarAction(UIMAction):

    """Toggling statusbar visibility."""

    toggle_item = (
        'toggle_statusbar',
        None,
        _('_Statusbar'),
        None,
        _('Toggle the visibility of the statusbar'),
        'on_toggle_statusbar_activate',
        True
    )

    paths = ['/ui/menubar/view/statusbar']

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        return conf.application_window.show_statusbar

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class ToggleTranslationTextColumnAction(_ToggleColumnAction):

    """Toggling translation text column visibility."""

    col = TTXT

    toggle_item = (
        'toggle_translation_text_column',
        None,
        _('_Translation Text'),
        None,
        _('Change the visibility of the "Translation Text" column'),
        'on_toggle_column_activate',
        True
    )

    paths = [cons.Column.uim_paths[col]]


class ToggleVideoToolbarAction(UIMAction):

    """Toggling video toolbar visibility."""

    toggle_item = (
        'toggle_video_toolbar',
        None,
        _('_Video Toolbar'),
        None,
        _('Toggle the visibility of the video toolbar'),
        'on_toggle_video_toolbar_activate',
        True
    )

    paths = ['/ui/menubar/view/video_toolbar']

    @classmethod
    def get_toggle_value(cls):
        """Get value of toggle item."""

        return conf.application_window.show_video_toolbar

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return True


class ShowColumnsMenuAction(UIMAction):

    """Toggling column visibilities."""

    menu_item = ('show_columns_menu', None, _('_Columns'))
    paths = ['/ui/menubar/view/columns']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class ViewDelegate(Delegate):

    """Changing application and project appearance."""

    def on_framerate_combo_changed(self, *args):
        """Change framerate."""

        page = self.get_current_page()
        framerate = self._framerate_combo.get_active()
        if framerate == page.project.framerate:
            return

        gtklib.set_cursor_busy(self._window)
        page.project.change_framerate(framerate)
        conf.editor.framerate = framerate
        path = cons.Framerate.uim_paths[framerate]
        self._uim.get_widget(path).set_active(True)
        if page.edit_mode != page.project.main_file.mode:
            page.reload_columns([SHOW, HIDE, DURN])
        gtklib.set_cursor_normal(self._window)

    def on_output_window_closed(self, *args):
        """Close output window."""

        self._uim.get_action('/ui/menubar/view/output_window').activate()

    def on_toggle_column_activate(self, action):
        """Toggle the visibility of a column."""

        page = self.get_current_page()
        col = cons.Column.uim_action_names.index(action.get_name())
        column = page.view.get_column(col)
        visible = column.get_visible()
        path = cons.Column.uim_paths[col]
        active = self._uim.get_action(path).get_active()
        if active is visible:
            return

        gtklib.set_cursor_busy(self._window)
        column.set_visible(not visible)
        visible_columns = []
        for i in range(6):
            if page.view.get_column(i).get_visible():
                visible_columns.append(i)
        conf.editor.visible_cols = visible_columns
        self.set_sensitivities(page)
        self.set_character_status(page)
        gtklib.set_cursor_normal(self._window)

    def on_toggle_edit_mode_activate(self, unknown, action):
        """Toggle edit mode."""

        page = self.get_current_page()
        edit_mode = cons.Mode.uim_action_names.index(action.get_name())
        if edit_mode == page.edit_mode:
            return

        gtklib.set_cursor_busy(self._window)
        page.edit_mode = edit_mode
        conf.editor.mode = edit_mode

        has_focus = page.view.props.has_focus
        focus_row, focus_col = page.view.get_focus()
        selected_rows = page.view.get_selected_rows()

        scrolled_window = page.view.get_parent()
        scrolled_window.remove(page.view)
        old_view = page.view
        page.view = View(edit_mode)
        gtklib.destroy_gobject(old_view)
        self.connect_view_signals(page)
        scrolled_window.add(page.view)
        scrolled_window.show_all()
        page.reload_all()
        page.view.columns_autosize()

        try:
            page.view.set_focus(focus_row, focus_col)
        except TypeError:
            pass
        page.view.select_rows(selected_rows)
        try:
            page.view.scroll_to_row(focus_row)
        except TypeError:
            pass
        page.view.props.has_focus = has_focus
        gtklib.set_cursor_normal(self._window)

    def on_toggle_framerate_activate(self, unknown, action):
        """Toggle framerate."""

        page = self.get_current_page()
        framerate = cons.Framerate.uim_action_names.index(action.get_name())
        if framerate == page.project.framerate:
            return

        gtklib.set_cursor_busy(self._window)
        page.project.change_framerate(framerate)
        conf.editor.framerate = framerate
        self._framerate_combo.set_active(framerate)
        if page.edit_mode != page.project.main_file.mode:
            page.reload_columns([SHOW, HIDE, DURN])
        gtklib.set_cursor_normal(self._window)

    def on_toggle_main_toolbar_activate(self, *args):
        """Toggle main toolbar visibility."""

        toolbar = self._uim.get_widget('/ui/main_toolbar')
        visible = toolbar.props.visible
        toolbar.props.visible = not visible
        conf.application_window.show_main_toolbar = not visible

    def on_toggle_output_window_activate(self, *args):
        """Toggle output window visibility."""

        visible = self._output_window.get_visible()
        if visible:
            self._output_window.hide()
        else:
            self._output_window.show()
        conf.output_window.show = not visible

    def on_toggle_statusbar_activate(self, *args):
        """Toggle statusbar visibility."""

        hbox = gtklib.get_parent_widget(self._msg_statusbar, gtk.HBox)
        visible = hbox.props.visible
        hbox.props.visible = not visible
        conf.application_window.show_statusbar = not visible

    def on_toggle_video_toolbar_activate(self, *args):
        """Toggle video toolbar visibility."""

        toolbar = gtklib.get_parent_widget(self._video_button, gtk.Toolbar)
        visible = toolbar.props.visible
        toolbar.props.visible = not visible
        conf.application_window.show_video_toolbar = not visible

    def on_view_header_button_press_event(self, button, event):
        """Display column pop-up menu."""

        if event.button == 3:
            menu = self._uim.get_widget('/ui/view_header')
            menu.popup(None, None, None, event.button, event.time)
