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


"""Formatting text."""


try:
    from psyco.classes import *
except ImportError:
    pass

import re

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.base.tags.classes import *
from gaupol.base.text.parser  import TextParser
from gaupol.base.util         import relib
from gaupol.constants         import Action, Document, Format


class FormatDelegate(Delegate):

    """Formatting text."""

    def _get_format_class_name(self, document):
        """
        Get the class name of document's file format.

        Translation column will inherit original column's format if
        translation file does not exist.
        Return name or None.
        """
        if document == Document.MAIN:
            try:
                return Format.class_names[self.main_file.format]
            except AttributeError:
                return None

        elif document == Document.TRAN:
            try:
                return Format.class_names[self.tran_file.format]
            except AttributeError:
                return self._get_format_class_name(Document.MAIN)

    def get_regular_expression_for_tag(self, document):
        """
        Get the regular expression for a text tag for document.

        Return re pattern or None.
        """
        format_name = self._get_format_class_name(document)

        if format_name is None:
            return None

        regex, flags = eval(format_name).tag
        return relib.compile(regex, flags)

    def toggle_dialog_lines(self, rows, document, register=Action.DO):
        """Toggle dialog lines."""

        re_tag       = self.get_regular_expression_for_tag(document)
        re_dialog    = re.compile(r'^-\s*', re.MULTILINE)
        re_no_dialog = re.compile(r'^([^-])', re.MULTILINE)
        parser = TextParser(re_tag)

        texts = (self.main_texts, self.tran_texts)[document]
        new_texts = []

        # Get action to be done.
        dialogize = False
        for row in rows:
            lines = texts[row].split('\n')
            for line in lines:
                # Strip all tags from line. If leftover doesn't start with
                # "-", dialog lines should be added.
                tagless_line = re_tag.sub('', line)
                if not tagless_line.startswith('-'):
                    dialogize = True
                    break

        # Add or remove dialog lines.
        for row in rows:
            parser.set_text(texts[row])
            parser.substitute(re_dialog, '')
            if dialogize:
                parser.substitute(re_no_dialog, r'- \1')
            new_texts.append(parser.get_text())

        self.replace_texts(rows, document, new_texts, register)
        description = _('Toggling dialog lines')
        self.modify_action_description(register, description)

    def toggle_italicization(self, rows, document, register=Action.DO):
        """Toggle italicization."""

        format_name = self._get_format_class_name(document)
        re_tag = self.get_regular_expression_for_tag(document)
        regex, flags = eval(format_name).italic_tag
        re_italic_tag = relib.compile(regex, flags)

        texts = (self.main_texts, self.tran_texts)[document]
        new_texts = []

        # Get action to be done.
        italicize = False
        for row in rows:

            # Remove tags from the start of the text, ending after all
            # tags are removed or when an italic tag is found.
            tagless_text = texts[row][:]
            while re_tag.match(tagless_text):
                if re_italic_tag.match(tagless_text):
                    break
                tagless_text = re_tag.sub('', tagless_text, 1)

            # If there is no italic tag at the start of the text,
            # texts should be italicized.
            if re_italic_tag.match(tagless_text) is None:
                italicize = True
                break

        # Remove existing italic tags and italicize or unitalicize.
        for row in rows:
            text = texts[row][:]
            text = re_italic_tag.sub('', text)
            if italicize:
                text = eval(format_name).italicize(text)
            new_texts.append(text)

        self.replace_texts(rows, document, new_texts, register)
        description = _('Toggling italicization')
        self.modify_action_description(register, description)
