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


"""Statistics and information."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.base.delegates import Delegate


class StatisticsDelegate(Delegate):

    """Statistics and information."""

    def get_character_count(self, row, document):
        """
        Get character count of text.

        Return list of row lengths, total length.
        """
        text = [self.main_texts, self.tran_texts][document][row]
        re_tag = self.get_regular_expression_for_tag(document)
        if re_tag is not None:
            text = re_tag.sub('', text)

        lengths = []
        total   = 0
        for line in text.split('\n'):
            length = len(line)
            lengths.append(length)
            total += length

        return lengths, total


if __name__ == '__main__':

    from gaupol.constants import Document
    from gaupol.test      import Test

    class TestStatisticsDelegate(Test):

        def test_get_character_count(self):

            project = self.get_project()
            project.main_texts[0] = '<i>test\ntest.</i>'
            lengths, total = project.get_character_count(0, Document.MAIN)
            assert lengths == [4, 5]
            assert total   == 9

    TestStatisticsDelegate().run()
