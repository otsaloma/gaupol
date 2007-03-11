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


"""Entry for time data in format HH:MM:SS.SSS.

Module variables:

    _RE_DIGIT: Regular expression for a digit
    _RE_TIME:  Regular expression for time in format HH:MM:SS.SSS
"""


import functools
import gobject
import gtk
import re

from gaupol.gtk import util


_RE_DIGIT = re.compile(r"\d")
_RE_TIME  = re.compile(r"^\d\d:[0-5]\d:[0-5]\d\.\d\d\d$")


def _blocked(function):
    """Decorator for methods to be run blocked."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        entry = args[0]
        entry.handler_block(entry._delete_handler)
        entry.handler_block(entry._insert_handler)
        value = function(*args, **kwargs)
        entry.handler_unblock(entry._insert_handler)
        entry.handler_unblock(entry._delete_handler)
        return value

    return wrapper


class TimeEntry(gtk.Entry):

    """Entry for time data in format HH:MM:SS.SSS.

    Instance variables:

        _delete_handler: Handler for 'delete-text' signal
        _insert_handler: Handler for 'insert-text' signal
    """

    def __init__(self):

        gtk.Entry.__init__(self)

        self._delete_handler = None
        self._insert_handler = None

        self.set_width_chars(12)
        self.set_max_length(12)
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "cut-clipboard")
        util.connect(self, self, "key-press-event")
        util.connect(self, self, "toggle-overwrite")

        self._delete_handler = util.connect(self, self, "delete-text")
        self._insert_handler = util.connect(self, self, "insert-text")

    @_blocked
    @util.ignore_exceptions(AssertionError)
    def _insert_text(self, text):
        """Insert text."""

        length = len(text)
        pos = self.get_position()
        orig_text = self.get_text()
        new_text = orig_text[:pos] + text + orig_text[pos + length:]
        assert _RE_TIME.match(new_text)
        self.set_text(new_text)
        if length == 1:
            new_pos = pos + length
            self.set_position(new_pos)
            if new_pos in (2, 5, 8):
                self.set_position(new_pos + 1)

    def _on_cut_clipboard(self, entry):
        """Transform cut signal to a copy signal."""

        self.stop_emission("cut-clipboard")
        self.emit("copy-clipboard")

    def _on_delete_text(self, entry, start_pos, end_pos):
        """Do not allow deleting text."""

        self.stop_emission("delete-text")
        self.set_position(start_pos)

    @util.ignore_exceptions(AssertionError)
    def _on_key_press_event(self, entry, event):
        """Change numbers to zero if BackSpace or Delete pressed."""

        assert event.keyval in (gtk.keysyms.BackSpace, gtk.keysyms.Delete)
        self.stop_emission("key-press-event")
        if self.get_selection_bounds():
            gobject.idle_add(self._zero_selection)
        elif event.keyval == gtk.keysyms.BackSpace:
            gobject.idle_add(self._zero_previous)
        elif event.keyval == gtk.keysyms.Delete:
            gobject.idle_add(self._zero_next)

    def _on_insert_text(self, entry, text, length, pos):
        """Insert text if it is proper."""

        self.stop_emission("insert-text")
        gobject.idle_add(self._insert_text, text)

    def _on_toggle_overwrite(self, entry):
        """Do not allow toggling overwrite."""

        self.stop_emission("toggle-overwrite")

    @_blocked
    @util.ignore_exceptions(AssertionError)
    def _zero_next(self):
        """Change next digit to zero."""

        pos = self.get_position()
        assert pos in (2, 5, 8, 12)
        orig_text = self.get_text()
        text_before = orig_text[:pos]
        text_after = orig_text[pos + 1:]
        full_text = text_before + "0" + text_after
        self.set_text(full_text)
        self.set_position(pos)

    @_blocked
    def _zero_previous(self):
        """Change previous digit to zero."""

        pos = self.get_position()
        if pos in (0, 3, 6, 9):
            self.set_position(max(0, pos - 1))
            return
        orig_text = self.get_text()
        text_before = orig_text[:pos - 1]
        text_after = orig_text[pos:]
        full_text = text_before + "0" + text_after
        self.set_text(full_text)
        self.set_position(pos - 1)

    @_blocked
    @util.ignore_exceptions(AssertionError)
    def _zero_selection(self):
        """Change digits in selection to zero."""

        assert self.get_selection_bounds()
        a, z = self.get_selection_bounds()
        orig_text = self.get_text()
        zero_text = _RE_DIGIT.sub("0", orig_text[a:z])
        full_text = orig_text[:a] + zero_text + orig_text[z:]
        self.set_text(full_text)
        self.set_position(a)
