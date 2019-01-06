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

import aeidon
import functools
import gaupol
import re

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("TimeEntry",)


def _blocked(function):
    """Decorator for methods to be run blocked to avoid recursion."""
    @functools.wraps(function)
    def wrapper(entry, *args, **kwargs):
        entry.handler_block(entry._delete_handler)
        entry.handler_block(entry._insert_handler)
        value = function(entry, *args, **kwargs)
        entry.handler_unblock(entry._insert_handler)
        entry.handler_unblock(entry._delete_handler)
        return value
    return wrapper


class TimeEntry(Gtk.Entry):

    """
    Entry for time data in format ``[-]HH:MM:SS.SSS``.

    :ivar _delete_handler: Handler for "delete-text" signal
    :ivar _insert_handler: Handler for "insert-text" signal

    This widget uses :func:`GLib.idle_add` a lot, which means that clients may
    need to call :func:`Gtk.main_iteration` to ensure proper updating.
    """
    _re_digit = re.compile(r"\d")
    _re_time = re.compile(r"^-?\d\d:[0-5]\d:[0-5]\d\.\d\d\d$")

    def __init__(self):
        """Initialize a :class:`TimeEntry` instance."""
        GObject.GObject.__init__(self)
        self._delete_handler = None
        self._insert_handler = None
        self.set_width_chars(13)
        self.set_max_length(13)
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "cut-clipboard")
        aeidon.util.connect(self, self, "key-press-event")
        aeidon.util.connect(self, self, "toggle-overwrite")
        self._delete_handler = aeidon.util.connect(self, self, "delete-text")
        self._insert_handler = aeidon.util.connect(self, self, "insert-text")

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

    def _on_cut_clipboard(self, entry):
        """Change "cut-clipboard" signal to "copy-clipboard"."""
        self.stop_emission_by_name("cut-clipboard")
        self.emit("copy-clipboard")

    def _on_delete_text(self, entry, start_pos, end_pos):
        """Do not allow deleting text."""
        self.stop_emission_by_name("delete-text")
        self.set_position(start_pos)

    def _on_key_press_event(self, entry, event):
        """Change numbers to zero if Backspace or Delete pressed."""
        keys = (Gdk.KEY_BackSpace, Gdk.KEY_Delete)
        if not event.keyval in keys: return
        self.stop_emission_by_name("key-press-event")
        if self.get_selection_bounds():
            gaupol.util.idle_add(self._zero_selection)
        elif event.keyval == Gdk.KEY_BackSpace:
            gaupol.util.idle_add(self._zero_previous)
        elif event.keyval == Gdk.KEY_Delete:
            gaupol.util.idle_add(self._zero_next)

    def _on_insert_text(self, entry, text, length, pos):
        """Insert `text` after validation."""
        self.stop_emission_by_name("insert-text")
        gaupol.util.idle_add(self._insert_text, text)

    def _on_toggle_overwrite(self, entry):
        """Do not allow toggling overwrite."""
        self.stop_emission_by_name("toggle-overwrite")

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
