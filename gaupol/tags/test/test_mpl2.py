# Copyright (C) 2005-2007 Osmo Salomaa
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


from .test_microdvd import TestMicroDVD
from .. import mpl2


class TestMPL2(TestMicroDVD):

    def setup_method(self, method):

        self.taglib = mpl2.MPL2()

    def test_decode(self):

        # Italic
        text = \
            "/All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<i>All things weird are normal</i>\n" + \
            "in this whore of cities."

        # Italic
        text = \
            "/All things weird are normal\n" + \
            "/in this whore of cities."
        assert self.taglib.decode(text) == \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"

        # Bold
        text = \
            "All things \\weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things <b>weird are normal</b>\n" + \
            "in this whore of cities."

        # Bold
        text = \
            "All things \\weird are normal\n" + \
            "in this \\whore of cities."
        assert self.taglib.decode(text) == \
            "All things <b>weird are normal</b>\n" + \
            "in this <b>whore of cities.</b>"

        # Underline
        text = \
            "All things weird are normal\n" + \
            "_in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "<u>in this whore of cities.</u>"

        # Underline
        text = \
            "_All things weird are normal\n" + \
            "in this _whore of cities."
        assert self.taglib.decode(text) == \
            "<u>All things weird are normal</u>\n" + \
            "in this <u>whore of cities.</u>"

        TestMicroDVD.test_decode(self)

    def test_encode(self):

        # Italic
        text = \
            "<i>All things weird are normal</i>\n" + \
            "in this whore of cities."
        assert self.taglib.encode(text) == \
            "/All things weird are normal\n" + \
            "in this whore of cities."

        # Italic
        text = \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
        assert self.taglib.encode(text) == \
            "/All things weird are normal\n" + \
            "/in this whore of cities."

        # Bold
        text = \
            "<b>All things weird</b> are normal\n" + \
            "in this whore of cities."
        assert self.taglib.encode(text) == \
            "\\All things weird are normal\n" + \
            "in this whore of cities."

        # Bold
        text = \
            "<b>All things weird are normal\n" + \
            "in this whore</b> of cities."
        assert self.taglib.encode(text) == \
            "\\All things weird are normal\n" + \
            "\\in this whore of cities."

        # Underline
        text = \
            "All things <u>weird are normal</u>\n" + \
            "in this whore of cities."
        assert self.taglib.encode(text) == \
            "All things _weird are normal\n" + \
            "in this whore of cities."

        # Underline
        text = \
            "All things <u>weird are normal\n" + \
            "in this whore of cities.</u>"
        assert self.taglib.encode(text) == \
            "All things _weird are normal\n" + \
            "_in this whore of cities."

        TestMicroDVD.test_encode_non_style(self)

    def test_italicize(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.italicize(text) == \
            "/All things weird are normal\n" + \
            "/in this whore of cities."
