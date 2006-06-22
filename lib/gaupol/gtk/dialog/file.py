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


"""Dialogs for selecting files."""


from gettext import gettext as _
import os

import gtk

from gaupol.base.util            import enclib, listlib
from gaupol.gtk                  import cons
from gaupol.gtk.dialog.encoding  import AdvancedEncodingDialog
from gaupol.gtk.dialog.message   import QuestionDialog
from gaupol.gtk.util             import conf, gtklib

try:
    import chardet
    _CHARDET_AVAILABLE = True
except ImportError:
    _CHARDET_AVAILABLE = False


class _OverwriteQuestionDialog(QuestionDialog):

    """Dialog for confirming overwrite."""

    def __init__(self, parent, basename):

        QuestionDialog.__init__(
            self, parent,
            _('A file named "%s" already exists') % basename,
            _('Do you want to replace it with the one you are saving?')
        )
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
        self.add_button(gtk.STOCK_SAVE_AS, gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)

        button = self.action_area.get_children()[0]
        alignment = button.get_children()[0]
        hbox = alignment.get_children()[0]
        label = hbox.get_children()[1]
        label.set_text(_('_Replace'))
        label.set_use_underline(True)


class _TextFileDialog(gtk.FileChooserDialog):

    """
    Base class for dialogs for selecting text files.

    Instance variables:

        _encodings: List of tuples: Python name, display name

    """

    def __init__(self, *args, **kwargs):

        gtk.FileChooserDialog.__init__(self, *args, **kwargs)

        self._encodings = None

        self._init_encodings()
        self._init_filters()

    def _init_encoding_data(self):
        """Initialize encoding combo box data."""

        model = self._encoding_combo.get_model()
        while len(model) > 0:
            self._encoding_combo.remove_text(0)
        for entry in self._encodings:
            self._encoding_combo.append_text(entry[1])

        self._encoding_combo.set_row_separator_func(gtklib.separate)

    def _init_encodings(self, custom=None):
        """Initialize encodings."""

        self._encodings = []

        encodings = conf.encoding.visibles[:]
        if custom is not None:
            encodings.append(custom)
        for encoding in encodings:
            try:
                name = enclib.get_long_name(encoding)
                self._encodings.append((encoding, name))
            except ValueError:
                pass

        def sort(x, y):
            return cmp(x[1], y[1])
        self._encodings.sort(sort)
        self._encodings = listlib.unique(self._encodings)
        if not self._encodings:
            self._encodings.append(('utf_8', enclib.get_long_name('utf_8')))

        try:
            encoding = enclib.get_locale_encoding()[0]
            name = enclib.get_locale_long_name()
        except ValueError:
            pass
        else:
            for i, entry in enumerate(self._encodings):
                if entry[0] == encoding:
                    self._encodings.pop(i)
                    break
            self._encodings.insert(0, (encoding, name))

        self._init_special_encodings()
        self._encodings.append((gtklib.COMBO_SEP, gtklib.COMBO_SEP))
        self._encodings.append(('other', _('Other...')))

    def _init_filters(self):
        """Initialize file filters."""

        file_filter = gtk.FileFilter()
        file_filter.set_name(_('All files'))
        file_filter.add_pattern('*')
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.set_name(_('Plain text files'))
        file_filter.add_mime_type('text/plain')
        self.add_filter(file_filter)

        for i, name in enumerate(cons.Format.display_names):
            pattern = '*' + cons.Format.extensions[i]
            # Translators: File filters, e.g. "SubRip (*.srt)".
            name = _('%s (%s)') % (name, pattern)
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            self.add_filter(file_filter)

    def _init_special_encodings(self):
        """Initialize special encodings."""

        pass

    def _on_encoding_combo_changed(self, *args):
        """Show encoding selection dialog."""

        if self.get_encoding() != 'other':
            return

        encoding = None
        dialog = AdvancedEncodingDialog(self)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            encoding = dialog.get_encoding()
            conf.encoding.visibles = dialog.get_visible_encodings()
        dialog.destroy()
        self.set_encoding(encoding)

    def get_encoding(self):
        """
        Get encoding.

        Return name or None.
        """
        index = self._encoding_combo.get_active()
        if index < 0:
            return None
        return self._encodings[index][0]

    def set_encoding(self, encoding):
        """Set encoding."""

        for i, entry in enumerate(self._encodings):
            if entry[0] == encoding:
                self._encoding_combo.set_active(i)
                return

        if encoding is not None and enclib.is_valid(encoding):
            self._init_encodings(encoding)
            self._init_encoding_data()
            return self.set_encoding(encoding)

        self._encoding_combo.set_active(0)


