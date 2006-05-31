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


"""Formatting text."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _
import re

from gaupol.base.cons import SHOW, HIDE, DURN
from gaupol.base.delegates    import Delegate
from gaupol.base.tags.classes import *
from gaupol.base.text.parser  import Parser
from gaupol.base.cons         import Action, Document, Format


class FormatDelegate(Delegate):

    """Formatting text."""

    def change_case(self, rows, document, method, register=Action.DO):
        """
        Change case.

        method: "title", "capitalize", "upper" or "lower"
        """
        re_tag = self.get_regular_expression_for_tag(document)
        parser = Parser(re_tag)
        texts  = (self.main_texts, self.tran_texts)[document]

        new_texts = []
        for row in rows:
            parser.set_text(texts[row])
            parser.text = eval('parser.text.%s()' % method)
            new_texts.append(parser.get_text())

        self.replace_texts(rows, document, new_texts, register)
        self.modify_action_description(register, _('Changing case'))

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
        Get regular expression for a text tag for document.

        Return re object or None.
        """
        format_name = self._get_format_class_name(document)
        if format_name is None:
            return None

        regex, flags = eval(format_name).tag
        return re.compile(regex, flags or 0)

    def toggle_dialog_lines(self, rows, document, register=Action.DO):
        """Toggle dialog lines."""

        re_tag       = self.get_regular_expression_for_tag(document)
        re_dialog    = re.compile(r'^-\s*'  , re.MULTILINE)
        re_no_dialog = re.compile(r'^([^-])', re.MULTILINE)

        texts = (self.main_texts, self.tran_texts)[document]
        new_texts = []

        # Get action to be done.
        dialogize = False
        for row in rows:
            lines = texts[row].split('\n')
            for line in lines:
                # Strip all tags from line. If leftover doesn't start with
                # "-", dialog lines should be added.
                tagless_line = line
                if re_tag is not None:
                    tagless_line = re_tag.sub('', line)
                if not tagless_line.startswith('-'):
                    dialogize = True
                    break

        parser = Parser(re_tag)

        # Add or remove dialog lines.
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

        self.replace_texts(rows, document, new_texts, register)
        description = _('Toggling dialog lines')
        self.modify_action_description(register, description)

    def toggle_italicization(self, rows, document, register=Action.DO):
        """Toggle italicization."""

        format_name   = self._get_format_class_name(document)
        re_tag        = self.get_regular_expression_for_tag(document)
        regex, flags  = eval(format_name).italic_tag
        re_italic_tag = re.compile(regex, flags or 0)

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

        # Italicize or unitalicize.
        for row in rows:
            text = texts[row][:]
            text = re_italic_tag.sub('', text)
            if italicize:
                text = eval(format_name).italicize(text)
            new_texts.append(text)

        self.replace_texts(rows, document, new_texts, register)
        description = _('Toggling italicization')
        self.modify_action_description(register, description)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestFormatDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.project = self.get_project()

        def test_change_case(self):

            self.project.main_texts[1] = 'test'
            self.project.change_case([1], Document.MAIN, 'upper')
            assert self.project.main_texts[1] == 'TEST'

            self.project.undo()
            assert self.project.main_texts[1] == 'test'

        def test_get_format_class_name(self):

            delegate = FormatDelegate(self.project)
            name = delegate._get_format_class_name(Document.MAIN)
            assert name in Format.class_names or name is None

        def test_get_regular_expression_for_tag(self):

            regex = self.project.get_regular_expression_for_tag(Document.MAIN)
            assert hasattr(regex, 'match') or regex is None

        def test_toggle_dialog_lines(self):

            self.project.main_texts[1] = 'test\ntest'
            self.project.toggle_dialog_lines([1], Document.MAIN)
            assert self.project.main_texts[1] == '- test\n- test'
            self.project.toggle_dialog_lines([1], Document.MAIN)
            assert self.project.main_texts[1] == 'test\ntest'

            self.project.undo(2)
            assert self.project.main_texts[1] == 'test\ntest'

        def test_toggle_italicization(self):

            self.project.main_texts[1] = 'test'
            self.project.toggle_italicization([1], Document.MAIN)
            assert self.project.main_texts[1] == '<i>test</i>'
            self.project.toggle_italicization([1], Document.MAIN)
            assert self.project.main_texts[1] == 'test'

            self.project.undo(2)
            assert self.project.main_texts[1] == 'test'

    TestFormatDelegate().run()
