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


"""Saving documents."""


from gettext import gettext as _
import os

import gtk

from gaupol.base.util          import enclib
from gaupol.gtk.icons          import *
from gaupol.gtk.delegate       import Delegate, UIMAction
from gaupol.gtk.dialog.file    import SaveFileDialog
from gaupol.gtk.dialog.header  import HeaderDialog
from gaupol.gtk.dialog.message import ErrorDialog
from gaupol.gtk.error          import Default
from gaupol.gtk.util           import gtklib


class EditHeadersAction(UIMAction):

    """Edit subtitle file headers."""

    action_item = (
        'edit_headers',
        gtk.STOCK_PROPERTIES,
        _('_Headers'),
        '<alt>Return',
        _('Edit file headers'),
        'on_edit_headers_activate'
    )

    paths = ['/ui/menubar/file/headers']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False

        main_file = page.project.main_file
        tran_file = page.project.tran_file
        if main_file is not None:
            if main_file.has_header:
                return True
        if tran_file is not None:
            if tran_file.has_header:
                return True

        return False


class _SaveAction(UIMAction):

    """Base class for save actions."""

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        return page is not None


class SaveAllDocumentsAction(_SaveAction):

    """Saving all documents."""

    action_item = (
        'save_all_documents',
        gtk.STOCK_SAVE,
        _('_Save All'),
        '<shift><control>L',
        _('Save all open documents'),
        'on_save_all_documents_activate'
    )

    paths = ['/ui/menubar/projects/save_all']


class SaveMainDocumentAction(_SaveAction):

    """Saving main document."""

    action_item = (
        'save_main_document',
        gtk.STOCK_SAVE,
        _('_Save'),
        '<control>S',
        _('Save the current main document'),
        'on_save_main_document_activate'
    )

    paths = ['/ui/menubar/file/save', '/ui/main_toolbar/save']


class SaveMainDocumentAsAction(_SaveAction):

    """Saving main document with a different name."""

    action_item = (
        'save_main_document_as',
        gtk.STOCK_SAVE_AS,
        _('Save _As...'),
        '<shift><control>S',
        _('Save the current main document with a different name'),
        'on_save_main_document_as_activate'
    )

    paths = ['/ui/menubar/file/save_as']


class SaveTranslationDocumentAction(_SaveAction):

    """Saving translation document."""

    action_item = (
        'save_translation_document',
        gtk.STOCK_SAVE,
        _('Sav_e Translation'),
        '<control>T',
        _('Save the current translation document'),
        'on_save_translation_document_activate'
    )

    paths = ['/ui/menubar/file/save_translation']


class SaveTranslationDocumentAsAction(_SaveAction):

    """Saving translation document with a different name."""

    action_item = (
        'save_translation_document_as',
        gtk.STOCK_SAVE_AS,
        _('Save _Translation As...'),
        '<shift><control>T',
        _('Save the current translation document with a different name'),
        'on_save_translation_document_as_activate'
    )

    paths = ['/ui/menubar/file/save_translation_as']


class _IOErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while saving file."""

    def __init__(self, parent, basename, message):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to save file "%s"') % basename,
            _('%s.') % message
        )


class _UnicodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while saving file."""

    def __init__(self, parent, basename, codec):

        ErrorDialog.__init__(
            self, parent,
            _('Failed to encode file "%s" with codec "%s"') % (
                basename, enclib.get_display_name(codec)),
            _('Please try to save the file with a different character '
              'encoding.')
        )


