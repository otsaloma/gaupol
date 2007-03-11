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


"""Saving documents."""


import gtk
import os
from gettext import gettext as _

from gaupol import enclib
from gaupol.base import Delegate
from gaupol.gtk import cons, util
from gaupol.gtk.dialogs import ErrorDialog, SaveDialog
from gaupol.gtk.errors import Default
from gaupol.gtk.index import *


class SaveAgent(Delegate):

    """Saving documents."""

    # pylint: disable-msg=E0203,W0201

    def _get_main_props(self, page):
        """Get path, format, encoding, newline of page's main file."""

        if page.project.main_file is not None:
            return [
                page.project.main_file.path,
                page.project.main_file.format,
                page.project.main_file.encoding,
                page.project.main_file.newline,]
        return [None, None, None, None]

    def _get_translation_props(self, page):
        """Get path, format, encoding, newline of page's translation file."""

        if page.project.tran_file is not None:
            return [
                page.project.tran_file.path,
                page.project.tran_file.format,
                page.project.tran_file.encoding,
                page.project.tran_file.newline,]
        if page.project.main_file is not None:
            return [
                None,
                page.project.main_file.format,
                page.project.main_file.encoding,
                page.project.main_file.newline,]
        return [None, None, None, None]

    def _save_document(self, page, doc, props):
        """Save document.

        Raise Default if something goes wrong.
        """
        util.set_cursor_busy(self.window)
        try:
            page.project.save(doc, props)
        except IOError, (no, message):
            util.set_cursor_normal(self.window)
            basename = os.path.basename(props[0])
            self._show_io_error_dialog(basename, message)
            raise Default
        except UnicodeError:
            util.set_cursor_normal(self.window)
            basename = os.path.basename(props[0])
            self._show_encoding_error_dialog(basename, props[2])
            raise Default
        finally:
            util.set_cursor_normal(self.window)

    @util.gc_collected
    def _select_file(self, title, props):
        """Select a file and return path, format, encoding, newline."""

        path, format, encoding, newline = props
        props = [None, None, None, None]
        util.set_cursor_busy(self.window)
        dialog = SaveDialog(title, self.window)
        dialog.set_name(path)
        dialog.set_format(format)
        dialog.set_encoding(encoding)
        dialog.set_newline(newline)
        util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        if response == gtk.RESPONSE_OK:
            props[0] = dialog.get_filename()
            props[1] = dialog.get_format()
            props[2] = dialog.get_encoding()
            props[3] = dialog.get_newline()
        dialog.destroy()
        while gtk.events_pending():
            gtk.main_iteration()
        return props

    def _show_encoding_error_dialog(self, basename, codec):
        """Show an error dialog after failing to encode file."""

        codec = enclib.get_display_name(codec)
        fields = {"filename": basename, "codec": codec}
        title = _('Failed to encode file "%(filename)s" '
            'with codec "%(codec)s"') % fields
        message = _("Please try to save the file with "
            "a different character encoding.")
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to write file."""

        title = _('Failed to save file "%s"') % basename
        message = _("%s.") % message
        dialog = ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def on_save_all_documents_activate(self, *args):
        """Save all open documents."""

        save_main = util.ignore_exceptions(Default)(self.save_main)
        save_tran = util.ignore_exceptions(Default)(self.save_translation)
        for page in self.pages:
            save_main(page)
            if page.project.tran_active:
                save_tran(page)
        self.push_message(_("Saved all open documents"))
        self.update_gui()

    @util.ignore_exceptions(Default)
    def on_save_main_document_activate(self, *args):
        """Save the current main document."""

        page = self.get_current_page()
        self.save_main(page)
        self.update_gui()

    @util.ignore_exceptions(Default)
    def on_save_main_document_as_activate(self, *args):
        """Save the current main document with a different name."""

        page = self.get_current_page()
        self.save_main_as(page)
        self.update_gui()

    @util.ignore_exceptions(Default)
    def on_save_translation_document_activate(self, *args):
        """Save the current translation document."""

        page = self.get_current_page()
        self.save_translation(page)
        self.update_gui()

    @util.ignore_exceptions(Default)
    def on_save_translation_document_as_activate(self, *args):
        """Save the current translation document with a different name."""

        page = self.get_current_page()
        self.save_translation_as(page)
        self.update_gui()

    def save_main(self, page):
        """Save the main document of page.

        Raise Default if something goes wrong.
        """
        props = self._get_main_props(page)
        if None in props:
            return self.save_main_as(page)
        self._save_document(page, cons.DOCUMENT.MAIN, props)
        self.push_message(_("Saved main document"))

    def save_main_as(self, page):
        """Save the main document of page to a selected file.

        Raise Default if something goes wrong.
        """
        props = self._get_main_props(page)
        if props[0] is None:
            props[0] = page.untitle
        orig_format = props[1]
        props = self._select_file(_("Save As"), props)
        if None in props:
            raise Default
        self._save_document(page, cons.DOCUMENT.MAIN, props)
        if orig_format is not None:
            if props[1] != orig_format:
                page.reload_view_all()
        self.add_to_recent_files(props[0], cons.DOCUMENT.MAIN)
        basename = os.path.basename(props[0])
        self.push_message(_('Saved main document as "%s"') % basename)

    def save_translation(self, page):
        """Save the translation document of page.

        Raise Default if something goes wrong.
        """
        props = self._get_translation_props(page)
        if None in props:
            return self.save_translation_as(page)
        self._save_document(page, cons.DOCUMENT.TRAN, props)
        self.push_message(_("Saved translation document"))

    def save_translation_as(self, page):
        """Save the translation document of page to a selected file.

        Raise Default if something goes wrong.
        """
        props = self._get_translation_props(page)
        if props[0] is None:
            props[0] = page.get_translation_corename()
        orig_format = props[1]
        props = self._select_file(_("Save Translation As"), props)
        if None in props:
            raise Default
        self._save_document(page, cons.DOCUMENT.TRAN, props)
        if orig_format is not None:
            if props[1] != orig_format:
                rows = range(len(page.project.times))
                page.reload_view(rows, [TTXT])
        self.add_to_recent_files(props[0], cons.DOCUMENT.TRAN)
        basename = os.path.basename(props[0])
        self.push_message(_('Saved translation document as "%s"') % basename)
