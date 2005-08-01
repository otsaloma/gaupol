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


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.lib.util import encodings as encodings_module
from gaupol.gui.dialogs.encoding import EncodingDialog


ENCODINGS = encodings_module.get_valid_python_names()

FILTERS = (
    # Format   , # Name               , Mime-type   , Pattern
    (None      , _('All files')       , None        , '*'    ),
    (None      , _('Plain text')      , 'text/plain', None   ),
    ('MicroDVD', _('MicroDVD (*.sub)'), None        , '*.sub'),
    ('SubRip'  , _('SubRip (*.srt)')  , None        , '*.srt'),
)

FORMATS  = ['MicroDVD', 'SubRip']
NEWLINES = ['Mac', 'Unix', 'Windows']


class CustomFileChooserDialog(gtk.FileChooserDialog):
    
    """
    Custom dialog to select files for opening and saving.
    
    This is a generic class meant to be subclassed and extended by actual open-
    and savedialogs.
    """
    
    def _add_filters(self):
        """Add file filters displayed in a ComboBox."""

        # File-filter setting is not remembered, because applying it is
        # somewhat problematic. Setting a filename that conflicts with the
        # filter causes the filter combo box to display empty. The filter
        # would have to be checked and possible adjusted when setting the
        # filename and there is no easy way to determine when the filename
        # conflicts with the filter.
        
        for entry in FILTERS:
        
            format, name, mime, pattern = entry
            file_filter = gtk.FileFilter()

            file_filter.set_name(name)
            if mime is not None:
                file_filter.add_mime_type(mime)
            if pattern is not None:
                file_filter.add_pattern(pattern)
                
            self.add_filter(file_filter)

    def get_encoding(self):
        """
        Get selected encoding.
        
        Raise ValueError if an invalid encoding is selected.
        """
        desc_name = self._enc_cmbox.get_active_text()

        if desc_name == encodings_module.get_locale_descriptive_name():
            return encodings_module.get_locale_encoding()[0]
        
        for python_name in ENCODINGS:
            if desc_name == encodings_module.get_descriptive_name(python_name):
                return python_name
    
    def _fill_encoding_combo_box(self, encoding=None):
        """Insert items to encoding ComboBox."""

        cmbox_entries = self._get_encoding_combo_box_entries()

        # Clear ComboBox.
        while self._enc_cmbox.get_active_text():
            self._enc_cmbox.remove_text(0)
        
        # Fill ComboBox.
        for entry in cmbox_entries:
            self._enc_cmbox.append_text(entry)
            
        # Set active encoding.
        self.set_encoding(self._config.get('file', 'encoding'))
                        
    def _get_encoding_combo_box_entries(self):
        """Get a list of entries to be put in the encoding combo box."""

        vis_encs = self._config.getlist('file', 'visible_encodings')
        act_enc  = self._config.get('file', 'encoding')
        
        if encodings_module.is_valid_python_name(act_enc):
            if not act_enc in vis_encs:
                vis_encs.append(act_enc)
        
        # Get descriptive names for encodings.
        entries = []
        for encoding in vis_encs:
            try:
                entries.append(encodings_module.get_descriptive_name(encoding))
            except ValueError:
                continue
        
        entries.sort()
        
        # Add locale encoding.
        loc_name = encodings_module.get_locale_descriptive_name()
        if loc_name is not None:
            entries.insert(0, loc_name)
        
        entries.append(_('Other...'))

        return entries

    def _on_encoding_changed(self, combo_box):
        """Present a dialog if "Other..." encoding was selected."""

        entry = combo_box.get_active_text()

        if entry != _('Other...'):
            return
        
        enc_dialog = EncodingDialog(self._config, self)
        response = enc_dialog.run()
        
        if response == gtk.RESPONSE_OK:

            encoding = enc_dialog.get_encoding()
            if encoding is not None:
                self._config.set('file', 'encoding', encoding)
                
            vis_encs = enc_dialog.get_visible_encodings()
            self._config.setlist('file', 'visible_encodings', vis_encs)

        enc_dialog.destroy()
        self._fill_encoding_combo_box()

    def set_encoding(self, encoding, entries=None):
        """
        Set active encoding in the encoding combo box.
        
        entries: encoding combo box entries
        """

        entries = entries or self._get_encoding_combo_box_entries()

        try:
            loc_enc = encodings_module.get_locale_encoding()[0]
        except TypeError:
            loc_enc = None

        self._enc_cmbox.set_active(0)

        if loc_enc != encoding:
            try:
                enc_desc_name = encodings_module.get_descriptive_name(encoding)
            except ValueError:
                pass
            else:
                for i in range(len(entries)):
                    if enc_desc_name == entries[i]:
                        self._enc_cmbox.set_active(i)
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
        self._enc_cmbox = None

        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(self._config.get('file', 'directory'))

        self._add_filters()
        self._build_extra_widget()
        self._fill_encoding_combo_box()
        
    def _build_extra_widget(self):
        """Build a ComboBox to select encoding."""

        self._enc_cmbox = gtk.combo_box_new_text()
        self._enc_cmbox.connect('changed', self._on_encoding_changed)
        
        enc_label = gtk.Label()
        enc_label.set_markup_with_mnemonic(_('Character _encoding:'))
        enc_label.set_mnemonic_widget(self._enc_cmbox)
        
        enc_hbox = gtk.HBox(False, 12)
        enc_hbox.pack_start(enc_label      , False, True, 0)
        enc_hbox.pack_start(self._enc_cmbox, True , True, 0)

        enc_hbox.show_all()
        self.set_extra_widget(enc_hbox)