class OpenFileDialog(_TextFileDialog):

    """Dialog for selecting text files to open."""

    def __init__(self, title, parent):

        _TextFileDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN  , gtk.RESPONSE_OK     )
        )

        self._encoding_combo = None

        self._init_extra_widget()
        self._init_encoding_data()
        self._init_signals()

        self.set_encoding(conf.file.encoding)
        if conf.file.directory is not None:
            self.set_current_folder(conf.file.directory)
        self.set_default_response(gtk.RESPONSE_OK)

    def _init_extra_widget(self):
        """Initialize extra widget."""

        self._encoding_combo = gtk.combo_box_new_text()
        label = gtk.Label()
        label.set_markup_with_mnemonic(_('C_haracter encoding:'))
        label.set_mnemonic_widget(self._encoding_combo)

        hbox = gtk.HBox(False, 12)
        hbox.pack_start(label, False, True, 0)
        hbox.pack_start(self._encoding_combo, True , True, 0)
        hbox.show_all()
        self.set_extra_widget(hbox)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, self, 'response')
        gtklib.connect(self, '_encoding_combo', 'changed')

    def _init_special_encodings(self):
        """Initialize special encodings."""

        if _CHARDET_AVAILABLE:
            self._encodings.append((gtklib.COMBO_SEP, gtklib.COMBO_SEP))
            self._encodings.append(('auto', _('Auto-detected')))

    def _on_response(self, dialog, response):
        """Save settings."""

        if response != gtk.RESPONSE_OK:
            return

        conf.file.encoding  = self.get_encoding()
        conf.file.directory = self.get_current_folder()


