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


"""Saving documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import os

import gtk

from gaupol.base.util               import encodinglib
from gaupol.base.cons               import Document
from gaupol.gtk.cons        import *
from gaupol.gtk.delegates           import Delegate, UIMAction
from gaupol.gtk.dialogs.filechooser import SaveFileDialog
from gaupol.gtk.dialogs.header      import HeaderDialog
from gaupol.gtk.dialogs.message     import ErrorDialog
from gaupol.gtk.error               import Cancelled
from gaupol.gtk.util                import config, gtklib


class EditHeadersAction(UIMAction):

    """Edit subtitle file headers."""

    uim_action_item = (
        'edit_headers',
        gtk.STOCK_PROPERTIES,
        _('_Headers...'),
        '<alt>Return',
        _('Edit file headers'),
        'on_edit_headers_activated'
    )

    uim_paths = ['/ui/menubar/file/headers']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        main_file = page.project.main_file
        tran_file = page.project.tran_file

        if main_file is not None and main_file.has_header:
            return True
        if tran_file is not None and tran_file.has_header:
            return True

        return False


class SaveAction(UIMAction):

    """Saving a document."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return page is not None


class SaveAllDocumentsAction(SaveAction):

    """Saving all documents of all projects."""

    uim_action_item = (
        'save_all_documents',
        gtk.STOCK_SAVE,
        _('_Save All'),
        '<shift><control>L',
        _('Save all open documents'),
        'on_save_all_documents_activated'
    )

    uim_paths = ['/ui/menubar/projects/save_all']


class SaveMainDocumentAction(SaveAction):

    """Saving the current main document."""

    uim_action_item = (
        'save_main_document',
        gtk.STOCK_SAVE,
        _('_Save'),
        '<control>S',
        _('Save the current main document'),
        'on_save_main_document_activated'
    )

    uim_paths = ['/ui/menubar/file/save', '/ui/main_toolbar/save']


class SaveMainDocumentAsAction(SaveAction):

    """Saving the current main document as."""

    uim_action_item = (
        'save_main_document_as',
        gtk.STOCK_SAVE_AS,
        _('Save _As...'),
        '<shift><control>S',
        _('Save the current main document with a different name'),
        'on_save_main_document_as_activated'
    )

    uim_paths = ['/ui/menubar/file/save_as']


class SaveACopyOfMainDocumentAction(SaveAction):

    """Saving a copy of the current main document."""

    uim_action_item = (
        'save_a_copy_of_main_document',
        None,
        _('Sa_ve A Copy...'),
        None,
        _('Save a copy of the current main document'),
        'on_save_a_copy_of_main_document_activated'
    )

    uim_paths = ['/ui/menubar/file/save_a_copy']


class SaveTranslationDocumentAction(SaveAction):

    """Saving the current translation document."""

    uim_action_item = (
        'save_translation_document',
        gtk.STOCK_SAVE,
        _('Sav_e Translation'),
        '<control>T',
        _('Save the current translation document'),
        'on_save_translation_document_activated'
    )

    uim_paths = ['/ui/menubar/file/save_translation']


class SaveTranslationDocumentAsAction(SaveAction):

    """Saving the current translation document as."""

    uim_action_item = (
        'save_translation_document_as',
        gtk.STOCK_SAVE_AS,
        _('Save _Translation As...'),
        '<shift><control>T',
        _('Save the current translation document with a different name'),
        'on_save_translation_document_as_activated'
    )

    uim_paths = ['/ui/menubar/file/save_translation_as']


class SaveACopyOfTranslationDocumentAction(SaveAction):

    """Saving a copy of the current translation document."""

    uim_action_item = (
        'save_a_copy_of_translation_document',
        None,
        _('Save A Cop_y Of Translation...'),
        None,
        _('Save a copy of the current translation document.'),
        'on_save_a_copy_of_translation_document_activated'
    )

    uim_paths = ['/ui/menubar/file/save_a_copy_of_translation']


class SaveFileErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while saving file."""

    def __init__(self, parent, basename, message):

        title   = _('Failed to save file "%s"') % basename
        message = _('%s.') % message
        ErrorDialog.__init__(self, parent, title, message)


class UnicodeEncodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while saving file."""

    def __init__(self, parent, basename, codec):

        title   = _('Failed to encode file "%s" with codec "%s"') \
                  % (basename, codec)
        message = _('Please try to save the file with a different character '
                   'encoding.')
        ErrorDialog.__init__(self, parent, title, message)


class FileSaveDelegate(Delegate):

    """Saving documents."""

    def _get_main_file_properties(self, page):
        """
        Get properties of the main file.

        Return (path, format, encoding, newlines) or (None, None, None None).
        """
        try:
            path     = page.project.main_file.path
            format   = page.project.main_file.format
            encoding = page.project.main_file.encoding
            newlines = page.project.main_file.newlines
            return path, format, encoding, newlines
        except AttributeError:
            return None, None, None, None

    def _get_translation_file_properties(self, page):
        """
        Get properties of the translation file.

        Properties are inherited from the main file if the translation file
        does not exist.
        Return (path, format, encoding, newlines) or (None, None, None None).
        """
        if page.project.tran_file is not None:
            path     = page.project.tran_file.path
            format   = page.project.tran_file.format
            encoding = page.project.tran_file.encoding
            newlines = page.project.tran_file.newlines
            return path, format, encoding, newlines

        elif page.project.main_file is not None:
            path     = None
            format   = page.project.main_file.format
            encoding = page.project.main_file.encoding
            newlines = page.project.main_file.newlines
            return path, format, encoding, newlines

        else:
            return None, None, None, None

    def on_edit_headers_activated(self, *args):
        """Edit subtitle file headers."""

        page = self.get_current_page()
        dialog = HeaderDialog(self.window, page)
        response = dialog.run()
        main_header = dialog.get_main_header()
        tran_header = dialog.get_translation_header()
        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return

        main_file = page.project.main_file
        tran_file = page.project.tran_file

        if main_file is not None and main_file.has_header:
            main_file.header = main_header
        if tran_file is not None and tran_file.has_header:
            tran_file.header = tran_header

    def on_save_a_copy_of_main_document_activated(self, *args):
        """
        Save a copy of the main document.

        Return success (True or False).
        """
        page = self.get_current_page()
        return self.save_a_copy_of_main_document(page)

    def on_save_a_copy_of_translation_document_activated(self, *args):
        """
        Save a copy of the translation document.

        Return success (True or False).
        """
        page = self.get_current_page()
        return self.save_a_copy_of_translation_document(page)

    def on_save_all_documents_activated(self, *args):
        """Save all documents of all projects."""

        for page in self.pages:
            self.save_main_document(page)
            if page.project.tran_active:
                self.save_translation_document(page)
            page.update_tab_labels()

        self.set_sensitivities()
        self.set_status_message(_('Saved all open documents'))

    def on_save_main_document_activated(self, *args):
        """
        Save the main document.

        Return success (True or False).
        """
        page = self.get_current_page()
        success = self.save_main_document(page)
        if not success:
            return False

        self.set_sensitivities()
        return True

    def on_save_main_document_as_activated(self, *args):
        """
        Save the main document to a selected file.

        Return success (True or False).
        """
        page = self.get_current_page()
        success = self.save_main_document_as(page)
        if not success:
            return False

        self.set_sensitivities()
        return True

    def on_save_translation_document_activated(self, *args):
        """
        Save the translation document.

        Return success (True or False).
        """
        page = self.get_current_page()
        success = self.save_translation_document(page)
        if not success:
            return False

        self.set_sensitivities()
        return True

    def on_save_translation_document_as_activated(self, *args):
        """
        Save the translation document to a selected file.

        Return success (True or False).
        """
        page = self.get_current_page()
        success = self.save_translation_document_as(page)
        if not success:
            return False

        self.set_sensitivities()
        return True

    def save_a_copy_of_main_document(self, page):
        """
        Save a copy of the main document to a selected file.

        Return success (True or False).
        """
        gtklib.set_cursor_busy(self.window)
        properties = self._get_main_file_properties(page)
        path, format, encoding, newlines = properties

        # Translators: File basename for "Save As", "<basename> (copy)".
        path = _('%s (copy)') % page.get_main_corename()
        properties = path, format, encoding, newlines

        try:
            properties = self._select_file(_('Save A Copy'), properties)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return False

        args = page, Document.MAIN, self.window, False, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        self.add_to_recent_files(path)
        message = _('Saved a copy main document to "%s"') % path
        self.set_status_message(message)
        gtklib.set_cursor_normal(self.window)
        return True

    def save_a_copy_of_translation_document(self, page):
        """
        Save a copy of the translation document to a selected file.

        Return success (True or False).
        """
        gtklib.set_cursor_busy(self.window)
        properties = self._get_translation_file_properties(page)
        path, format, encoding, newlines = properties

        # Translators: File basename for "Save As", "<basename> (copy)".
        path = _('%s (copy)') % page.get_translation_corename()
        properties = path, format, encoding, newlines

        title = _('Save A Copy Of Translation')
        try:
            properties = self._select_file(title, properties)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return False

        args = page, Document.TRAN, self.window, False, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        self.add_to_recent_files(path)
        message = _('Saved a copy translation document to "%s"') % path
        self.set_status_message(message)
        gtklib.set_cursor_normal(self.window)
        return True

    def _save_file(self, page, document, parent, keep_changes, properties):
        """
        Check if file is writeable and write it if possible.

        properties: path, format, encoding, newlines
        Return success (True or False).
        """
        path, format, encoding, newlines = properties
        basename = os.path.basename(path)

        try:
            if document == Document.MAIN:
                page.project.save_main_file(keep_changes, properties)
            elif document == Document.TRAN:
                page.project.save_translation_file(keep_changes, properties)

        except IOError, (no, message):
            dialog = SaveFileErrorDialog(parent, basename, message)
            dialog.run()
            dialog.destroy()
            return False

        except UnicodeError:
            codec = encodinglib.get_display_name(encoding)
            dialog = UnicodeEncodeErrorDialog(parent, basename, codec)
            dialog.run()
            dialog.destroy()
            return False

        return True

    def save_main_document(self, page):
        """
        Save the main document.

        Return success (True or False).
        """
        properties = self._get_main_file_properties(page)
        if None in properties:
            return self.save_main_document_as(page)

        args = page, Document.MAIN, self.window, True, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        message = _('Saved main document')
        self.set_status_message(message)
        return True

    def save_main_document_as(self, page):
        """
        Save the main document to a selected file.

        Return success (True or False).
        """
        gtklib.set_cursor_busy(self.window)
        properties = self._get_main_file_properties(page)
        path, format, encoding, newlines = properties
        original_format = format
        if path is None:
            path = page.untitle
            properties = path, format, encoding, newlines

        try:
            properties = self._select_file(_('Save As'), properties)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return False

        args = page, Document.MAIN, self.window, True, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        path, format, encoding, newlines = properties

        # Reload data if saved in a different format, because tags in text
        # might have changed and times/frames are calculated differently
        # resulting from changing mode.
        if original_format is not None:
            if format != original_format:
                page.reload_all()

        # Try to find a video with the new filename.
        if page.project.video_path is None:
            page.project.guess_video_file_path()

        self.add_to_recent_files(path)
        message = _('Saved main document as "%s"') % path
        self.set_status_message(message)
        gtklib.set_cursor_normal(self.window)
        return True

    def save_translation_document(self, page):
        """
        Save the translation document.

        Return success (True or False).
        """
        properties = self._get_translation_file_properties(page)
        if None in properties:
            return self.save_translation_document_as(page)

        args = page, Document.TRAN, self.window, True, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        message = _('Saved translation document')
        self.set_status_message(message)
        return True

    def save_translation_document_as(self, page):
        """
        Save the translation document to a selected file.

        Return success (True or False).
        """
        gtklib.set_cursor_busy(self.window)
        properties = self._get_translation_file_properties(page)
        path, format, encoding, newlines = properties
        original_format = format
        if path is None:
            path = page.get_translation_corename()
            properties = path, format, encoding, newlines

        try:
            title = _('Save Translation As')
            properties = self._select_file(title, properties)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return False

        args = page, Document.TRAN, self.window, True, properties
        success = self._save_file(*args)
        if not success:
            gtklib.set_cursor_normal(self.window)
            return False

        path, format, encoding, newlines = properties

        # Reload text column data if saved in a different format, because tags
        # might have changed.
        if original_format is not None:
            if format != original_format:
                page.reload_columns([TTXT])

        self.add_to_recent_files(path)
        message = _('Saved translation document as "%s"') % path
        self.set_status_message(message)
        gtklib.set_cursor_normal(self.window)
        return True

    def _select_file(self, title, properties):
        """
        Select a file with a filechooser.

        properties: path, format, encoding, newlines
        Raise Cancelled if cancelled.
        Return path, format, encoding, newlines.
        """
        path, format, encoding, newlines = properties
        chooser = SaveFileDialog(title, self.window)
        chooser.set_filename_or_current_name(path)
        chooser.set_format(format)
        chooser.set_encoding(encoding)
        chooser.set_newlines(newlines)

        gtklib.set_cursor_normal(self.window)
        response = chooser.run()
        gtklib.set_cursor_busy(self.window)
        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(chooser)
            raise Cancelled

        filepath = chooser.get_filename_with_extension()
        format   = chooser.get_format()
        encoding = chooser.get_encoding()
        newlines = chooser.get_newlines()

        gtklib.destroy_gobject(chooser)
        return filepath, format, encoding, newlines


