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

from gaupol.base.util            import enclib
from gaupol.gtk                  import cons
from gaupol.gtk.dialog.encoding  import AdvancedEncodingDialog
from gaupol.gtk.dialog.message   import QuestionDialog
from gaupol.gtk.util             import config


class OverwriteQuestionDialog(QuestionDialog):

    """Dialog to ask whether to overwrite existing file or not."""

    def __init__(self, parent, basename):

        title = _('A file named "%s" already exists') % basename
        message = _('Do you want to replace it with the one you are saving?')
        QuestionDialog.__init__(self, parent, title, message)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(_('_Replace')   , gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)


class TextFileChooserDialog(gtk.FileChooserDialog):

    """Base class for dialogs for selecting text files."""

    def __init__(self, *args, **kwargs):

        gtk.FileChooserDialog.__init__(self, *args, **kwargs)

        self._encodings       = None
        self._locale_encoding = None

        self._init_locale_encoding()
        self._init_encodings()
        self._init_filters()

    def _init_encodings(self):
        """Initialize encodings."""

        self._encodings = []
        for encoding in config.Encoding.visible:
            try:
                name = enclib.get_long_name(encoding)
                self._encodings.append((encoding, name))
            except ValueError:
                pass

        if config.File.encoding is not None:
            found = False
            for encoding, name in self._encodings:
                if encoding == config.File.encoding:
                    found = True
                    break
            if not found:
                try:
                    encoding = config.File.encoding
                    name = enclib.get_long_name(encoding)
                    self._encodings.append((encoding, name))
                except ValueError:
                    pass

        def sort(x, y):
            return cmp(x[1], y[1])
        self._encodings.sort(sort)

        if self._locale_encoding is not None:
            for i, entry in enumerate(self._encodings):
                if entry[0] == self._locale_encoding[0]:
                    self._encodings.pop(i)
                    break
            self._encodings.insert(0, self._locale_encoding)

    def _init_encoding_data(self):
        """Initialize encoding combo box data."""

        while self._encoding_combo.get_active_text() is not None:
            self._encoding_combo.remove_text(0)

        for entry in self._encodings:
            self._encoding_combo.append_text(entry[1])
        self._encoding_combo.append_text('--')
        self._encoding_combo.append_text(_('Other...'))

        def set_row_separator(store, iter_):
            row = store.get_path(iter_)[0]
            return row == len(store) - 2
        self._encoding_combo.set_row_separator_func(set_row_separator)

        self.set_encoding(config.File.encoding)

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

    def _init_locale_encoding(self):
        """Initialize locale encoding."""

        try:
            encoding = enclib.get_locale_encoding()[0]
            name = enclib.get_locale_long_name()
            self._locale_encoding = (encoding, name)
        except ValueError:
            pass

    def get_encoding(self):
        """
        Get selected encoding.

        Return name or None.
        """
        index = self._encoding_combo.get_active()
        try:
            return self._encodings[index][0]
        except IndexError:
            return None

    def _on_current_folder_changed(self, *args):
        """Save directory."""

        config.File.directory = self.get_current_folder()

    def _on_encoding_combo_changed(self, combo_box):
        """Save encoding or show encoding dialog."""

        encoding = self.get_encoding()
        if encoding is not None:
            config.File.encoding = encoding
            return

        dialog = AdvancedEncodingDialog(self)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            try:
                config.File.encoding = dialog.get_encoding()
            except ValueError:
                pass
            config.Encoding.visible = dialog.get_visible_encodings()
        dialog.destroy()

        self._init_encodings()
        self._init_encoding_data()

    def set_encoding(self, encoding):
        """Set active encoding."""

        for i, entry in enumerate(self._encodings):
            if entry[0] == encoding:
                self._encoding_combo.set_active(i)
                return

        index = self._encoding_combo.get_active()
        if index not in range(len(self._encodings)):
            self._encoding_combo.set_active(0)


class OpenFileDialog(TextFileChooserDialog):

    """Dialog for selecting text files to open."""

    def __init__(self, title, parent):

        TextFileChooserDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN  , gtk.RESPONSE_OK     )
        )

        self._encoding_combo = None

        self._init_extra_widget()
        self._init_encoding_data()
        self._init_signals()

        if config.File.directory is not None:
            self.set_current_folder(config.File.directory)
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

        self.connect('current-folder-changed', self._on_current_folder_changed)
        self._encoding_combo.connect(
            'changed', self._on_encoding_combo_changed)


class SaveFileDialog(TextFileChooserDialog):

    """Dialog for selecting text files to save."""

    def __init__(self, title, parent):

        TextFileChooserDialog.__init__(
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

        self.set_format(config.File.format)
        self.set_newlines(config.File.newlines)
        if config.File.directory is not None:
            self.set_current_folder(config.File.directory)
        self.set_default_response(gtk.RESPONSE_OK)

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

        self.connect('current-folder-changed', self._on_current_folder_changed)
        self.connect('response', self._on_response)

        self._format_combo.connect('changed', self._on_format_combo_changed)
        self._encoding_combo.connect(
            'changed', self._on_encoding_combo_changed)
        self._newline_combo.connect('changed', self._on_newline_combo_changed)

    def _confirm_overwrite(self):
        """
        Add extension to filename for confirming overwrite.

        Return gtk.FILE_CHOOSER_CONFIRMATION constant.
        """
        filepath = self.get_filename_with_extension()
        if not os.path.isfile(filepath):
            return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME

        dialog = OverwriteQuestionDialog(self, os.path.basename(filepath))
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME
        else:
            return gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN

    def get_filename_with_extension(self):
        """Get selected filename with extension."""

        path = self.get_filename()
        if path is None:
            return None

        extension = cons.Format.extensions[self.get_format()]
        if not path.endswith(extension):
            path += extension
        return path

    def get_format(self):
        """Get selected format."""

        return self._format_combo.get_active()

    def get_newlines(self):
        """Get selected newlines."""

        return self._newline_combo.get_active()

    def _on_format_combo_changed(self, combo_box):
        """Save format and change extension."""

        format = combo_box.get_active()
        config.File.format = format
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

        basename += cons.Format.extensions[format]
        path = os.path.join(dirname, basename)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_newline_combo_changed(self, combo_box):
        """Save newlines."""

        config.File.newlines = combo_box.get_active()

    def _on_response(self, dialog, response):
        """Add extension and confirm overwrite."""

        if response == gtk.RESPONSE_OK:
            confirmation = self._confirm_overwrite()
            if confirmation == gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN:
                return self.run()

    def set_filename_or_current_name(self, path):
        """Select file or set current name."""

        if os.path.isfile(path):
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_format(self, format):
        """Set active format."""

        try:
            self._format_combo.set_active(format)
        except (TypeError, ValueError):
            pass

    def set_newlines(self, newlines):
        """Set active newlines."""

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