class SaveFileDialog(_TextFileDialog):

    """Dialog for selecting text files to save."""

    def __init__(self, title, parent):

        _TextFileDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_SAVE  , gtk.RESPONSE_OK     )
        )

        self._format_combo   = None
        self._encoding_combo = None
        self._newline_combo  = None

        self._init_extra_widget()
        self._init_format_data()
        self._init_encoding_data()
        self._init_newline_data()
        self._init_signals()

        self.set_encoding(conf.file.encoding)
        self.set_format(conf.file.format)
        self.set_newlines(conf.file.newlines)
        if conf.file.directory is not None:
            self.set_current_folder(conf.file.directory)
        self.set_default_response(gtk.RESPONSE_OK)

    def _confirm_overwrite(self):
        """
        Add extension to filename and confirm overwrite.

        Return gtk.FILE_CHOOSER_CONFIRMATION constant.
        """
        path = self.get_full_filename()
        if not os.path.isfile(path):
            return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME

        basename = os.path.basename(path)
        response = gtklib.run(_OverwriteQuestionDialog(self, basename))
        if response == gtk.RESPONSE_YES:
            return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME
        return gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN

    def _init_extra_widget(self):
        """Initialize extra widget."""

        self._format_combo   = gtk.combo_box_new_text()
        self._encoding_combo = gtk.combo_box_new_text()
        self._newline_combo  = gtk.combo_box_new_text()

        format_label = gtk.Label()
        format_label.props.xalign = 0
        format_label.set_markup_with_mnemonic(_('Fo_rmat:'))
        format_label.set_mnemonic_widget(self._format_combo)

        encoding_label = gtk.Label()
        encoding_label.props.xalign = 0
        encoding_label.set_markup_with_mnemonic(_('C_haracter encoding:'))
        encoding_label.set_mnemonic_widget(self._encoding_combo)

        newline_label = gtk.Label()
        newline_label.props.xalign = 0
        newline_label.set_markup_with_mnemonic(_('Ne_wlines:'))
        newline_label.set_mnemonic_widget(self._newline_combo)

        table = gtk.Table(3, 2)
        table.set_row_spacings(6)
        table.set_col_spacings(12)

        options = gtk.FILL
        table.attach(format_label  , 0, 1, 0, 1, options, options)
        table.attach(encoding_label, 0, 1, 1, 2, options, options)
        table.attach(newline_label , 0, 1, 2, 3, options, options)

        options = gtk.EXPAND|gtk.FILL
        table.attach(self._format_combo  , 1, 2, 0, 1, options, options)
        table.attach(self._encoding_combo, 1, 2, 1, 2, options, options)
        table.attach(self._newline_combo , 1, 2, 2, 3, options, options)

        table.show_all()
        self.set_extra_widget(table)

    def _init_format_data(self):
        """Initialize format combo box data."""

        for name in cons.Format.display_names:
            self._format_combo.append_text(name)
        self._format_combo.set_active(0)

    def _init_newline_data(self):
        """Initialize newline combo box data."""

        for name in cons.Newlines.display_names:
            self._newline_combo.append_text(name)
        self._format_combo.set_active(0)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, self, 'response')
        gtklib.connect(self, '_format_combo', 'changed')
        gtklib.connect(self, '_encoding_combo', 'changed')

    def _on_format_combo_changed(self, combo_box):
        """Change extension."""

        path = self.get_filename()
        if path is None:
            return
        self.unselect_filename(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)

        for extension in cons.Format.extensions:
            if basename.endswith(extension):
                basename = basename[:-len(extension)]
                break

        format = combo_box.get_active()
        basename += cons.Format.extensions[format]
        path = os.path.join(dirname, basename)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_response(self, dialog, response):
        """Confirm overwrite and save settings."""

        if response != gtk.RESPONSE_OK:
            return

        confirmation = self._confirm_overwrite()
        if confirmation == gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN:
            return self.run()

        conf.file.directory = self.get_current_folder()
        conf.file.format    = self.get_format()
        conf.file.encoding  = self.get_encoding()
        conf.file.newlines  = self.get_newlines()

    def get_full_filename(self):
        """Get filename with extension."""

        path = self.get_filename()
        if path is None:
            return None

        extension = cons.Format.extensions[self.get_format()]
        if not path.endswith(extension):
            path += extension
        return path

    def get_format(self):
        """Get format."""

        return self._format_combo.get_active()

    def get_newlines(self):
        """Get newlines."""

        return self._newline_combo.get_active()

    def set_name(self, path):
        """Set filename or set current name."""

        if os.path.isfile(path):
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_format(self, format):
        """Set format."""

        try:
            self._format_combo.set_active(format)
        except (TypeError, ValueError):
            pass

    def set_newlines(self, newlines):
        """Set newlines."""

        try:
            self._newline_combo.set_active(newlines)
        except (TypeError, ValueError):
            pass


class OpenVideoDialog(gtk.FileChooserDialog):

    """Dialog for selecting video files."""

    def __init__(self, parent):

        gtk.FileChooserDialog.__init__(
            self, _('Select Video'), parent,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_OK    , gtk.RESPONSE_OK     ),
        )

        self._init_filters()

    def _init_filters(self):
        """Intialize file filters."""

        file_filter = gtk.FileFilter()
        file_filter.add_pattern('*')
        file_filter.set_name(_('All files'))
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.add_mime_type('video/*')
        file_filter.set_name(_('Video files'))
        self.add_filter(file_filter)
        self.set_filter(file_filter)