if __name__ == '__main__':

    from gaupol.base.cons       import Format
    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestDialog(Test):

        def test_init(self):

            SaveFileErrorDialog(gtk.Window(), 'test', 'test')
            UnicodeEncodeErrorDialog(gtk.Window(), 'test', 'utf_8')

    class TestFileSaveDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.delegate = FileSaveDelegate(self.application)

        def destroy(self):

            self.application.window.destroy()

        def test_get_properties(self):

            self.application.on_new_project_activated()
            page = self.application.get_current_page()
            properties = self.delegate._get_main_file_properties(page)
            assert properties == (None, None, None, None)
            properties = self.delegate._get_translation_file_properties(page)
            assert properties == (None, None, None, None)

            self.application.open_main_files([self.get_subrip_path()])
            page = self.application.get_current_page()
            properties = self.delegate._get_main_file_properties(page)
            assert properties == (
                page.project.main_file.path,
                page.project.main_file.format,
                page.project.main_file.encoding,
                page.project.main_file.newlines
            )

        def test_on_edit_headers_activated(self):

            self.application.open_main_files([self.get_subrip_path()])
            page = self.application.get_current_page()
            properties = (
                page.project.main_file.path,
                Format.SUBVIEWER2,
                page.project.main_file.encoding,
                page.project.main_file.newlines
            )
            page.project.save_main_file(True, properties)

            self.application.on_edit_headers_activated()

        def test_save_files(self):

            self.application.open_main_files([self.get_subrip_path()])
            page = self.application.get_current_page()
            properties = list(self.delegate._get_main_file_properties(page))
            properties[0] = self.get_subrip_path()
            page.project.save_translation_file(True, properties)

            self.application.on_save_a_copy_of_main_document_activated()
            self.application.on_save_a_copy_of_translation_document_activated()
            self.application.on_save_all_documents_activated()
            self.application.on_save_main_document_activated()
            self.application.on_save_main_document_as_activated()
            self.application.on_save_translation_document_activated()
            self.application.on_save_translation_document_as_activated()

    TestDialog().run()
    TestFileSaveDelegate().run()

