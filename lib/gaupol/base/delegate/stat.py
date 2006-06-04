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


"""Statistics and information."""


from gaupol.base.delegate import Delegate


class StatisticsDelegate(Delegate):

    """Statistics and information."""

    def get_line_lengths(self, row, doc):
        """Get list of line lengths."""

        text = [self.main_texts, self.tran_texts][doc][row]
        try:
            re_tag = self.get_tag_regex(doc)
            text = re_tag.sub('', text)
        except ValueError:
            pass

        return list(len(x) for x in text.split('\n'))
