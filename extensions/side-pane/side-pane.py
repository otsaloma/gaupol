# Copyright (C) 2008 Osmo Salomaa
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

"""A side pane that can be used by other extensions."""

import gaupol.gtk
import gtk
import os
_ = gaupol.i18n._


class SidePane(gaupol.Observable):

    """A side pane object for the main window.

    The side pane is installed as an attribute to gaupol.gtk.Application and
    thus accessible to extensions as application.side_pane.

    Signals (arguments):
     * close-button-clicked (side_pane)
     * page-switched (side_pane, new_page)
    """

    # Parts of the code dealing with the header's toggle button and the menu
    # associated with it have been adapted from Nautilus, file
    # 'nautilus-side-pane.c' with the following copyright statement and info.
    # Copyright (C) 2002 Ximian Inc.
    # Author: Dave Camp <dave@ximian.com>

    _signals = ("close-button-clicked", "page-switched")

    def __init__(self, application):

        gaupol.Observable.__init__(self)
        self._conf = gaupol.gtk.conf.extensions.side_pane
        self._label = gtk.Label(_("(Empty)"))
        self._notebook = gtk.Notebook()
        self._paned = gtk.HPaned()
        self._toggle_button = gtk.ToggleButton()
        self.application = application
        self._init_gui()

    def _init_gui(self):
        """Initialize all user interface widgets."""

        side_vbox = gtk.VBox()
        self._init_paned(side_vbox)
        self._init_header(side_vbox)
        self._init_notebook(side_vbox)
        self._paned.show_all()
        child = self._paned.get_child1()
        child.props.visible = self._conf.visible

    def _init_header(self, side_vbox):
        """Initialize the side pane header."""

        header_hbox = gtk.HBox(False, 12)
        header_hbox.set_border_width(1)
        self._toggle_button.set_relief(gtk.RELIEF_NONE)
        self._toggle_button.set_focus_on_click(False)
        toggle_button_hbox = gtk.HBox(False, 6)
        toggle_button_hbox.pack_start(self._label)
        arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_NONE)
        toggle_button_hbox.pack_start(arrow)
        self._toggle_button.add(toggle_button_hbox)
        callback = self._on_header_toggle_button_button_press_event
        self._toggle_button.connect("button-press-event", callback)
        callback = self._on_header_toggle_button_key_press_event
        self._toggle_button.connect("key-press-event", callback)
        header_hbox.pack_start(self._toggle_button, False, False)
        header_hbox.pack_start(gtk.Alignment(), True, True)
        close_button = gtk.Button()
        args = (gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        image = gtk.image_new_from_stock(*args)
        close_button.add(image)
        close_button.set_relief(gtk.RELIEF_NONE)
        close_button.set_focus_on_click(False)
        callback = self._on_header_close_button_clicked
        close_button.connect("clicked", callback)
        header_hbox.pack_start(close_button, False, False)
        side_vbox.pack_start(header_hbox, False, False)

    def _init_notebook(self, side_vbox):
        """Initialize the side pane notebook."""

        self._notebook.set_show_border(False)
        self._notebook.set_show_tabs(False)
        side_vbox.pack_start(self._notebook, True, True)

    def _init_paned(self, side_vbox):
        """Initialize the horizontal pane container."""

        main_vbox = self.application.window.get_children()[0]
        main_notebook = main_vbox.get_children()[2]
        self._paned.pack1(side_vbox, False, False)
        main_notebook_vbox = gtk.VBox()
        main_notebook.reparent(main_notebook_vbox)
        self._paned.pack2(main_notebook_vbox, True, False)
        main_vbox.pack_start(self._paned)
        main_vbox.reorder_child(self._paned, 2)
        self._paned.set_position(self._conf.width)

    def _on_header_close_button_clicked(self, button):
        """Hide the side pane from the main window."""

        self.hide()
        self.emit("close-button-clicked")

    def _on_header_menu_deactivate(self, menu):
        """Set the header toggle button back to inactive."""

        self._toggle_button.set_active(False)
        menu.destroy()

    def _on_header_menu_item_activate(self, menu_item):
        """Set the currently active page to correspond to menu_item."""

        child = menu_item.get_data("child")
        self.set_current_page(child)
        self._toggle_button.set_active(False)
        parent = menu_item.get_parent()
        while not isinstance(parent, gtk.Menu):
            parent = parent.get_parent()
        parent.destroy()
        self.emit("page-switched", child)

    def _on_header_toggle_button_button_press_event(self, button, event):
        """Show a menu listing all side pane pages."""

        if event.button != 1: return False
        self._show_header_menu(event)
        return True

    def _on_header_toggle_button_key_press_event(self, key, event):
        """Show a menu listing all side pane pages."""

        spaces = (gtk.keysyms.space, gtk.keysyms.KP_Space)
        enters = (gtk.keysyms.Return, gtk.keysyms.KP_Enter)
        if not event.keyval in (spaces + enters): return False
        self._show_header_menu(event)
        return True

    def _position_header_menu(self, menu):
        """Return x-coordinate, y-coordinate and boolean push value."""

        x, y, = self._toggle_button.window.get_origin()
        allocation = self._toggle_button.get_allocation()
        x += allocation.x
        y += allocation.y + allocation.height
        return x, y, True

    def _show_header_menu(self, event):
        """Show a menu listing all side pane pages."""

        menu = gtk.Menu()
        for i in range(self._notebook.get_n_pages()):
            child = self._notebook.get_nth_page(i)
            title = self._notebook.get_tab_label_text(child)
            menu_item = gtk.MenuItem(title, False)
            menu_item.set_data("child", child)
            callback = self._on_header_menu_item_activate
            menu_item.connect("activate", callback)
            menu.append(menu_item)
        menu.show_all()
        self._toggle_button.set_active(True)
        function = self._position_header_menu
        menu.popup(None, None, function, 1, event.time)

    def add_page(self, child, name, title):
        """Add child as a page to the side pane.

        name should be a unique string and is used internally for saving the
        active page name to the configuration file. Using the extension's
        module name is a good idea since that should be unique anyway, or if
        having multiple side pane pages per extension, then a name prefixed
        with the module name. title is a translated string shown to the user.
        """
        child.set_data("side_pane_extension_name", name)
        self._notebook.append_page(child)
        self._notebook.set_tab_label_text(child, title)
        if self._notebook.get_n_pages() == 1:
            self.set_current_page(child)
        elif name == self._conf.page:
            self.set_current_page(child)

    def get_current_page(self):
        """Return the child widget of the currently active page or None."""

        if self._notebook.get_n_pages() == 0: return None
        page_num = self._notebook.get_current_page()
        return self._notebook.get_nth_page(page_num)

    def hide(self):
        """Hide the side pane from the main window."""

        self._paned.get_child1().hide()

    def remove(self):
        """Remove the entire side pane from the application window."""

        self._conf.width = self._paned.get_position()
        child = self.get_current_page()
        if child is not None:
            self._conf.page = child.get_data("side_pane_extension_name")
        child = self._paned.get_child1()
        self._conf.visible = child.props.visible
        main_vbox = self.application.window.get_children()[0]
        main_notebook = self._paned.get_child2().get_children()[0]
        main_vbox.remove(self._paned)
        main_notebook.reparent(main_vbox)
        main_vbox.reorder_child(main_notebook, 2)
        self._paned.destroy()

    def remove_page(self, child):
        """Remove child page from the side pane."""

        page_num = self._notebook.page_num(child)
        self._notebook.remove_page(page_num)

    def set_current_page(self, child):
        """Set the currently active page to child widget."""

        page_num = self._notebook.page_num(child)
        self._notebook.set_current_page(page_num)
        title = self._notebook.get_tab_label_text(child)
        self._label.set_text(title)

    def show(self):
        """Show the side pane in the main window."""

        self._paned.get_child1().show()


class SidePaneExtension(gaupol.gtk.Extension):

    """A side pane that can be used by other extensions."""

    def __init__(self):
        """Initialize a SidePaneExtension object."""

        self._action_group = None
        self._conf = None
        self._uim_id = None
        self.application = None

    def _on_side_pane_close_button_clicked(self, side_pane):
        """Update the state of the corresponding menu item."""

        path = "/ui/menubar/view/1/side_pane"
        action = self.application.uim.get_action(path)
        action.set_active(False)

    def _on_toggle_side_pane_toggled(self, *args):
        """Show or hide the side pane."""

        if not self._conf.visible:
            self.application.side_pane.show()
        else: # Is visible.
            self.application.side_pane.hide()
        self._conf.visible = not self._conf.visible

    def setup(self, application):
        """Setup extension for use with application."""

        directory = os.path.dirname(__file__)
        spec_file = os.path.join(directory, "side-pane.conf.spec")
        self.read_config(spec_file)
        application.side_pane = SidePane(application)
        self._conf = gaupol.gtk.conf.extensions.side_pane
        self._action_group = gtk.ActionGroup("side-pane")
        self._action_group.add_toggle_actions((
            ("toggle_side_pane", None, "Si_de Pane",
             None, _("Show or hide the side pane"),
             self._on_toggle_side_pane_toggled, self._conf.visible),))
        application.uim.insert_action_group(self._action_group, -1)
        ui_file = os.path.join(directory, "side-pane.ui.xml")
        self._uim_id = application.uim.add_ui_from_file(ui_file)
        callback = self._on_side_pane_close_button_clicked
        application.side_pane.connect("close-button-clicked", callback)
        application.uim.ensure_update()
        application.set_menu_notify_events("side-pane")
        self.application = application

    def teardown(self, application):
        """End use of extension with application."""

        application.side_pane.remove()
        del application.side_pane
        self.application.uim.remove_ui(self._uim_id)
        self.application.uim.remove_action_group(self._action_group)
        self.application.uim.ensure_update()
