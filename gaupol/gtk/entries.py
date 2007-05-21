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


"""Entry for time data in format [-]HH:MM:SS.SSS."""


import functools
import gobject
import gtk
import re

from gaupol.gtk import util


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

    This widget uses 'gobject.idle_add' a lot, which means that clients may
    need to call 'gtk.main_iteration' to ensure that proper updating.
    """

    __metaclass__ = util.get_contractual_metaclass()
    _re_digit = re.compile(r"\d")
    _re_time  = re.compile(r"^-?\d\d:[0-5]\d:[0-5]\d\.\d\d\d$")

    def __init__(self):

        gtk.Entry.__init__(self)
        self._delete_handler = None
        self._insert_handler = None

        self.set_width_chars(13)
        self.set_max_length(13)
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "cut-clipboard")
        util.connect(self, self, "key-press-event")
        util.connect(self, self, "toggle-overwrite")

        self._delete_handler = util.connect(self, self, "delete-text")
        self._insert_handler = util.connect(self, self, "insert-text")

    @_blocked
    @util.asserted_return
    def _insert_text(self, value):
        """Insert text."""

        pos = self.get_position()
        text = self.get_text()
        if (pos == 0) and value.startswith("-"):
            text = "-%s" % text
            pos += 1
            value = value[1:]
        length = len(value)
        text = text[:pos] + value + text[pos + length:]
        assert self._re_time.match(text)
        self.set_text(text)
        self.set_position(pos)
        assert length == 1
        self.set_position(pos + 1)
        assert pos + 1 < len(text)
        if text[pos + 1] in (":", "."):
            self.set_position(pos + 2)

    def _on_cut_clipboard_ensure(self, *args, **kwargs):
        text = self.get_text()
        assert (not text) or self._re_time.match(text)

    def _on_cut_clipboard(self, entry):
        """Transform cut signal to a copy signal."""

        self.stop_emission("cut-clipboard")
        self.emit("copy-clipboard")

    def _on_delete_text_ensure(self, *args, **kwargs):
        text = self.get_text()
        assert (not text) or self._re_time.match(text)

    def _on_delete_text(self, entry, start_pos, end_pos):
        """Do not allow deleting text."""

        self.stop_emission("delete-text")
        self.set_position(start_pos)

    def _on_key_press_event_ensure(self, *args, **kwargs):
        text = self.get_text()
        assert (not text) or self._re_time.match(text)

    @util.asserted_return
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

    def _on_insert_text_ensure(self, *args, **kwargs):
        text = self.get_text()
        assert (not text) or self._re_time.match(text)

    def _on_insert_text(self, entry, text, length, pos):
        """Insert text if it is proper."""

        self.stop_emission("insert-text")
        gobject.idle_add(self._insert_text, text)

    def _on_toggle_overwrite(self, entry):
        """Do not allow toggling overwrite."""

        self.stop_emission("toggle-overwrite")

    @_blocked
    @util.asserted_return
    def _zero_next(self):
        """Change the next digit to zero."""

        pos = self.get_position()
        text = self.get_text()
        assert pos < len(text)
        if (pos == 0) and text.startswith("-"):
            self.set_text(text[1:])
            return self.set_position(0)
        assert text[pos].isdigit()
        before = text[:pos]
        after = text[pos + 1:]
        text = before + "0" + after
        self.set_text(text)
        self.set_position(pos)

    @_blocked
    @util.asserted_return
    def _zero_previous(self):
        """Change the previous digit to zero."""

        pos = self.get_position()
        text = self.get_text()
        assert pos > 0
        if (pos == 1) and text.startswith("-"):
            self.set_text(text[1:])
            return self.set_position(0)
        if not text[pos - 1].isdigit():
            return self.set_position(pos - 1)
        before = text[:pos - 1]
        after = text[pos:]
        text = before + "0" + after
        self.set_text(text)
        self.set_position(pos - 1)

    @_blocked
    @util.asserted_return
    def _zero_selection(self):
        """Change digits in selection to zero."""

        assert self.get_selection_bounds()
        a, z = self.get_selection_bounds()
        text = self.get_text()
        zero = self._re_digit.sub("0", text[a:z])
        text = text[:a] + zero + text[z:]
        self.set_text(text)
        self.set_position(a)
