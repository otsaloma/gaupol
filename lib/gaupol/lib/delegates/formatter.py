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


"""Data Formatter to alter text style."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.constants import SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.lib.delegates.delegate import Delegate
from gaupol.lib.formats import tags as tags_module


class Formatter(Delegate):
    
    """Data Formatter to alter text style."""

    def change_case(self, rows, col, method):
        """
        Change case of texts specified by rows and col.
        
        method: "capitalize", "upper", "lower", "title" or "swapcase"
        Return: new texts
        """
        texts = [self.texts[i][col] for i in rows]

        format = self.get_format(col)
        re_tag = tags_module.get_tag_re(format)

        for i in range(len(texts)):

            text = texts[i]

            # List of found tags and their positions.
            tags = []

            for match in re_tag.finditer(text):
                start = match.start()
                end   = match.end()
                tags.append([text[start:end], start])

            text = re_tag.sub('', text)
            text = eval('text.%s()' % method)

            for entry in tags:
                tag, start = entry
                text = text[:start] + tag + text[start:]

            texts[i] = text
        
        for i in range(len(rows)):
            self.texts[rows[i]][col] = texts[i]
            
        return texts

    def clear(self, rows, col):
        """Clear texts specified by rows and col."""
        
        for row in rows:
            self.texts[row][col] = u''

    def toggle_dialog_lines(self, rows, col):
        """
        Toggle dialog lines on texts specified by rows and col.

        Return: new texts
        """
        texts = [self.texts[i][col] for i in rows]

        format = self.get_format(col)
        re_tag = tags_module.get_tag_re(format)
        re_dialog = re.compile('^-\s*')
        TAG, POS = 0, 1
        
        turn_into_dialog = False
        
        # Get action to be done.
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
                
                for match in re_tag.finditer(line):
                    start = match.start()
                    end   = match.end()
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

        return texts

    def toggle_italicization(self, rows, col):
        """
        Toggle italicization of texts specified by rows and col.

        Return: new texts
        """
        texts = [self.texts[i][col] for i in rows]
        format = self.get_format(col)
        
        texts = tags_module.toggle_italicization(format, texts)

        for i in range(len(rows)):
            self.texts[rows[i]][col] = texts[i]
            
        return texts

    def get_format(self, col):
        """Get file format used in given text column."""
        
        if col == ORIG:
            try:
                return self.main_file.FORMAT
            except AttributeError:
                return None

        elif col == TRAN:
            try:
                return self.tran_file.FORMAT
            except AttributeError:
                return self.get_format(ORIG)
