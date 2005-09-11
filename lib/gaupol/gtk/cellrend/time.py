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


"""CellRenderer for cells containing time in format hh:mm:ss,sss."""


# Resources:
# PyGTK FAQ 14.5
# http://www.async.com.br/faq/pygtk/index.py?req=show&file=faq14.005.htp


import re

try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gui.cellrend.custom import CustomCellRenderer


RE_TIME   = re.compile('^\d\d:[0-5]\d:[0-5]\d,\d\d\d$')
RE_NUMBER = re.compile('\d')


class CellRendererTime(CustomCellRenderer):

    """CellRenderer for cells containing time in format hh:mm:ss,sss."""

    def __init__(self, *args):
    
        CustomCellRenderer.__init__(self, *args)
        
        # Signal IDs
        self._delete_signal    = None
        self._insert_signal    = None
        self._key_press_signal = None

    def _change_to_zero(self, editor, keyname):
        """
        Change numbers to zero.
        
        keyname: "BackSpace" or "Delete"
        """
        editor.handler_block(self._delete_signal   )
        editor.handler_block(self._insert_signal   )

        position  = editor.get_position()
        bounds    = editor.get_selection_bounds()
        orig_text = editor.get_text()

        # Change numbers in selection to zero.
        if bounds:

            start = bounds[0]
            end   = bounds[1]
            
            zero_text = RE_NUMBER.sub('0', orig_text[start:end])
            new_text  = orig_text[:start] + zero_text + orig_text[end:]

            editor.set_text(new_text)
            editor.set_position(start)

        # Change previous number to zero.
        elif keyname == 'BackSpace':
        
            if position > 0 and orig_text[position - 1].isdigit():

                text_before = orig_text[:position - 1]
                text_after  = orig_text[position:]
                new_text    = text_before + '0' + text_after

                editor.set_text(new_text)

            editor.set_position(max(position - 1, 0))
        
        # Change next number to zero.
        elif keyname == 'Delete':
        
            if position < 12 and orig_text[position].isdigit():

                text_before = orig_text[:position]
                text_after  = orig_text[position + 1:]
                new_text    = text_before + '0' + text_after
                
                editor.set_text(new_text)
                
            editor.set_position(position)

        editor.handler_unblock(self._delete_signal   )
        editor.handler_unblock(self._insert_signal   )

    def _insert_text(self, editor, text):
        """
        Insert text to editor.
        
        This method is called after the default emission has been cancelled.
        """
        editor.handler_block(self._delete_signal)
        editor.handler_block(self._insert_signal)
      
        length    = len(text)
        position  = editor.get_position()

        orig_text = editor.get_text()
        new_text = orig_text[:position] + text + orig_text[position + length:]
        
        if RE_TIME.match(new_text):
            
            editor.set_text(new_text)

            new_position = position + length
            editor.set_position(new_position)
            if new_position in [2, 5, 8]:
                editor.set_position(new_position + 1)

        editor.handler_unblock(self._delete_signal)
        editor.handler_unblock(self._insert_signal)

    def on_cut_clipboard(self, editor):
        """Transform cut signal to a copy signal."""

        editor.emit_stop_by_name('cut-clipboard')
        editor.emit('copy-clipboard')

    def on_delete_text(self, editor, start_position, end_position):
        """Do not allow deleting text."""

        editor.emit_stop_by_name('delete-text')
        editor.set_position(start_position)

    def on_insert_text(self, editor, text, length, pointer):
        """Insert text to editor."""

        editor.emit_stop_by_name('insert-text')
        gobject.idle_add(self._insert_text, editor, text)

    def on_key_press_event(self, editor, event):
        """Change numbers to zero if BackSpace or Delete pressed"""
        
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname in ['BackSpace', 'Delete']:
            editor.emit_stop_by_name('key-press-event')
            gobject.idle_add(self._change_to_zero, editor, keyname)

    def on_start_editing(self, event, widget, row, background_area, cell_area,
                         flags):
        """
        Initiate editing of the cell.

        Return: gtk.Entry
        """
        editor = gtk.Entry()

        editor.set_has_frame(False)
        editor.set_activates_default(True)
        editor.set_width_chars(12)
        editor.set_max_length(12)
        editor.set_size_request(-1, cell_area.height)
        editor.modify_font(self.font_description)

        editor.set_text(self.text or '')

        # Simple methods
        editor.connect('cut-clipboard'   , self.on_cut_clipboard        )
        editor.connect('editing-done'    , self.on_editing_done    , row)
        editor.connect('toggle-overwrite', self.on_toggle_overwrite     )

        # Overriding methods
        signal = 'delete-text'
        method = self.on_delete_text
        self._delete_signal = editor.connect(signal, method)
        
        signal = 'insert-text'
        method = self.on_insert_text
        self._insert_signal = editor.connect(signal, method)

        signal = 'key-press-event'
        method = self.on_key_press_event
        self._key_press_signal = editor.connect(signal, method)
        
        editor.grab_focus()
        editor.show()

        return editor

    def on_toggle_overwrite(self, editor):
        """Do not allow toggling overwrite."""

        editor.emit_stop_by_name('toggle-overwrite')
