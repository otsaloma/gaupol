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
from gaupol.lib.constants import *
from gaupol.lib.delegates.delegate import Delegate
from gaupol.lib.tags.all import *


class Formatter(Delegate):
    
    """Text style formatting."""

    def change_case(self, rows, col, method):
        """
        Change case of texts specified by rows and col.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        """
        texts = [self.texts[row][col] for row in rows]
        re_tag = self.get_regex_for_tag(col)

        for i in range(len(texts)):

            text = texts[i]

            # List of found tags and their positions.
            tags = []

            # Find tags.
            for match in re_tag.finditer(text):
                start, end = match.span()
                tags.append([text[start:end], start])

            # Remove tags and change case.
            text = re_tag.sub('', text)
            text = eval('text.%s()' % method)

            # Reconstruct text.
            for entry in tags:
                tag, start = entry
                text = text[:start] + tag + text[start:]

            texts[i] = text
        
        for i in range(len(rows)):
            self.texts[rows[i]][col] = texts[i]

    def _get_format_name(self, col):
        """
        Get name of file format used in given text column.
        
        Translation column will inherit original column's format if
        translation file does not exist.

        Return: format name or None
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
        
        Return: re object or None
        """
        format_name = self._get_format_name(col)

        if format is None:
            return None

        regex, flags = eval(format_name).TAG
        
        try:
            return re.compile(regex, flags)
        except TypeError:
            return re.compile(regex)

    def toggle_dialog_lines(self, rows, col):
        """Toggle dialog lines on texts specified by rows and col."""
        
        texts = [self.texts[row][col] for row in rows]
        re_tag = self.get_regex_for_tag(col)
        re_dialog = re.compile('^-\s*')
        
        # Get action to be done.
        turn_into_dialog = False
        for text in texts:
            lines = text.split('\n')
            for line in lines:
                if not line.startswith('-'):
                    turn_into_dialog = True
                    break

        for i in range(len(texts)):

            lines = texts[i].split('\n')

            for k in range(len(lines)):

                line = lines[k]
            
                # List of found tags and their positions.
                tags = []
                
                # Find tags.
                for match in re_tag.finditer(line):
                    start, end = match.span()
                    tags.append([line[start:end], start])

                line = re_tag.sub('', line)

                # Shift in tag positions caused by dialog line operations.
                shift = 0

                # Remove existing dialog lines.
                match = re_dialog.match(line)
                if match is not None:
                    line = re_dialog.sub('', line)
                    shift -= match.end()

                # Add dialog line.
                if turn_into_dialog:
                    line = '- ' + line
                    shift += 2

                # Sum of the lengths of preceding tags.
                length = 0
                
                # Reconstruct line.
                for entry in tags:
                    tag, start = entry
                    if start > length:
                        start = start + shift
                    line = line[:start] + tag + line[start:]
                    length += len(tag)

                lines[k] = line

            texts[i] = '\n'.join(lines)
            
        for i in range(len(rows)):
            self.texts[rows[i]][col] = texts[i]

    def toggle_italicization(self, rows, col):
        """Toggle italicization of texts specified by rows and col."""
        
        texts = [self.texts[row][col] for row in rows]
        format_name = self._get_format_name(col)

        # Get regular expression for an italic tag.
        regex, flags = eval(format_name).ITALIC
        try:
            re_italic_tag = re.compile(regex, flags)
        except TypeError:
            re_italic_tag = re.compile(regex)

        # Get action to be done.
        turn_into_italics = False
        for text in texts:
            if re_italic_tag.match(text) is None:
                turn_into_italics = True
                break

        # Remove existing italic tags and italicize if that is to be done.
        for i in range(len(texts)):
            texts[i] = re_italic_tag.sub('', texts[i])
            if turn_into_italics:
                texts[i] = eval(format).italicize(texts[i])

        for i in range(len(rows)):
            self.texts[rows[i]][col] = texts[i]
