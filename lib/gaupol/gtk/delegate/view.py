# Copyright (C) 2005 Osmo Salomaa
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


"""Altering application and project appearance."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import gtk

from gaupol.gtk.cons import *
from gaupol.gtk.colcons import *
from gaupol.gtk.delegates    import Delegate, UIMAction
from gaupol.gtk.util         import config, gtklib
from gaupol.gtk.view         import View


class ToggleColumnActionMenu(UIMAction):

    """Toggling the visibility of a column."""

    uim_menu_item = (
        'show_columns_menu',
        None,
        _('_Columns')
    )

    uim_paths = ['/ui/menubar/view/columns']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class ToggleColumnAction(UIMAction):

    """Toggling the visibility of a column."""

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""

        return cls.col in config.Editor.visible_cols

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class ToggleColumnNoAction(ToggleColumnAction):

    col = NUMB

    uim_toggle_item = (
        'toggle_number_column',
        None,
        _('_No.'),
        None,
        _('Change the visibility of the "No." column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleColumnShowAction(ToggleColumnAction):

    col = SHOW

    uim_toggle_item = (
        'toggle_show_column',
        None,
        _('_Show'),
        None,
        _('Change the visibility of the "Show" column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleColumnHideAction(ToggleColumnAction):

    col = HIDE

    uim_toggle_item = (
        'toggle_hide_column',
        None,
        _('_Hide'),
        None,
        _('Change the visibility of the "Hide" column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleColumnDurationAction(ToggleColumnAction):

    col = DURN

    uim_toggle_item = (
        'toggle_duration_column',
        None,
        _('_Duration'),
        None,
        _('Change the visibility of the "Duration" column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleColumnMainTextAction(ToggleColumnAction):

    col = MTXT

    uim_toggle_item = (
        'toggle_main_text_column',
        None,
        _('_Main Text'),
        None,
        _('Change the visibility of the "Main Text" column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleColumnTranslationTextAction(ToggleColumnAction):

    col = TTXT

    uim_toggle_item = (
        'toggle_tran_text_column',
        None,
        _('_Translation Text'),
        None,
        _('Change the visibility of the "Translation Text" column'),
        'on_toggle_column_activated',
        1
    )

    uim_paths = [Column.uim_paths[col]]


class ToggleEditModeAction(UIMAction):

    """Toggling the edit mode."""

    uim_radio_items = (
        (
            (
                'show_times',
                None,
                _('T_imes'),
                '<control>M',
                _('Use time units'),
                0
            ), (
                'show_frames',
                None,
                _('F_rames'),
                '<control>R',
                _('Use frame units'),
                1
            )
        ),
        0,
        'on_toggle_edit_mode_activated'
    )

    uim_paths = ['/ui/menubar/view/times', '/ui/menubar/view/frames']

    @classmethod
    def get_uim_radio_items_index(cls):
        """Return the active index of the UI manager radio items."""

        return config.Editor.mode

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return not page is None


class ToggleFramerateAction(UIMAction):

    """Toggling the framerate."""

    uim_menu_item = (
        'show_framerate_menu',
        None,
        _('_Framerate')
    )

    uim_radio_items = (
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
        'on_toggle_framerate_activated'
    )

    uim_paths = ['/ui/menubar/view/framerate']
    widgets   = ['framerate_combo']

    @classmethod
    def get_uim_radio_items_index(cls):
        """Return the active index of the UI manager radio items."""

        return config.Editor.framerate

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False
        elif page.project.main_file is None:
            return False
        else:
            return True


class ToggleMainToolbarAction(UIMAction):

    """Toggling the visibility of the main toolbar."""

    uim_toggle_item = (
        'toggle_main_toolbar',
        None,
        _('_Main Toolbar'),
        None,
        _('Toggle the visibility of the main toolbar'),
        'on_toggle_main_toolbar_activated',
        True
    )

    uim_paths = ['/ui/menubar/view/main_toolbar']

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""

        return config.AppWindow.show_main_toolbar

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class ToggleOutputWindowAction(UIMAction):

    """Toggling the visibility of the output window."""

    uim_toggle_item = (
        'toggle_output_window',
        None,
        _('_Output Window'),
        '<control><alt>O',
        _('Toggle the visibility of the output window'),
        'on_toggle_output_window_activated',
        True
    )

    uim_paths = ['/ui/menubar/view/output_window']

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""

        return config.OutputWindow.show

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class ToggleStatusbarAction(UIMAction):

    """Toggling the visibility of the statusbar."""

    uim_toggle_item = (
        'toggle_statusbar',
        None,
        _('_Statusbar'),
        None,
        _('Toggle the visibility of the statusbar'),
        'on_toggle_statusbar_activated',
        True
    )

    uim_paths = ['/ui/menubar/view/statusbar']

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""

        return config.AppWindow.show_statusbar

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class ToggleVideoToolbarAction(UIMAction):

    """Toggling the visibility of the video toolbar."""

    uim_toggle_item = (
        'toggle_video_toolbar',
        None,
        _('_Video Toolbar'),
        None,
        _('Toggle the visibility of the video toolbar'),
        'on_toggle_video_toolbar_activated',
        True
    )

    uim_paths = ['/ui/menubar/view/video_toolbar']

    @classmethod
    def get_uim_toggle_item_value(cls):
        """Return value of the UI manager toggle item."""

        return config.AppWindow.show_video_toolbar

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class ViewDelegate(Delegate):

    """Altering application and project appearance."""

    def on_framerate_changed(self, *args):
        """
        Change framerate.

        This method is called from the framerate combo box.
        """
        page = self.get_current_page()
        framerate = self.framerate_combo.get_active()

        # Return if only refreshing widget state.
        if framerate == page.project.framerate:
            return

        gtklib.set_cursor_busy(self.window)

        page.project.change_framerate(framerate)
        config.Editor.framerate = framerate

        path = Framerate.uim_paths[framerate]
        self.uim.get_widget(path).set_active(True)

        if page.edit_mode != page.project.main_file.mode:
            page.reload_columns([SHOW, HIDE, DURN])

        gtklib.set_cursor_normal(self.window)

    def on_output_window_close(self, *args):
        """Synchronize output window visibility menu item."""

        path = '/ui/menubar/view/output_window'
        self.uim.get_action(path).activate()

    def on_toggle_column_activated(self, action):
        """Toggle the visibility of a column."""

        page = self.get_current_page()

        col = [
            'toggle_number_column',
            'toggle_show_column',
            'toggle_hide_column',
            'toggle_duration_column',
            'toggle_main_text_column',
            'toggle_tran_text_column'
        ].index(action.get_name())

        tree_view_column = page.view.get_column(col)
        visible = tree_view_column.get_visible()

        path = Column.uim_paths[col]
        action = self.uim.get_action(path)
        active = action.get_active()

        # Return if only refreshing widget state.
        if active is visible:
            return

        gtklib.set_cursor_busy(self.window)
        tree_view_column.set_visible(not visible)
        visible_columns = []

        for i in range(6):
            if page.view.get_column(i).get_visible():
                visible_columns.append(i)

        config.Editor.visible_cols = visible_columns
        self.set_sensitivities(page)
        self.set_character_status(page)
        gtklib.set_cursor_normal(self.window)

    def on_toggle_edit_mode_activated(self, unknown, action):
        """Toggle the edit mode."""

        page = self.get_current_page()
        if action.get_name() == 'show_times':
            edit_mode = Mode.TIME
        elif action.get_name() == 'show_frames':
            edit_mode = Mode.FRAME

        # Return if only refreshing widget state.
        if edit_mode == page.edit_mode:
            return

        gtklib.set_cursor_busy(self.window)
        page.edit_mode = edit_mode
        config.Editor.mode = edit_mode

        # Get properties.
        has_focus = page.view.props.has_focus
        focus_row, focus_col = page.view.get_focus()
        selected_rows = page.view.get_selected_rows()

        # Remove view.
        scrolled_window = page.view.get_parent()
        scrolled_window.remove(page.view)

        # Create a new view. This could alternatively be done with
        # gtk.TreeView.remove_column() and gtk.TreeView.insert_column(), but
        # rebuilding the entire view is not much slower.
        old_view = page.view
        page.view = View(edit_mode)
        gtklib.destroy_gobject(old_view)
        self.connect_view_signals(page)

        # Add view.
        scrolled_window.add(page.view)
        scrolled_window.show_all()
        page.reload_all()
        page.view.columns_autosize()

        # Restore properties.
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
        gtklib.set_cursor_normal(self.window)

    def on_toggle_framerate_activated(self, unknown, action):
        """
        Toggle the framerate.

        This method is called from the menu.
        """
        page = self.get_current_page()
        name = action.get_name()
        if name == 'view_framerate_23_976':
            framerate = Framerate.FR_23_976
        elif name == 'view_framerate_25':
            framerate = Framerate.FR_25
        elif name == 'view_framerate_29_97':
            framerate = Framerate.FR_29_97

        # Return if only refreshing widget state.
        if framerate == page.project.framerate:
            return

        gtklib.set_cursor_busy(self.window)

        page.project.change_framerate(framerate)
        config.Editor.framerate = framerate
        self.framerate_combo.set_active(framerate)

        if page.edit_mode != page.project.main_file.mode:
            page.reload_columns([SHOW, HIDE, DURN])
        gtklib.set_cursor_normal(self.window)

    def on_toggle_main_toolbar_activated(self, *args):
        """Toggle the visibility of the main toolbar."""

        toolbar = self.uim.get_widget('/ui/main_toolbar')
        visible = toolbar.props.visible

        toolbar.props.visible = not visible
        config.AppWindow.show_main_toolbar = not visible

    def on_toggle_output_window_activated(self, *args):
        """Toggle the visibility of the video player output window."""

        visible = self.output_window.get_visible()

        if visible:
            self.output_window.hide()
        else:
            self.output_window.show()
        config.OutputWindow.show = not visible

    def on_toggle_statusbar_activated(self, *args):
        """Toggle the visibility of the statusbar."""

        hbox = gtklib.get_parent_widget(self.msg_statusbar, gtk.HBox)
        visible = hbox.props.visible

        hbox.props.visible = not visible
        config.AppWindow.show_statusbar = not visible

    def on_toggle_video_toolbar_activated(self, *args):
        """Toggle the visibility of the video toolbar."""

        toolbar = gtklib.get_parent_widget(self.video_button, gtk.Toolbar)
        visible = toolbar.props.visible

        toolbar.props.visible = not visible
        config.AppWindow.show_video_toolbar = not visible

    def on_view_headers_clicked(self, button, event):
        """Show a popup menu when the view header is right-clicked."""

        if event.button == 3:
            menu = self.uim.get_widget('/ui/view_header')
            menu.popup(None, None, None, event.button, event.time)


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestViewDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])

        def destroy(self):

            self.application.window.destroy()

        def test_actions(self):

            uim = self.application.uim

            action = uim.get_action('/ui/menubar/view/columns/show')
            self.application.on_toggle_column_activated(action)
            self.application.on_toggle_column_activated(action)

            action = uim.get_action('/ui/menubar/view/times')
            self.application.on_toggle_edit_mode_activated(None, action)
            self.application.on_toggle_edit_mode_activated(None, action)

            self.application.on_framerate_changed()
            action = uim.get_action('/ui/menubar/view/framerate/23_976')
            self.application.on_toggle_framerate_activated(None, action)
            self.application.on_toggle_framerate_activated(None, action)

            self.application.on_toggle_main_toolbar_activated()
            self.application.on_toggle_main_toolbar_activated()

            self.application.on_toggle_output_window_activated()
            self.application.on_toggle_output_window_activated()

            if self.application.output_window.get_visible():
                self.application.on_output_window_close()
            else:
                self.application.on_toggle_output_window_activated()
                self.application.on_output_window_close()

            self.application.on_toggle_statusbar_activated()
            self.application.on_toggle_statusbar_activated()

            self.application.on_toggle_video_toolbar_activated()
            self.application.on_toggle_video_toolbar_activated()

    TestViewDelegate().run()
