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

"""Cell renderer for multiline text data."""

import aeidon
import difflib
import gaupol
import re

from aeidon.i18n import _
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("MultilineCellRenderer", "MultilineDiffCellRenderer")


class CellTextView(Gtk.TextView, Gtk.CellEditable):

    """A :class:`Gtk.TextView` suitable for cell renderer use."""

    __gproperties__ = {
        "editing-canceled": (bool,
                             "Editing canceled",
                             "Editing canceled",
                             False,
                             GObject.ParamFlags.READWRITE),

    }
    __gtype_name__ = "CellTextView"

    def __init__(self, text_buffer=None):
        """Initialize a :class:`CellTextView` instance."""
        GObject.GObject.__init__(self)
        gaupol.util.prepare_text_view(self)
        aeidon.util.connect(self, self, "key-press-event")
        aeidon.util.connect(self, self, "populate-popup")

    def do_editing_done(self, *args):
        """End editing."""
        pass

    def do_remove_widget(self, *args):
        """Remove widget."""
        pass

    def do_start_editing(self, *args):
        """Start editing."""
        # Don't let anyone else handle button-press-events
        # that happen within the text view.
        self.connect_after("button-press-event", lambda *args: True)

    def get_text(self):
        """Return text."""
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _on_key_press_event(self, text_view, event):
        """Toggle italicization if Control+I pressed."""
        if (event.get_state() & Gdk.ModifierType.CONTROL_MASK and
            event.keyval in (Gdk.KEY_i, Gdk.KEY_I)):
            self._on_toggle_italic()
            return True
        return False

    def _on_populate_popup(self, text_view, popup):
        """Add a context menu item to toggle italicization."""
        if not isinstance(popup, Gtk.Menu): return
        item = Gtk.MenuItem(label=_("Italic"))
        item.connect("activate", self._on_toggle_italic)
        child = item.get_child()
        if isinstance(child, Gtk.AccelLabel):
            child.set_accel(Gdk.KEY_i, Gdk.ModifierType.CONTROL_MASK)
        item.show_all()
        popup.append(item)

    def _on_toggle_italic(self, *args):
        """Add or remove italic tags around selection."""
        if not getattr(gaupol, "italic_tag", None): return
        if not getattr(gaupol, "italicize", None): return
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, False)
        bounds = text_buffer.get_selection_bounds()
        if not bounds:
            # If no selection, replicate cursor position.
            cursor = text_buffer.get_insert()
            cursor = text_buffer.get_iter_at_mark(cursor)
            bounds = (cursor, cursor)
        a, b = [x.get_offset() for x in bounds]
        # Strip possible existing italic tags around selection.
        # If none found, then selection should be italicized.
        text1 = re.sub(gaupol.italic_tag.pattern + r"\Z", "", text[:a])
        text2 = re.sub(gaupol.italic_tag.pattern, "", text[a:b])
        text3 = re.sub(r"\A" + gaupol.italic_tag.pattern, "", text[b:])
        if text1 + text2 + text3 == text:
            text2 = gaupol.italicize(text2)
            match = gaupol.italic_tag.match(text2)
            a += match.end() - match.start()
            b += match.end() - match.start()
        else:
            a = len(text1)
            b = len(text1) + len(text2)
        text_buffer.set_text(text1 + text2 + text3)
        ins = text_buffer.get_iter_at_offset(a)
        bound = text_buffer.get_iter_at_offset(b)
        text_buffer.select_range(ins, bound)

    def set_text(self, text):
        """Set text."""
        self.get_buffer().set_text(text)


