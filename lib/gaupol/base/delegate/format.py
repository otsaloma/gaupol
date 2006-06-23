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


"""Formatting text."""


from gettext import gettext as _
import re

from gaupol.base              import cons
from gaupol.base.icons        import *
from gaupol.base.delegate     import Delegate
from gaupol.base.tags.classes import *
from gaupol.base.text.parser  import Parser


class FormatDelegate(Delegate):

    """Formatting text."""

    def _get_format_class_name(self, doc):
        """
        Get class name of document's file format.

        Translation document will inherit main document's format if translation
        file does not exist.

        Return name or None.
        """
        if doc == MAIN:
            try:
                return cons.Format.class_names[self.main_file.format]
            except AttributeError:
                return None
        elif doc == TRAN:
            try:
                return cons.Format.class_names[self.tran_file.format]
            except AttributeError:
                return self._get_format_class_name(MAIN)

    def change_case(self, rows, doc, method, register=cons.Action.DO):
        """
        Change case of text.

        method: "title", "capitalize", "upper" or "lower"
        """
        try:
            re_tag = self.get_tag_regex(doc)
            parser = Parser(re_tag)
        except ValueError:
            parser = Parser(None)

        new_texts = []
        texts = (self.main_texts, self.tran_texts)[doc]
        for row in rows:
            parser.set_text(texts[row])
            parser.set_text(eval('parser.text.%s()' % method))
            new_texts.append(parser.get_text())

        self.replace_texts(rows, doc, new_texts, register)
        self.set_action_description(register, _('Changing case'))

    def get_tag_regex(self, document):
        """
        Get regular expression for tag in document.

        Raise ValueError if no tag (no format).
        """
        name = self._get_format_class_name(document)
        if name is None:
            raise ValueError

        return re.compile(*eval(name).tag)

    def toggle_dialog_lines(self, rows, doc, register=cons.Action.DO):
        """Toggle dialog lines on text."""

        try:
            re_tag = self.get_tag_regex(doc)
            parser = Parser(re_tag)
        except ValueError:
            parser = Parser(None)
        texts = (self.main_texts, self.tran_texts)[doc]

        # Get action to be done.
        dialogize = False
        for row in rows:
            lines = texts[row].split('\n')
            for line in lines:
                # Strip all tags from line. If leftover doesn't start with "-",
                # dialog lines should be added.
                tagless_line = line
                if re_tag is not None:
                    tagless_line = re_tag.sub('', line)
                if not tagless_line.startswith('-'):
                    dialogize = True
                    break

        new_texts = []
        for row in rows:
            parser.set_text(texts[row])
            parser.set_regex(r'^-\s*', re.MULTILINE)
            parser.replacement = ''
            parser.replace_all()
            if dialogize:
                parser.set_regex(r'^([^-])', re.MULTILINE)
                parser.replacement = r'- \1'
                parser.replace_all()
            new_texts.append(parser.get_text())

        self.replace_texts(rows, doc, new_texts, register)
        self.set_action_description(register, _('Toggling dialog lines'))

    def toggle_italicization(self, rows, doc, register=cons.Action.DO):
        """Toggle italicization of text."""

        try:
            re_tag = self.get_tag_regex(doc)
        except ValueError:
            re_tag = None
        format_name = self._get_format_class_name(doc)
        re_italic_tag = re.compile(*eval(format_name).italic_tag)
        texts = (self.main_texts, self.tran_texts)[doc]

        # Get action to be done.
        italicize = False
        for row in rows:
            # Remove tags from the start of the text, ending after all tags are
            # removed or when an italic tag is found.
            tagless_text = texts[row][:]
            if re_tag is not None:
                while re_tag.match(tagless_text):
                    if re_italic_tag.match(tagless_text):
                        break
                    tagless_text = re_tag.sub('', tagless_text, 1)
            # If there is no italic tag at the start of the text, texts should
            # be italicized.
            if re_italic_tag.match(tagless_text) is None:
                italicize = True
                break

        new_texts = []
        for row in rows:
            text = re_italic_tag.sub('', texts[row])
            if italicize:
                text = eval(format_name).italicize(text)
            new_texts.append(text)

        self.replace_texts(rows, doc, new_texts, register)
        self.set_action_description(register, _('Toggling italicization'))
