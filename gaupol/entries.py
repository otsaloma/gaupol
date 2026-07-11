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

"""Entry for time data in format ``[-]HH:MM:SS.SSS``."""

import functools
import gaupol
import re

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("TimeEntry",)


def _blocked(function):
    """Decorator for methods to be run with buffer edits allowed."""
    @functools.wraps(function)
    def wrapper(entry, *args, **kwargs):
        entry.get_buffer().allow_edit = True
        try:
            return function(entry, *args, **kwargs)
        finally:
            entry.get_buffer().allow_edit = False
    return wrapper


class _TimeBuffer(Gtk.EntryBuffer):

    """
    Entry buffer that blocks all edits not explicitly allowed.

    Blocked insertions are routed to the entry's validating
    :meth:`TimeEntry._insert_text` instead; blocked deletions
    only move the cursor to the start of the range.
    """

    def __init__(self, entry):
        """Initialize a :class:`_TimeBuffer` instance."""
        GObject.GObject.__init__(self)
        self.allow_edit = False
        self._entry = entry

    def do_delete_text(self, position, n_chars):
        """Delete text if allowed, otherwise just move the cursor."""
        if self.allow_edit:
            return Gtk.EntryBuffer.do_delete_text(self, position, n_chars)
        gaupol.util.idle_add(self._entry.set_position, position)
        return 0

    def do_insert_text(self, position, chars, n_chars):
        """Insert text if allowed, otherwise route to validation."""
        if self.allow_edit:
            return Gtk.EntryBuffer.do_insert_text(self, position, chars, n_chars)
        gaupol.util.idle_add(self._entry._insert_text, chars)
        return 0


class TimeEntry(Gtk.Entry):

    """
    Entry for time data in format ``[-]HH:MM:SS.SSS``.

    This widget uses :func:`GLib.idle_add` a lot, which means that clients may
    need to call :func:`gaupol.util.iterate_main` to ensure proper updating.
    """
    _re_digit = re.compile(r"\d")
    _re_time = re.compile(r"^-?\d\d:[0-5]\d:[0-5]\d\.\d\d\d$")

    def __init__(self):
        """Initialize a :class:`TimeEntry` instance."""
        GObject.GObject.__init__(self)
        self.set_buffer(_TimeBuffer(self))
        self.set_width_chars(13)
        self.set_max_length(13)
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        text_widget = self.get_delegate()
        text_widget.connect("cut-clipboard", self._on_cut_clipboard)
        text_widget.connect("toggle-overwrite", self._on_toggle_overwrite)
        controller = Gtk.EventControllerKey()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(controller)

    @_blocked
    def _insert_text(self, value):
        """Insert `value` as text after validation."""
        pos = self.get_position()
        text = self.get_text()
        if pos == 0 and value.startswith("-"):
            text = text if text.startswith("-") else "-{}".format(text)
        length = len(value)
        text = text[:pos] + value + text[pos+length:]
        text = text.replace(",", ".")
        if not self._re_time.match(text): return
        self.set_text(text)
        self.set_position(pos)
        if length != 1: return
        self.set_position(pos + 1)
        if len(text) > pos + 1 and text[pos+1] in (":", "."):
            self.set_position(pos + 2)

    def _on_cut_clipboard(self, text_widget):
        """Change "cut-clipboard" signal to "copy-clipboard"."""
        text_widget.stop_emission_by_name("cut-clipboard")
        text_widget.emit("copy-clipboard")

    def _on_key_pressed(self, controller, keyval, keycode, state):
        """Change numbers to zero if Backspace or Delete pressed."""
        keys = (Gdk.KEY_BackSpace, Gdk.KEY_Delete)
        if not keyval in keys: return False
        if self.get_selection_bounds():
            gaupol.util.idle_add(self._zero_selection)
        elif keyval == Gdk.KEY_BackSpace:
            gaupol.util.idle_add(self._zero_previous)
        elif keyval == Gdk.KEY_Delete:
            gaupol.util.idle_add(self._zero_next)
        return True

    def _on_toggle_overwrite(self, text_widget):
        """Do not allow toggling overwrite."""
        text_widget.stop_emission_by_name("toggle-overwrite")

    @_blocked
    def _zero_next(self):
        """Change the next digit to zero."""
        pos = self.get_position()
        text = self.get_text()
        if pos >= len(text): return
        if pos == 0 and text.startswith("-"):
            self.set_text(text[1:])
            return self.set_position(0)
        if not text[pos].isdigit(): return
        self.set_text(text[:pos] + "0" + text[pos+1:])
        self.set_position(pos)

    @_blocked
    def _zero_previous(self):
        """Change the previous digit to zero."""
        pos = self.get_position()
        text = self.get_text()
        if pos <= 0: return
        if pos == 1 and text.startswith("-"):
            self.set_text(text[1:])
            return self.set_position(0)
        if not text[pos-1].isdigit():
            return self.set_position(pos-1)
        self.set_text(text[:pos-1] + "0" + text[pos:])
        self.set_position(pos-1)

    @_blocked
    def _zero_selection(self):
        """Change digits in selection to zero."""
        if not self.get_selection_bounds(): return
        a, z = self.get_selection_bounds()
        text = self.get_text()
        zero = self._re_digit.sub("0", text[a:z])
        self.set_text(text[:a] + zero + text[z:])
        self.set_position(a)