class SaveDialog(CustomFileChooserDialog):
    
    """Dialog to select file for saving."""
    
    def __init__(self, config, title, parent):
        """
        Initialize a SaveDialog object.
        
        Either filename or untitle must be given.
        """

        gtk.FileChooserDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
             gtk.STOCK_SAVE  , gtk.RESPONSE_OK     )
        )
        
        self._config = config

        # Widgets
        self._frm_cmbox = None
        self._enc_cmbox = None
        self._nwl_cmbox = None
        
        self.set_default_response(gtk.RESPONSE_OK)
        self.set_current_folder(self._config.get('file', 'directory'))
        
        self._add_filters()
        self._build_extra_widget()
        
        self._fill_format_combo_box()
        self._fill_encoding_combo_box()
        self._fill_newlines_combo_box()

    def _build_extra_widget(self):
        """Build ComboBoxes for selecting format, encoding and newlines."""

        self._frm_cmbox = gtk.combo_box_new_text()
        
        frm_label = gtk.Label()
        frm_label.set_property('xalign', 0)
        frm_label.set_markup_with_mnemonic(_('Fo_rmat:'))
        frm_label.set_mnemonic_widget(self._frm_cmbox)

        self._enc_cmbox = gtk.combo_box_new_text()
        self._enc_cmbox.connect('changed', self._on_encoding_changed)
        
        enc_label = gtk.Label()
        enc_label.set_property('xalign', 0)
        enc_label.set_markup_with_mnemonic(_('Character _encoding:'))
        enc_label.set_mnemonic_widget(self._enc_cmbox)

        self._nwl_cmbox = gtk.combo_box_new_text()
        
        nwl_label = gtk.Label()
        nwl_label.set_property('xalign', 0)
        nwl_label.set_markup_with_mnemonic(_('Ne_wlines:'))
        nwl_label.set_mnemonic_widget(self._nwl_cmbox)

        table = gtk.Table(3, 2)
        table.set_row_spacings(12)
        table.set_col_spacings(12)
        
        options = gtk.FILL
        table.attach(frm_label, 0, 1, 0, 1, options, options)
        table.attach(enc_label, 0, 1, 1, 2, options, options)
        table.attach(nwl_label, 0, 1, 2, 3, options, options)
        
        options = gtk.EXPAND|gtk.FILL
        table.attach(self._frm_cmbox, 1, 2, 0, 1, options, options)
        table.attach(self._enc_cmbox, 1, 2, 1, 2, options, options)
        table.attach(self._nwl_cmbox, 1, 2, 2, 3, options, options)

        table.show_all()
        self.set_extra_widget(table)
    
    def _fill_format_combo_box(self):
        """Insert items to format ComboBox."""

        for i in range(len(FORMATS)):
            self._frm_cmbox.append_text(FORMATS[i])

        format = self._config.get('file', 'format')
        self._frm_cmbox.set_active(FORMATS.index(format))

    def _fill_newlines_combo_box(self):
        """Insert items to newlines ComboBox."""

        for i in range(len(NEWLINES)):
            self._nwl_cmbox.append_text(NEWLINES[i])

        newlines = self._config.get('file', 'newlines')
        self._nwl_cmbox.set_active(NEWLINES.index(newlines))

    def get_format(self):
        """Get selected format."""

        return self._frm_cmbox.get_active_text()

    def get_newlines(self):
        """Get selected newlines."""

        return self._nwl_cmbox.get_active_text()

    def set_format(self, format):
        """Set active format in the format combo box."""

        try:
            self._frm_cmbox.set_active(FORMATS.index(format))
        except ValueError:
            pass

    def set_newlines(self, newlines):
        """Set active newlines in the newlines combo box."""
        
        try:
            self._nwl_cmbox.set_active(NEWLINES.index(newlines))
        except ValueError:
            pass