class FileSaveDelegate(Delegate):

    """Saving documents."""

    def _get_main_props(self, page):
        """
        Get properties of main file.

        Return four-tuple: path, format, encoding, newlines.
        """
        try:
            return (
                page.project.main_file.path,
                page.project.main_file.format,
                page.project.main_file.encoding,
                page.project.main_file.newlines,
            )
        except AttributeError:
            return (None, None, None, None)

    def _get_translation_props(self, page):
        """
        Get properties of translation file.

        Return four-tuple: path, format, encoding, newlines.
        """
        if page.project.tran_file is not None:
            return (
                page.project.tran_file.path,
                page.project.tran_file.format,
                page.project.tran_file.encoding,
                page.project.tran_file.newlines,
            )
        elif page.project.main_file is not None:
            return (
                page.project.main_file.path,
                page.project.main_file.format,
                page.project.main_file.encoding,
                page.project.main_file.newlines,
            )
        else:
            return (None, None, None, None)

    def _save_file(self, page, doc, parent, props):
        """
        Write file.

        props: Path, format, encoding, newlines
        Raise Default if unsuccessful.
        """
        path, format, encoding, newlines = props
        basename = os.path.basename(path)
        try:
            if doc == MAIN:
                page.project.save_main_file(props)
            elif doc == TRAN:
                page.project.save_translation_file(props)
        except IOError, (no, message):
            gtklib.run(_IOErrorDialog(parent, basename, message))
            raise Default
        except UnicodeError:
            encoding = enclib.get_display_name(encoding)
            gtklib.run(_UnicodeErrorDialog(parent, basename, encoding))
            raise Default

    def _select_file(self, title, props):
        """
        Select a file with filechooser.

        props: Path, format, encoding, newlines
        Raise Default if cancelled.
        Return path, format, encoding, newlines.
        """
        path, format, encoding, newlines = props
        dialog = SaveFileDialog(title, self._window)
        dialog.set_name(path)
        dialog.set_format(format)
        dialog.set_encoding(encoding)
        dialog.set_newlines(newlines)
        gtklib.set_cursor_normal(self._window)
        response = dialog.run()
        gtklib.set_cursor_busy(self._window)
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(dialog)
            raise Default

        props = (
            dialog.get_full_filename(),
            dialog.get_format(),
            dialog.get_encoding(),
            dialog.get_newlines(),
        )
        gtklib.destroy_gobject(dialog)
        return props

    def on_edit_headers_activate(self, *args):
        """Edit subtitle file headers."""

        page = self.get_current_page()
        gtklib.run(HeaderDialog(self._window, page.project))

    def on_save_all_documents_activate(self, *args):
        """Save all documents."""

        for page in self.pages:
            try:
                self.save_main(page)
            except Default:
                pass
            if page.project.tran_active:
                try:
                    self.save_translation(page)
                except Default:
                    pass
            page.update_tab_labels()
        self.set_sensitivities()
        self.set_status_message(_('Saved all open documents'))

    def on_save_main_document_activate(self, *args):
        """Save main document."""

        page = self.get_current_page()
        try:
            self.save_main(page)
        except Default:
            pass
        self.set_sensitivities()

    def on_save_main_document_as_activate(self, *args):
        """Save main document to a selected file."""

        page = self.get_current_page()
        try:
            self.save_main_as(page)
        except Default:
            pass
        self.set_sensitivities()

    def on_save_translation_document_activate(self, *args):
        """Save translation document."""

        page = self.get_current_page()
        try:
            self.save_translation(page)
        except Default:
            pass
        self.set_sensitivities()

    def on_save_translation_document_as_activate(self, *args):
        """Save translation document to a selected file."""

        page = self.get_current_page()
        try:
            self.save_translation_as(page)
        except Default:
            pass
        self.set_sensitivities()

    def save_main(self, page):
        """
        Save main document.

        Raise Default in unsuccessful.
        """
        props = self._get_main_props(page)
        if None in props:
            return self.save_main_as(page)
        self._save_file(page, MAIN, self._window, props)
        self.set_status_message(_('Saved main document'))

    def save_main_as(self, page):
        """
        Save main document to a selected file.

        Raise Default in unsuccessful.
        """
        gtklib.set_cursor_busy(self._window)
        props = self._get_main_props(page)
        path, format, encoding, newlines = props
        orig_format = format
        if path is None:
            props = page.untitle, format, encoding, newlines
        try:
            props = self._select_file(_('Save As'), props)
            self._save_file(page, MAIN, self._window, props)
        except Default:
            gtklib.set_cursor_normal(self._window)
            raise

        path, format, encoding, newlines = props
        if orig_format is not None:
            if format != orig_format:
                page.reload_all()
        if page.project.video_path is None:
            page.project.guess_video_path()

        self.add_to_recent_files(path)
        self.set_status_message(
            _('Saved main document as "%s"') % os.path.basename(path))
        gtklib.set_cursor_normal(self._window)

    def save_translation(self, page):
        """
        Save translation document.

        Raise Default in unsuccessful.
        """
        props = self._get_translation_props(page)
        if None in props:
            return self.save_translation_as(page)
        self._save_file(page, TRAN, self._window, props)
        self.set_status_message(_('Saved translation document'))

    def save_translation_as(self, page):
        """
        Save translation document to a selected file.

        Raise Default in unsuccessful.
        """
        gtklib.set_cursor_busy(self._window)
        props = self._get_translation_props(page)
        path, format, encoding, newlines = props
        orig_format = format
        if path is None:
            path = page.get_translation_corename()
            props = path, format, encoding, newlines
        try:
            props = self._select_file(_('Save Translation As'), props)
            self._save_file(page, MAIN, self._window, props)
        except Default:
            gtklib.set_cursor_normal(self._window)
            raise

        path, format, encoding, newlines = props
        if orig_format is not None:
            if format != orig_format:
                page.reload_columns([TTXT])
        if page.project.video_path is None:
            page.project.guess_video_path()

        self.add_to_recent_files(path)
        self.set_status_message(
            _('Saved translation document as "%s"') % os.path.basename(path))
        gtklib.set_cursor_normal(self._window)
