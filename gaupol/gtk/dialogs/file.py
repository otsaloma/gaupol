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


"""Dialogs for selecting files."""


import os
from gettext import gettext as _

import gtk

from gaupol import enclib
from gaupol.gtk import conf, cons, util
from gaupol.gtk.index import *
from gaupol.gtk.runner import Runner
from .encoding import AdvEncodingDialog


class _FileDialog(gtk.FileChooserDialog, Runner):

    """Base class for dialogs for selecting text files.

    Instance variables:

        _encodings: List of tuples: Python name, display name
    """

    # pylint: disable-msg=W0231
    def __init__(self, *args, **kwargs):

        gtk.FileChooserDialog.__init__(self, *args, **kwargs)

        self._encodings = []

        self._init_encodings()
        self._init_filters()

    def _init_encoding_data(self):
        """Initialize data in the encoding combo box."""

        # pylint: disable-msg=W0612
        store = self._encoding_combo.get_model()
        store.clear()
        for encoding, name in self._encodings:
            store.append([name])
        self._encoding_combo.set_row_separator_func(util.separate_combo)

    def _init_encodings(self, custom=None):
        """Initialize the encodings."""

        self._encodings = []
        locale = enclib.get_locale_python_name()
        if locale is not None:
            name = enclib.get_locale_long_name()
            self._encodings.append((locale, name))

        encodings = list(conf.encoding.visibles)
        if custom is not None:
            encodings.append(custom)
        for encoding in encodings:
            if encoding != locale and enclib.is_valid(encoding):
                name = enclib.get_long_name(encoding)
                self._encodings.append((encoding, name))

        def sort(x, y):
            return cmp(x[1], y[1])
        a = (0 if locale is None else 1)
        self._encodings[a:] = sorted(self._encodings[a:], sort)
        self._encodings = util.get_unique(self._encodings)
        if not self._encodings:
            name = enclib.get_long_name("utf_8")
            self._encodings.append(("utf_8", name))

        self._init_special_encodings()
        self._encodings.append((util.COMBO_SEP, util.COMBO_SEP))
        self._encodings.append(("other", _("Other...")))

    def _init_filters(self):
        """Initialize the file filters."""

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("Plain text files"))
        file_filter.add_mime_type("text/plain")
        self.add_filter(file_filter)

        for format in cons.FORMAT.members:
            pattern = "*" + format.extension
            fields = {"format": format.display_name, "extension": pattern}
            name = _("%(format)s (%(extension)s)") % fields
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            self.add_filter(file_filter)

    def _init_special_encodings(self):
        """Initialize any possible special encodings."""

        pass

    def _on_encoding_combo_changed(self, *args):
        """Show the encoding selection dialog."""

        if self.get_encoding() != "other":
            return
        encoding = None
        dialog = AdvEncodingDialog(self)
        response = self.run_dialog(dialog)
        if response == gtk.RESPONSE_OK:
            encoding = dialog.get_encoding()
            conf.encoding.visibles = dialog.get_visible_encodings()
        dialog.destroy()
        self.set_encoding(encoding)

    def get_encoding(self):
        """Get the encoding or None."""

        index = self._encoding_combo.get_active()
        if index < 0:
            return None
        return self._encodings[index][0]

    def set_encoding(self, encoding):
        """Set the encoding."""

        for i, seq in enumerate(self._encodings):
            if seq[0] == encoding:
                self._encoding_combo.set_active(i)
                return
        if encoding is not None and enclib.is_valid(encoding):
            self._init_encodings(encoding)
            self._init_encoding_data()
            return self.set_encoding(encoding)
        self._encoding_combo.set_active(0)


class OpenDialog(_FileDialog):

    """Dialog for selecting subtitle files to open.

    Instance variables:

        _encoding_combo: gtk.ComboBox
        _smart_check:    gtk.CheckButton
    """

    def __init__(self, doc, title, parent):

        _FileDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        self._encoding_combo = None
        self._smart_check    = None

        self._init_extra_widget(doc)
        self._init_encoding_data()
        self._init_data(doc)
        self._init_signal_handlers()
        self.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self, doc):
        """Initialize default values for widgets."""

        self.set_select_multiple(doc == cons.DOCUMENT.MAIN)
        if os.path.isdir(conf.file.directory):
            self.set_current_folder(conf.file.directory)
        self.set_encoding(conf.file.encoding)
        self._smart_check.set_active(conf.file.smart_tran)
        if all(conf.open_dialog.size):
            self.set_default_size(*conf.open_dialog.size)

    def _init_extra_widget(self, doc):
        """Initialize the extra widget."""

        glade_xml = util.get_glade_xml("open-box", "extra_widget")
        self._encoding_combo = glade_xml.get_widget("encoding_combo")
        self._smart_check = glade_xml.get_widget("smart_check")
        self._smart_check.props.visible = (doc == cons.DOCUMENT.TRAN)
        self.set_extra_widget(glade_xml.get_widget("extra_widget"))

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")
        util.connect(self, "_encoding_combo", "changed")

    def _init_special_encodings(self):
        """Initialize encoding auto-detection entries."""

        if util.chardet_available():
            self._encodings.append((util.COMBO_SEP, util.COMBO_SEP))
            self._encodings.append(("auto", _("Auto-detected")))

    def _on_response(self, dialog, response):
        """Save settings."""

        conf.file.encoding = self.get_encoding()
        conf.file.directory = self.get_current_folder()
        conf.file.smart_tran = self._smart_check.get_active()
        conf.open_dialog.size = self.get_size()


