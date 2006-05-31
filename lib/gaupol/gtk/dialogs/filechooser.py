# Copyright (C) 2005 Osmo Salomaa
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


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import os

import gtk

from gaupol.base.util            import encodinglib
from gaupol.gtk.cons import *
from gaupol.gtk.dialogs.encoding import AdvancedEncodingDialog
from gaupol.gtk.dialogs.message  import QuestionDialog
from gaupol.gtk.util             import config


class OverwriteQuestionDialog(QuestionDialog):

    """Dialog to ask whether to overwrite existing file or not."""

    def __init__(self, parent, basename):

        title   = _('A file named "%s" already exists') % basename
        message = _('Do you want to replace it with the one you are saving?')
        QuestionDialog.__init__(self, parent, title, message)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(_('_Replace')   , gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)


class TextFileChooserDialog(gtk.FileChooserDialog):

    """Base class for custom dialogs for selecting text files."""

    def __init__(self, *args, **kwargs):

        gtk.FileChooserDialog.__init__(self, *args, **kwargs)

        # List of tuples (python name, descriptive name)
        self._encodings = None

        # Tuple (python name, descriptive name)
        self._locale_encoding = None

        self._init_locale_encoding()
        self._init_encodings()
        self._init_filters()

    def _init_encodings(self):
        """Initialize encodings."""

        self._encodings = []

        for encoding in config.encoding.visibles:
            try:
                name = encodinglib.get_descriptive_name(encoding)
                self._encodings.append((encoding, name))
            except ValueError:
                pass

        if config.file.encoding is not None:
            found = False
            for encoding, name in self._encodings:
                if encoding == config.file.encoding:
                    found = True
                    break
            if not found:
                try:
                    encoding = config.file.encoding
                    name = encodinglib.get_descriptive_name(encoding)
                    self._encodings.insert(0, (encoding, name))
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

        for encoding, name in self._encodings:
            self._encoding_combo.append_text(name)
        self._encoding_combo.append_text('--')
        self._encoding_combo.append_text(_('Other...'))

        def func(store, iter):
            row = store.get_path(iter)[0]
            return row == len(store) - 2
        self._encoding_combo.set_row_separator_func(func)

        self.set_encoding(config.file.encoding)

    def _init_filters(self):
        """Initialize file filters."""

        filters = [
            (_('All files')       , None        , '*' ),
            (_('Plain text files'), 'text/plain', None),
        ]

        for i, format_name in enumerate(Format.display_names):
            pattern = '*' + Format.extensions[i]
            # Translators: File filters, e.g. "SubRip (*.srt)".
            name = _('%s (%s)') % (format_name, pattern)
            filters.append((name, None, pattern))

        for name, mime, pattern in filters:
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            if mime is not None:
                file_filter.add_mime_type(mime)
            if pattern is not None:
                file_filter.add_pattern(pattern)
            self.add_filter(file_filter)

    def _init_locale_encoding(self):
        """Initialize locale encoding."""

        try:
            encoding = encodinglib.get_locale_encoding()[0]
            name = encodinglib.get_locale_descriptive_name()
            self._locale_encoding = encoding, name
        except ValueError:
            pass

    def get_encoding(self):
        """Get the selected encoding."""

        index = self._encoding_combo.get_active()
        try:
            return self._encodings[index][0]
        except IndexError:
            return None

    def _on_current_folder_changed(self, *args):
        """Save directory setting."""

        config.file.directory = self.get_current_folder()

    def _on_encoding_combo_changed(self, combo_box):
        """Save encoding setting or show encoding dialog."""

        encoding = self.get_encoding()
        if encoding is not None:
            config.file.encoding = encoding

        if combo_box.get_active() != len(combo_box.props.model) - 1:
            return

        dialog = AdvancedEncodingDialog(self)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            encoding = dialog.get_encoding()
            if encoding is not None:
                config.file.encoding = encoding
            config.encoding.visibles = dialog.get_visible_encodings()
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

        if config.file.directory is not None:
            self.set_current_folder(config.file.directory)
        self.set_default_response(gtk.RESPONSE_OK)

    def _init_extra_widget(self):
        """Initialize the filechooser extra widget area."""

        self._encoding_combo = gtk.combo_box_new_text()
        label = gtk.Label()
        label.set_markup_with_mnemonic(_('Character _encoding:'))
        label.set_mnemonic_widget(self._encoding_combo)

        hbox = gtk.HBox(False, 12)
        hbox.pack_start(label, False, True, 0)
        hbox.pack_start(self._encoding_combo, True , True, 0)
        hbox.show_all()
        self.set_extra_widget(hbox)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_current_folder_changed
        self.connect('current-folder-changed', method)

        method = self._on_encoding_combo_changed
        self._encoding_combo.connect('changed', method)


