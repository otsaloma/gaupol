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


"""Dialogs to select files for opening and saving."""


import os

try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.constants import EXTENSION, FORMAT, NEWLINE
from gaupol.gui.dialogs.encoding import EncodingDialog
from gaupol.lib.util import encodinglib


class CustomFileChooserDialog(gtk.FileChooserDialog):
    
    """Base class for custom dialogs to select files for opening and saving."""
    
    def _add_filters(self):
        """Add file filters displayed in a ComboBox."""

        # File-filter setting is not remembered, because applying it is
        # somewhat problematic. Setting a filename that conflicts with the
        # filter causes the filter combo box to display empty. The filter
        # would have to be checked and possibly adjusted when setting the
        # filename and there is no easy way to determine when the filename
        # conflicts with the filter.

        # Format, Name           , Mime-type   , Pattern
        filters = [
            (None   , _('All files') , None        , '*'    ),
            (None   , _('Plain text'), 'text/plain', None   ),
        ]

        for i in range(len(FORMAT.NAMES)):
        
            format_name = FORMAT.NAMES[i]
            extension_value = EXTENSION.VALUES[i]

            # TRANSLATORS: File filters - e.g. "SubRip (*.srt)".
            name = _('%s (*%s)') % (format_name, extension_value)
            pattern = '*%s' % extension_value
            
            filters.append((format_name, name, None, pattern))
        
        for entry in filters:
        
            format, name, mime, pattern = entry
            file_filter = gtk.FileFilter()

            file_filter.set_name(name)
            if mime is not None:
                file_filter.add_mime_type(mime)
            if pattern is not None:
                file_filter.add_pattern(pattern)
                
            self.add_filter(file_filter)

    def get_encoding(self):
        """Get selected encoding."""

        encodings = encodinglib.get_valid_python_names()
        entry = self._encoding_combo_box.get_active_text()

        if entry == encodinglib.get_locale_descriptive_name():
            return encodinglib.get_locale_encoding()[0]
        
        for python_name in encodings:
            if entry == encodinglib.get_descriptive_name(python_name):
                return python_name
    
    def _fill_encoding_combo_box(self):
        """Insert items to encoding ComboBox."""

        entries = self._get_encoding_combo_box_entries()

        # Clear ComboBox.
        while self._encoding_combo_box.get_active_text() is not None:
            self._encoding_combo_box.remove_text(0)
        
        # Fill ComboBox.
        for entry in entries:
            self._encoding_combo_box.append_text(entry)
            
        # Set active encoding.
        self.set_encoding(self._config.get('file', 'encoding'))
                        
    def _get_encoding_combo_box_entries(self):
        """Get a list of entries to be put in the encoding ComboBox."""

        visible_encodings = self._config.getlist('file', 'visible_encodings')
        active_encoding   = self._config.get('file', 'encoding')
        
        # Add active encoding.
        if encodinglib.is_valid_python_name(active_encoding):
            if not active_encoding in visible_encodings:
                visible_encodings.append(active_encoding)
        
        # Get descriptive names for encodings.
        entries = []
        for encoding in visible_encodings:
            try:
                entries.append(encodinglib.get_descriptive_name(encoding))
            except ValueError:
                continue
        
        entries.sort()
        
        # Add locale encoding.
        locale_name = encodinglib.get_locale_descriptive_name()
        if locale_name is not None:
            entries.insert(0, locale_name)
        
        entries.append(_('Other...'))

        return entries

    def _on_encoding_changed(self, combo_box):
        """Present a dialog if "Other..." encoding was selected."""

        entry = combo_box.get_active_text()

        if entry != _('Other...'):
            return
        
        dialog = EncodingDialog(self._config, self)
        response = dialog.run()

        if response != gtk.RESPONSE_OK:
            dialog.destroy()
            self._fill_encoding_combo_box()
            return

        encoding = dialog.get_encoding()
        if encoding is not None:
            self._config.set('file', 'encoding', encoding)
            
        visible_encodings = dialog.get_visible_encodings()
        self._config.setlist('file', 'visible_encodings', visible_encodings)

        dialog.destroy()
        self._fill_encoding_combo_box()

    def set_encoding(self, encoding, entries=None):
        """
        Set active encoding in the encoding combo box.
        
        entries: encoding ComboBox entries
        """
        entries = entries or self._get_encoding_combo_box_entries()

        self._encoding_combo_box.set_active(0)

        # Leave locale encoding active or...
        try:
            if encoding == encodinglib.get_locale_encoding()[0]:
                return
        except TypeError:
            pass

        # ...set another encoding active.
        try:
            encoding_name = encodinglib.get_descriptive_name(encoding)
        except ValueError:
            pass
        else:
            for i in range(len(entries)):
                if entries[i] == encoding_name:
                    self._encoding_combo_box.set_active(i)
                    break


