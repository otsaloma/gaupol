# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Entry for time data in format hh:mm:ss,sss."""


# References on validation:
# PyGTK FAQ 14.5
# http://www.async.com.br/faq/pygtk/index.py?req=show&file=faq14.005.htp


import re

import gobject
import gtk


re_time   = re.compile(r'^\d\d:[0-5]\d:[0-5]\d,\d\d\d$')
re_number = re.compile(r'\d')


def blockedmethod(function):
    """Decorator for methods to be run blocked."""

    def wrapper(*args, **kwargs):

        entry = args[0]

        entry.handler_block(entry._delete_signal)
        entry.handler_block(entry._insert_signal)

        function(*args, **kwargs)

        entry.handler_unblock(entry._delete_signal)
        entry.handler_unblock(entry._insert_signal)

    return wrapper


class TimeEntry(gtk.Entry):

    """Entry for time data in format hh:mm:ss,sss."""

    def __init__(self):

        gtk.Entry.__init__(self)

        self._delete_signal = None
        self._insert_signal = None

        self.set_width_chars(12)
        self.set_max_length(12)
        self._init_signals()

    def _init_signals(self):
        """Initialize signals."""

        self.connect('cut-clipboard'   , self._on_cut_clipboard   )
        self.connect('key-press-event' , self._on_key_press_event )
        self.connect('toggle-overwrite', self._on_toggle_overwrite)

        self._delete_signal = self.connect('delete-text', self._on_delete_text)
        self._insert_signal = self.connect('insert-text', self._on_insert_text)

    @blockedmethod
    def _insert_text(self, text):
        """Insert text."""

        length    = len(text)
        position  = self.get_position()
        orig_text = self.get_text()
        new_text  = orig_text[:position] + text + orig_text[position + length:]

        if not re_time.match(new_text):
            return

        self.set_text(new_text)

        if length == 1:
            new_position = position + length
            self.set_position(new_position)
            if new_position in (2, 5, 8):
                self.set_position(new_position + 1)

    @blockedmethod
    def _change_next_to_zero(self):
        """Change next number to zero."""

        position  = self.get_position()
        orig_text = self.get_text()

        if position in (2, 5, 8, 12):
            return

        text_before = orig_text[:position]
        text_after  = orig_text[position + 1:]
        full_text   = text_before + '0' + text_after

        self.set_text(full_text)
        self.set_position(position)

    @blockedmethod
    def _change_previous_to_zero(self):
        """Change next number to zero."""

        position  = self.get_position()
        orig_text = self.get_text()

        if position ==  0:
            return
        if position in (3, 6, 9):
            self.set_position(position - 1)
            return

        text_before = orig_text[:position - 1]
        text_after  = orig_text[position:]
        full_text   = text_before + '0' + text_after

        self.set_text(full_text)
        self.set_position(position - 1)

    @blockedmethod
    def _change_selection_to_zero(self):
        """Change numbers in selection to zero."""

        if not self.get_selection_bounds():
            return

        position   = self.get_position()
        start, end = self.get_selection_bounds()
        orig_text  = self.get_text()

        zero_text = re_number.sub('0', orig_text[start:end])
        full_text = orig_text[:start] + zero_text + orig_text[end:]

        self.set_text(full_text)
        self.set_position(start)

    def _on_cut_clipboard(self, entry):
        """Transform cut signal to a copy signal."""

        self.emit_stop_by_name('cut-clipboard')
        self.emit('copy-clipboard')

    def _on_delete_text(self, entry, start_position, end_position):
        """Do not allow deleting text."""

        self.emit_stop_by_name('delete-text')
        self.set_position(start_position)

    def _on_key_press_event(self, entry, event):
        """Change numbers to zero if BackSpace or Delete pressed."""

        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname in ('BackSpace', 'Delete'):
            self.emit_stop_by_name('key-press-event')

            if self.get_selection_bounds():
                gobject.idle_add(self._change_selection_to_zero)
            elif keyname == 'BackSpace':
                gobject.idle_add(self._change_previous_to_zero)
            elif keyname == 'Delete':
                gobject.idle_add(self._change_next_to_zero)

    def _on_insert_text(self, entry, text, length, position):
        """Insert text if it is proper."""

        self.emit_stop_by_name('insert-text')
        gobject.idle_add(self._insert_text, text)

    def _on_toggle_overwrite(self, entry):
        """Do not allow toggling overwrite."""

        self.emit_stop_by_name('toggle-overwrite')


if __name__ == '__main__':

    from gaupol.test import Test

    class TestIntegerEntry(Test):

        def test_init(self):

            entry = TimeEntry()
            entry.set_text('00:33:22,111')
            window = gtk.Window()
            window.connect('delete-event', gtk.main_quit)
            window.set_position(gtk.WIN_POS_CENTER)
            window.set_default_size(200, 50)
            window.add(entry)
            window.show_all()
            gtk.main()

    TestIntegerEntry().run()