class SaveFileDialog(TextFileChooserDialog):

    """Dialog for selecting text files to save."""

    # NOTE:
    # The stock overwrite dialog seems to be broken. Furthermore, the
    # "confirm-overwrite" signal is emitted before we get a chance to add an
    # extension to the filename. Therefore, we do confirming manually by
    # intercepting the "response" signal. These practices can be re-evaluated
    # in future PyGTK releases if things change. Especially the stock dialog
    # could be good HIG-wise, currently I don't even know what it looks like.

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

        self.set_format(config.file.format)
        self.set_newlines(config.file.newlines)

        self.set_current_folder(config.file.directory)
        self.set_default_response(gtk.RESPONSE_OK)

    def _init_extra_widget(self):
        """Initialize the filechooser extra widget area."""

        self._format_combo   = gtk.combo_box_new_text()
        self._encoding_combo = gtk.combo_box_new_text()
        self._newline_combo  = gtk.combo_box_new_text()

        format_label = gtk.Label()
        format_label.props.xalign = 0
        format_label.set_markup_with_mnemonic(_('Fo_rmat:'))
        format_label.set_mnemonic_widget(self._format_combo)

        encoding_label = gtk.Label()
        encoding_label.props.xalign = 0
        encoding_label.set_markup_with_mnemonic(_('Character _encoding:'))
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

        for name in Format.display_names:
            self._format_combo.append_text(name)
        self._format_combo.set_active(0)

    def _init_newline_data(self):
        """Initialize newline combo box data."""

        for name in Newlines.display_names:
            self._newline_combo.append_text(name)
        self._format_combo.set_active(0)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_current_folder_changed
        self.connect('current-folder-changed', method)
        method = self._on_response
        self.connect('response', method)

        method = self._on_format_combo_changed
        self._format_combo.connect('changed', method)
        method = self._on_encoding_combo_changed
        self._encoding_combo.connect('changed', method)
        method = self._on_newline_combo_changed
        self._newline_combo.connect('changed', method)

    def _confirm_overwrite(self):
        """
        Add extension to filename when confirming overwrite.

        Return a gtk.FILE_CHOOSER_CONFIRMATION constant.
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
        """Return filename with extension."""

        path = TextFileChooserDialog.get_filename(self)
        if path is None:
            return None

        extension = Format.extensions[self.get_format()]
        if not path.endswith(extension):
            path += extension
        return path

    def get_format(self):
        """Get the selected format."""

        return self._format_combo.get_active()

    def get_newlines(self):
        """Get the selected newlines."""

        return self._newline_combo.get_active()

    def _on_format_combo_changed(self, combo_box):
        """Save format setting and change extension."""

        new_format = combo_box.get_active()
        config.file.format = new_format

        path = self.get_filename()
        if path is None:
            return

        self.unselect_filename(path)
        dirname  = os.path.dirname(path)
        basename = os.path.basename(path)

        # Remove possible existing extension.
        for extension in Format.extensions:
            if basename.endswith(extension):
                basename = basename[:-len(extension)]
                break

        # Add new extension.
        basename += Format.extensions[new_format]
        path = os.path.join(dirname, basename)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_newline_combo_changed(self, combo_box):
        """Save newline setting."""

        config.file.newlines = combo_box.get_active()

    def _on_response(self, dialog, response):
        """Add extension and confirm overwrite before emitting response."""

        if response == gtk.RESPONSE_OK:
            confirmation = self._confirm_overwrite()
            if confirmation == gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN:
                return self.run()

    def set_filename_or_current_name(self, path):
        """Select file at path or set path as current name."""

        if os.path.isfile(path):
            self.set_filename(path)
        else:
            self.set_current_name(path)

    def set_format(self, format):
        """Set the active format."""

        try:
            self._format_combo.set_active(format)
        except (TypeError, ValueError):
            pass

    def set_newlines(self, newlines):
        """Set the active newlines."""

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
        self.set_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.add_mime_type('video/*')
        file_filter.set_name(_('Video files'))
        self.add_filter(file_filter)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestOverwriteQuestionDialog(Test):

        def test_init(self):

            OverwriteQuestionDialog(gtk.Window(), 'test')

    class TestOpenFileDialog(Test):

        def test_set_and_get_encoding(self):

            dialog = OpenFileDialog('test', gtk.Window())
            dialog.set_encoding('utf_8')
            assert dialog.get_encoding() == 'utf_8'

    class TestSaveFileDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.dialog = SaveFileDialog('test', gtk.Window())

        def destroy(self):

            self.dialog.destroy()

        def test_confirm_overwrite(self):

            self.dialog.set_current_name('test')
            self.dialog.emit('response', gtk.RESPONSE_OK)

            self.dialog.set_format(Format.SUBRIP)
            path = self.get_subrip_path()
            self.dialog.set_filename(path)
            self.dialog.set_current_name(os.path.basename(path))
            self.dialog.emit('response', gtk.RESPONSE_OK)

        def test_get_and_set_format(self):

            self.dialog.set_current_name('test')
            self.dialog.set_format(Format.MPL2)

            self.dialog.set_format(Format.SUBRIP)
            name = os.path.basename(self.dialog.get_filename())
            assert name == 'test.srt'

            self.dialog.set_format(Format.MICRODVD)
            name = os.path.basename(self.dialog.get_filename())
            assert name == 'test.sub'

            self.dialog.set_format(1)
            assert self.dialog.get_format() == 1

        def test_get_and_set_newlines(self):

            self.dialog.set_newlines(1)
            assert self.dialog.get_newlines() == 1

        def test_get_filename_with_extension(self):

            self.dialog.set_current_name('test')
            self.dialog.set_format(Format.SUBRIP)
            get_name = self.dialog.get_filename_with_extension
            assert get_name().endswith('test.srt')

        def test_set_filename_or_current_name(self):

            self.dialog.set_filename_or_current_name(self.get_subrip_path())
            self.dialog.set_filename_or_current_name('test')

    class TestOpenVideoDialog(Test):

        def test_init(self):

            OpenVideoDialog(gtk.Window())

    TestOverwriteQuestionDialog().run()
    TestOpenFileDialog().run()
    TestSaveFileDialog().run()
    TestOpenVideoDialog().run()