class AppendDialog(OpenDialog):

    """Dialog for selecting a subtitle file to append to project."""


    def __init__(self, parent):

        # pylint: disable-msg=E1101
        OpenDialog.__init__(
            self, cons.DOCUMENT.MAIN, _("Append File"), parent)

        self.set_select_multiple(False)
        button = self.action_area.get_children()[0]
        util.set_button(button, _("_Append"), gtk.STOCK_ADD)


class SaveDialog(_FileDialog):

    """Dialog for selecting a subtitle file to save.

    Instance variables:

        _encoding_combo: gtk.ComboBox
        _format_combo:   gtk.ComboBox
        _newline_combo:  gtk.ComboBox
    """

    def __init__(self, title, parent):

        _FileDialog.__init__(
            self, title, parent, gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        self._encoding_combo = None
        self._format_combo   = None
        self._newline_combo  = None

        self._init_extra_widget()
        self._init_format_data()
        self._init_encoding_data()
        self._init_newline_data()
        self._init_data()
        self._init_signal_handlers()
        self.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values for widgets."""

        self.set_do_overwrite_confirmation(True)
        if os.path.isdir(conf.file.directory):
            self.set_current_folder(conf.file.directory)
        self.set_encoding(conf.file.encoding)
        self.set_format(conf.file.format)
        self.set_newline(conf.file.newline)

    def _init_extra_widget(self):
        """Initialize the extra widget."""

        glade_xml = util.get_glade_xml("save-box", "extra_widget")
        self._encoding_combo = glade_xml.get_widget("encoding_combo")
        self._format_combo = glade_xml.get_widget("format_combo")
        self._newline_combo = glade_xml.get_widget("newline_combo")
        self.set_extra_widget(glade_xml.get_widget("extra_widget"))

    def _init_format_data(self):
        """Initialize data in the format combo box."""

        store = self._format_combo.get_model()
        store.clear()
        for name in cons.FORMAT.display_names:
            store.append([name])
        self._format_combo.set_active(0)

    def _init_newline_data(self):
        """Initialize data in the newline combo box."""

        store = self._newline_combo.get_model()
        store.clear()
        for name in cons.NEWLINE.display_names:
            store.append([name])
        self._newline_combo.set_active(0)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")
        util.connect(self, "_format_combo", "changed")
        util.connect(self, "_encoding_combo", "changed")

        def update(*args):
            self._format_combo.emit("changed")
        # pylint: disable-msg=E1101
        save_button = self.action_area.get_children()[0]
        save_button.connect("event", update)

    def _on_format_combo_changed(self, combo_box):
        """Change the extension of the current filename."""

        path = self.get_filename()
        if path is None:
            return
        self.unselect_filename(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        for extension in cons.FORMAT.extensions:
            if basename.endswith(extension):
                basename = basename[:-len(extension)]
                break
        format = cons.FORMAT.members[combo_box.get_active()]
        basename += format.extension
        path = os.path.join(dirname, basename)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_response(self, dialog, response):
        """Save settings."""

        conf.file.directory = self.get_current_folder()
        conf.file.encoding = self.get_encoding()
        conf.file.format = self.get_format()
        conf.file.newline = self.get_newline()

    def get_format(self):
        """Get the format."""

        index = self._format_combo.get_active()
        return cons.FORMAT.members[index]

    def get_newline(self):
        """Get the newline."""

        index = self._newline_combo.get_active()
        return cons.NEWLINE.members[index]

    def set_format(self, format):
        """Set the format."""

        self._format_combo.set_active(format)

    def set_name(self, path):
        """Set either filename or current name."""

        if os.path.isfile(path):
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_newline(self, newline):
        """Set the newline."""

        self._newline_combo.set_active(newline)


class VideoDialog(gtk.FileChooserDialog):

    """Dialog for selecting a video file."""

    def __init__(self, parent):

        gtk.FileChooserDialog.__init__(
            self, _("Select Video"), parent, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             _("_Select"), gtk.RESPONSE_OK))

        self._init_filters()

    def _init_filters(self):
        """Intialize the file filters."""

        file_filter = gtk.FileFilter()
        file_filter.add_pattern("*")
        file_filter.set_name(_("All files"))
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.add_mime_type("video/*")
        file_filter.set_name(_("Video files"))
        self.add_filter(file_filter)
        self.set_filter(file_filter)
