# Copyright (C) 2006 Osmo Salomaa
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


"""Text corrections."""


from gettext import gettext as _
import copy
import re

from gaupol.base             import cons
from gaupol.base.delegate    import Delegate, revertablemethod
from gaupol.base.text.finder import Finder
from gaupol.base.util        import listlib


class TextDelegate(Delegate):

    """Text corrections."""

    @revertablemethod
    def capitalize(self, rows, docs, pattern, flags=0, register=-1):
        """
        Capitalize texts following match of pattern.

        rows: None to process all, otherwise a single range
        re.UNICODE is automatically added to flags.
        Return changed rows.
        """
        finder = Finder()
        finder.set_regex(pattern, flags)
        re_alpha = re.compile('\w', re.UNICODE)

        new_rows  = [[], []]
        new_texts = [[], []]
        rows = rows or range(len(self.times))
        for doc in docs:
            texts = (self.main_texts, self.tran_texts)[doc]
            cap_next = False
            for row in rows:
                text = texts[row]
                if cap_next or row == 0:
                    match = re_alpha.search(text)
                    if match is not None:
                        start = match.start()
                        text = text[:start] + text[start:].capitalize()
                    cap_next = False
                finder.set_text(text)
                while True:
                    try:
                        end = finder.next()[1]
                    except StopIteration:
                        break
                    match = re_alpha.search(text[end:])
                    if match is not None:
                        end = end + match.start()
                        text = text[:end] + text[end:].capitalize()
                        continue
                    cap_next = True
                    break
                if text != texts[row]:
                    new_rows[doc].append(row)
                    new_texts[doc].append(text)

        self.replace_both_texts(new_rows, new_texts, register=register)
        self.set_action_description(register, _('Capitalizing texts'))
        return listlib.sorted_unique(new_rows[0] + new_rows[1])
