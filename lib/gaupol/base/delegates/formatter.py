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


"""Text style formatting."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FORMAT
from gaupol.base.colcons import *
from gaupol.base.delegates.delegate import Delegate
from gaupol.base.tags.classes import *
from gaupol.base.text.parser import TextParser


class Formatter(Delegate):
    
    """Text style formatting."""

    def change_case(self, rows, col, method):
        """
        Change case of texts specified by rows and col.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        texts = self.texts
        re_tag = self.get_regex_for_tag(col)
        parser = TextParser(re_tag)

        for row in rows:
            parser.set_text(texts[row][col])
            parser.text = eval('parser.text.%s()' % method)
            texts[row][col] = parser.get_text()

    def _get_format_name(self, col):
        """
        Get name of file format used in given text column.
        
        Translation column will inherit original column's format if
        translation file does not exist.

        Return name or None.
        """
        if col == TEXT:
            try:
                return FORMAT.NAMES[self.main_file.FORMAT]
            except AttributeError:
                return None

        elif col == TRAN:
            try:
                return FORMAT.NAMES[self.tran_file.FORMAT]
            except AttributeError:
                return self._get_format_name(TEXT)

    def get_regex_for_tag(self, col):
        """
        Get regular expression for tag in given text column.
        
        Return re object or None.
        """
        format_name = self._get_format_name(col)

        if format_name is None:
            return None

        regex, flags = eval(format_name).TAG
        
        try:
            return re.compile(regex, flags)
        except TypeError:
            return re.compile(regex)

    def toggle_dialog_lines(self, rows, col):
        """Toggle dialog lines on texts specified by rows and col."""
        
        re_tag = self.get_regex_for_tag(col)
        re_dialog = re.compile('^-\s*', re.MULTILINE)
        re_line_start = re.compile('^', re.MULTILINE)
        parser = TextParser(re_tag)
        
        # Get action to be done.
        dialogize = False
        for row in rows:
        
            lines = self.texts[row][col].split('\n')
            for line in lines:
            
                # Strip all tags from line. If leftover doesn't start with
                # "-", dialog lines should be added.
                tagless_line = re_tag.sub('', line)
                if not tagless_line.startswith('-'):
                    dialogize = True
                    break

        # Add or remove dialog lines.
        for row in rows:

            parser.set_text(self.texts[row][col])

            # Remove existing dialog lines.
            parser.substitute(re_dialog, '')

            # Add dialog lines.
            if dialogize:
                parser.substitute(re_line_start, '- ')

            self.texts[row][col] = parser.get_text()
            
    def toggle_italicization(self, rows, col):
        """Toggle italicization of texts specified by rows and col."""
        
        format_name = self._get_format_name(col)
        re_tag = self.get_regex_for_tag(col)

        # Get regular expression for an italic tag.
        regex, flags = eval(format_name).ITALIC
        try:
            re_italic_tag = re.compile(regex, flags)
        except TypeError:
            re_italic_tag = re.compile(regex)

        # Get action to be done.
        italicize = False
        for row in rows:
            
            # Remove tags from the start of the text, ending after all
            # tags are removed or when an italic tag is found.
            tagless_text = self.texts[row][col][:]
            while re_tag.match(tagless_text):
                if re_italic_tag.match(tagless_text):
                    break
                else:
                    tagless_text = re_tag.sub('', tagless_text, 1)

            # If there is no italic tag at the start of the text,
            # texts should be italicized.
            if re_italic_tag.match(tagless_text) is None:
                italicize = True
                break

        # Remove existing italic tags and italicize or unitalicize.
        for row in rows:
            text = self.texts[row][col]
            text = re_italic_tag.sub('', text)
            if italicize:
                text = eval(format_name).italicize(text)
            self.texts[row][col] = text