class OpenDialog(CustomFileChooserDialog):
    
    """Dialog to select file for opening."""
    
    def __init__(self, config, title, parent):

        gtk.FileChooserDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
             gtk.STOCK_OPEN  , gtk.RESPONSE_OK     )
        )
        
        self._config = config

        self._encoding_combo_box = None

        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(self._config.get('file', 'directory'))

        self._add_filters()
        self._build_extra_widget()
        self._fill_encoding_combo_box()
        
    def _build_extra_widget(self):
        """Build a ComboBox to select encoding."""

        combo_box = gtk.combo_box_new_text()
        combo_box.connect('changed', self._on_encoding_changed)
        
        label = gtk.Label()
        label.set_markup_with_mnemonic(_('Character _encoding:'))
        label.set_mnemonic_widget(combo_box)
        
        hbox = gtk.HBox(False, 12)
        hbox.pack_start(label    , False, True, 0)
        hbox.pack_start(combo_box, True , True, 0)
        hbox.show_all()

        self._encoding_combo_box = combo_box
        self.set_extra_widget(hbox)


class SaveDialog(CustomFileChooserDialog):
    
    """Dialog to select file for saving."""
    
    def __init__(self, config, title, parent):

        gtk.FileChooserDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
             gtk.STOCK_SAVE  , gtk.RESPONSE_OK     )
        )
        
        self._config = config

        # Widgets
        self._format_combo_box   = None
        self._encoding_combo_box = None
        self._newline_combo_box  = None
        
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(self._config.get('file', 'directory'))
        
        self._add_filters()
        self._build_extra_widget()
        
        self._fill_format_combo_box()
        self._fill_encoding_combo_box()
        self._fill_newline_combo_box()

    def _build_extra_widget(self):
        """Build ComboBoxes for selecting format, encoding and newlines."""

        self._format_combo_box   = gtk.combo_box_new_text()
        self._encoding_combo_box = gtk.combo_box_new_text()
        self._newline_combo_box  = gtk.combo_box_new_text()

        self._format_combo_box.connect(  'changed', self._on_format_changed  )
        self._encoding_combo_box.connect('changed', self._on_encoding_changed)

        format_label = gtk.Label()
        format_label.set_property('xalign', 0)
        format_label.set_markup_with_mnemonic(_('Fo_rmat:'))
        format_label.set_mnemonic_widget(self._format_combo_box)

        encoding_label = gtk.Label()
        encoding_label.set_property('xalign', 0)
        encoding_label.set_markup_with_mnemonic(_('Character _encoding:'))
        encoding_label.set_mnemonic_widget(self._encoding_combo_box)

        newline_label = gtk.Label()
        newline_label.set_property('xalign', 0)
        newline_label.set_markup_with_mnemonic(_('Ne_wlines:'))
        newline_label.set_mnemonic_widget(self._newline_combo_box)

        table = gtk.Table(3, 2)
        table.set_row_spacings(6)
        table.set_col_spacings(12)
        
        options = gtk.FILL
        table.attach(format_label  , 0, 1, 0, 1, options, options)
        table.attach(encoding_label, 0, 1, 1, 2, options, options)
        table.attach(newline_label , 0, 1, 2, 3, options, options)
        
        options = gtk.EXPAND|gtk.FILL
        table.attach(self._format_combo_box  , 1, 2, 0, 1, options, options)
        table.attach(self._encoding_combo_box, 1, 2, 1, 2, options, options)
        table.attach(self._newline_combo_box , 1, 2, 2, 3, options, options)

        table.show_all()
        self.set_extra_widget(table)
    
    def _fill_format_combo_box(self):
        """Insert items to format ComboBox."""

        for format_name in FORMAT.NAMES:
            self._format_combo_box.append_text(format_name)

        format_name = self._config.get('file', 'format')
        self._format_combo_box.set_active(FORMAT.NAMES.index(format_name))

    def _fill_newline_combo_box(self):
        """Insert items to newline ComboBox."""

        for newline_name in NEWLINE.NAMES:
            self._newline_combo_box.append_text(newline_name)

        newline_name = self._config.get('file', 'newlines')
        self._newline_combo_box.set_active(NEWLINE.NAMES.index(newline_name))

    def get_filename_with_extension(self):
        """Get filename and add extension if it is lacking."""
        
        path = self.get_filename()

        if path is None:
            return None

        extension_value = EXTENSION.VALUES[self.get_format()]
        if not path.endswith(extension_value):
            path += extension_value

        return path
        
    def get_format(self):
        """Get selected format."""

        return self._format_combo_box.get_active()

    def get_newlines(self):
        """Get selected newlines."""

        return self._newline_combo_box.get_active()

    def _on_format_changed(self, combo_box):
        """Change extension to reflect new format."""

        new_format_name = combo_box.get_active_text()
        new_format = FORMAT.NAMES.index(new_format_name)
        path = self.get_filename()

        if path is None:
            return
        
        self.unselect_filename(path)

        dirname  = os.path.dirname(path)
        basename = os.path.basename(path)
        
        # Remove possible existing extension.
        for extension in EXTENSION.VALUES:
            if basename.endswith(extension):
                basename = basename[:-len(extension)]
                break

        # Add new extension.
        basename += EXTENSION.VALUES[new_format]
        path = os.path.join(dirname, basename)

        self.set_current_name(basename)
        self.set_filename(path)

    def set_format(self, format):
        """Set active format in the format combo box."""

        try:
            self._format_combo_box.set_active(format)
        except (TypeError, ValueError):
            pass

    def set_newlines(self, newlines):
        """Set active newlines in the newlines combo box."""
        
        try:
            self._newline_combo_box.set_active(newlines)
        except (TypeError, ValueError):
            pass