class MultilineCellRenderer(Gtk.CellRendererText):

    """
    Cell renderer for multiline text data.

    If :attr:`gaupol.conf.editor.show_lengths_cell` is ``True``, line lengths
    are shown at the end of each line.
    """

    __gtype_name__ = "MultilineCellRenderer"

    def __init__(self):
        """Initialize a :class:`MultilineCellRenderer` instance."""
        GObject.GObject.__init__(self)
        self._in_editor_menu = False
        self._show_lengths = gaupol.conf.editor.show_lengths_cell
        self._text = ""
        gaupol.conf.connect_notify("editor", "show_lengths_cell", self)
        aeidon.util.connect(self, self, "notify::text")

    def do_start_editing(self, event, widget, path, bg_area, cell_area, flags):
        """Initialize and return a :class:`CellTextView` widget."""
        editor = CellTextView()
        gaupol.style.use_font(editor, "custom")
        editor.set_text(self._text)
        editor.set_size_request(cell_area.width, cell_area.height)
        editor.set_left_margin(self.props.xpad)
        editor.set_right_margin(self.props.xpad)
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK 3.18.
            editor.set_top_margin(self.props.ypad)
            editor.set_bottom_margin(self.props.ypad)
        editor.gaupol_path = path
        editor.connect("focus-out-event", self._on_editor_focus_out_event)
        editor.connect("key-press-event", self._on_editor_key_press_event)
        editor.connect("populate-popup",  self._on_editor_populate_popup)
        editor.show()
        return editor

    def _on_conf_editor_notify_show_lengths_cell(self, *args):
        """Hide or show line lengths if ``conf`` changed."""
        self._show_lengths = gaupol.conf.editor.show_lengths_cell

    def _on_editor_focus_out_event(self, editor, *args):
        """End editing."""
        if self._in_editor_menu: return
        editor.remove_widget()
        self.emit("editing-canceled")

    def _on_editor_key_press_event(self, editor, event):
        """End editing if ``Enter`` or ``Escape`` pressed."""
        if (event.get_state() &
            (Gdk.ModifierType.SHIFT_MASK |
             Gdk.ModifierType.CONTROL_MASK)): return
        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            editor.editing_done()
            editor.remove_widget()
            self.emit("edited", editor.gaupol_path, editor.get_text())
            return True
        if event.keyval == Gdk.KEY_Escape:
            editor.editing_done()
            editor.remove_widget()
            self.emit("editing-canceled")
            return True

    def _on_editor_populate_popup(self, editor, menu):
        """Disable "focus-out-event" ending editing."""
        self._in_editor_menu = True
        def on_menu_unmap(menu, self):
            self._in_editor_menu = False
        menu.connect("unmap", on_menu_unmap, self)

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""
        # Since GTK 3.6, the notify::text signal seems to get
        # emitted insanely often even if text hasn't changed at
        # all. Let's try to keep this callback as fast as possible.
        self._text = self.props.text
        self.props.markup = self._text_to_markup(self.props.text,
                                                 self._show_lengths,
                                                 gaupol.conf.editor.length_unit)

    def set_show_lengths(self, show_lengths):
        """Show or hide line lengths, overriding ``conf``."""
        self._show_lengths = show_lengths
        gaupol.conf.disconnect_notify("editor", "show_lengths_cell", self)

    @aeidon.deco.memoize(1000)
    def _text_to_markup(self, text, show_lengths, length_unit):
        """Return `text` rendered as markup for display."""
        # We don't actually use the length_unit argument,
        # but do need it accounted for in memoized values.
        if not text: return ""
        text = GLib.markup_escape_text(text)
        if not show_lengths: return text
        lines = text.split("\n")
        lengths = gaupol.ruler.get_lengths(text)
        return "\n".join(("{} <small>[{:d}]</small>"
                          .format(lines[i], lengths[i])
                          if lines[i] else lines[i]
                          for i in range(len(lines))))


class MultilineDiffCellRenderer(MultilineCellRenderer):

    """Cell renderer for multiline diffed text data."""

    __gtype_name__ = "MultilineDiffCellRenderer"

    ref_text = GObject.Property(type=str, default="")
    ref_type = GObject.Property(type=int, default=-1)

    COLOR_CHANGE = gaupol.conf.general.diff_color_change
    COLOR_DELETE = gaupol.conf.general.diff_color_delete
    COLOR_INSERT = gaupol.conf.general.diff_color_insert

    def __init__(self):
        """Initialize a :class:`MultilineDiffCellRenderer` instance."""
        MultilineCellRenderer.__init__(self)
        self._ref_text = ""

    def _add_diff_markup(self, a, b):
        """Return `a` with markup for parts different from `b`."""
        matcher = difflib.SequenceMatcher(a=a, b=b)
        ops = matcher.get_opcodes()
        return "".join(self._highlight(a[i1:i2], tag)
                       for tag, i1, i2, j1, j2 in ops)

    def _get_diff_color(self, tag):
        """Return color to use to highlight changes of type `tag`."""
        if tag == "insert" and self.props.ref_type > 0: return self.COLOR_INSERT
        if tag == "insert" and self.props.ref_type < 0: return self.COLOR_DELETE
        if tag == "delete" and self.props.ref_type > 0: return self.COLOR_DELETE
        if tag == "delete" and self.props.ref_type < 0: return self.COLOR_INSERT
        return self.COLOR_CHANGE

    def _highlight(self, text, tag):
        """Return `text` as markup highlighting changes of type `tag`."""
        if tag == "equal": return text
        color = self._get_diff_color(tag)
        return '<span background="{}">{}</span>'.format(color, text)

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""
        # Since GTK 3.6, the notify::text signal seems to get
        # emitted insanely often even if text hasn't changed at
        # all. Let's try to keep this callback as fast as possible.
        self._text = self.props.text
        self._ref_text = self.props.ref_text
        self.props.markup = self._text_to_markup(self.props.text,
                                                 self.props.ref_text,
                                                 self._show_lengths,
                                                 gaupol.conf.editor.length_unit)

    @aeidon.deco.memoize(1000)
    def _text_to_markup(self, text, ref_text, show_lengths, length_unit):
        """Return `text` rendered as markup for display."""
        # We don't actually use the length_unit argument,
        # but do need it accounted for in memoized values.
        if not text: return ""
        text = GLib.markup_escape_text(text)
        ref_text = GLib.markup_escape_text(ref_text)
        with aeidon.util.silent(Exception, tb=True):
            text = self._add_diff_markup(text, ref_text)
        if not show_lengths: return text
        lines = text.split("\n")
        lengths = gaupol.ruler.get_lengths(text)
        return "\n".join(("{} <small>[{:d}]</small>"
                          .format(lines[i], lengths[i])
                          if lines[i] else lines[i]
                          for i in range(len(lines))))
