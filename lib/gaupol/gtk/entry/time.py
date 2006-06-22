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


"""Entry for time data in format HH:MM:SS.SSS."""


import re

import gobject
import gtk

from gaupol.gtk.util import gtklib


_RE_TIME   = re.compile(r'^\d\d:[0-5]\d:[0-5]\d.\d\d\d$')
_RE_NUMBER = re.compile(r'\d')


def blockedmethod(function):
    """Decorator for methods to be run blocked."""

    def wrapper(*args, **kwargs):
        entry = args[0]
        entry.handler_block(entry._delete_signal)
        entry.handler_block(entry._insert_signal)
        function(*args, **kwargs)
        entry.handler_unblock(entry._insert_signal)
        entry.handler_unblock(entry._delete_signal)

    return wrapper


class EntryTime(gtk.Entry):

    """
    Entry for time data in format HH:MM:SS.SSS.

    Instance variables:

        _delete_signal: Delete signal to block
        _insert_signal: Insert signal to block

    """

    def __init__(self):

        gtk.Entry.__init__(self)

        self._delete_signal = None
        self._insert_signal = None

        self.set_width_chars(12)
        self.set_max_length(12)
        self._init_signals()

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, self, 'cut-clipboard')
        gtklib.connect(self, self, 'key-press-event')
        gtklib.connect(self, self, 'toggle-overwrite')

        self._delete_signal = gtklib.connect(self, self, 'delete-text')
        self._insert_signal = gtklib.connect(self, self, 'insert-text')

    @blockedmethod
    def _insert_text(self, text):
        """Insert text."""

        length = len(text)
        pos = self.get_position()
        orig_text = self.get_text()
        new_text = orig_text[:pos] + text + orig_text[pos + length:]

        if not _RE_TIME.match(new_text):
            return
        self.set_text(new_text)

        if length == 1:
            new_pos = pos + length
            self.set_position(new_pos)
            if new_pos in (2, 5, 8):
                self.set_position(new_pos + 1)

    def _on_cut_clipboard(self, entry):
        """Transform cut signal to a copy signal."""

        self.stop_emission('cut-clipboard')
        self.emit('copy-clipboard')

    def _on_delete_text(self, entry, start_pos, end_pos):
        """Do not allow deleting text."""

        self.stop_emission('delete-text')
        self.set_position(start_pos)

    def _on_key_press_event(self, entry, event):
        """Change numbers to zero if BackSpace or Delete pressed."""

        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in ('BackSpace', 'Delete'):
            return

        self.stop_emission('key-press-event')
        if self.get_selection_bounds():
            gobject.idle_add(self._zero_selection)
        elif keyname == 'BackSpace':
            gobject.idle_add(self._zero_previous)
        elif keyname == 'Delete':
            gobject.idle_add(self._zero_next)

    def _on_insert_text(self, entry, text, length, pos):
        """Insert text if it is proper."""

        self.stop_emission('insert-text')
        gobject.idle_add(self._insert_text, text)

    def _on_toggle_overwrite(self, entry):
        """Do not allow toggling overwrite."""

        self.stop_emission('toggle-overwrite')

    @blockedmethod
    def _zero_next(self):
        """Change next number to zero."""

        pos = self.get_position()
        if pos in (2, 5, 8, 12):
            return

        orig_text = self.get_text()
        text_before = orig_text[:pos]
        text_after = orig_text[pos + 1:]
        full_text = text_before + '0' + text_after

        self.set_text(full_text)
        self.set_position(pos)

    @blockedmethod
    def _zero_previous(self):
        """Change previous number to zero."""

        pos = self.get_position()
        if pos in (0, 3, 6, 9):
            if pos in (3, 6, 9):
                self.set_position(pos - 1)
            return

        orig_text = self.get_text()
        text_before = orig_text[:pos - 1]
        text_after = orig_text[pos:]
        full_text = text_before + '0' + text_after

        self.set_text(full_text)
        self.set_position(pos - 1)

    @blockedmethod
    def _zero_selection(self):
        """Change numbers in selection to zero."""

        if not self.get_selection_bounds():
            return

        start, end = self.get_selection_bounds()
        orig_text = self.get_text()
        zero_text = _RE_NUMBER.sub('0', orig_text[start:end])
        full_text = orig_text[:start] + zero_text + orig_text[end:]

        self.set_text(full_text)
        self.set_position(start)
