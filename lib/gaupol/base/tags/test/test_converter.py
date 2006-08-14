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


from gaupol.base                import cons
from gaupol.base.tags.converter import TagConverter
from gaupol.test                import Test


class TestTagConverter(Test):

    def test_ass_to_microdvd(self):

        converter = TagConverter(cons.Format.ASS, cons.Format.MICRODVD)

        orig = \
            "{\\i1\\b1}All{\\r} that {\\i1}because{\\r} I wasn't\n" \
            "in {\\fs12}their{\\r} shoes, {\\c&H0000ff&}but mine."
        new = \
            "{y:i}{y:b}All that {y:i}because I wasn't\n" \
            "in {s:12}their shoes, {c:$0000ff}but mine."
        assert converter.convert(orig) == new

        orig = \
            "{\\i1}All that because I wasn't\n" \
            "in their shoes, but mine."
        new = \
            "{Y:i}All that because I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

    def test_ass_to_subrip(self):

        converter = TagConverter(cons.Format.ASS, cons.Format.SUBRIP)

        orig = \
            "{\\i1\\b1}All{\\r} that {\\i1}because{\\r} I wasn't\n" \
            "in {\\fs12}their{\\r} shoes, {\\c&H0000ff&}but mine."
        new = \
            "<i><b>All</b></i> that <i>because</i> I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

        orig = \
            "{\\i1}All that because I wasn't\n" \
            "in their shoes, but mine."
        new = \
            "<i>All that because I wasn't\n" \
            "in their shoes, but mine.</i>"
        assert converter.convert(orig) == new

    def test_microdvd_to_ass(self):

        converter = TagConverter(cons.Format.MICRODVD, cons.Format.ASS)

        orig = \
            "{y:i}{y:b}All that because I wasn't\n" \
            "in {s:12}their shoes, {c:$0000ff}but mine."
        new = \
            "{\\i1}{\\b1}All that because I wasn't{\\b0}{\\i0}\n" \
            "in {\\fs12}their shoes, {\\c&H0000ff&}but mine."
        assert converter.convert(orig) == new

        orig = \
            "{Y:i}All that because I wasn't\n" \
            "in their shoes, but mine."
        new = \
            "{\\i1}All that because I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

    def test_microdvd_to_subrip(self):

        converter = TagConverter(cons.Format.MICRODVD, cons.Format.SUBRIP)

        orig = \
            "{y:i}{y:b}All that because I wasn't\n" \
            "in {s:12}their shoes, {c:$0000ff}but mine."
        new = \
            "<i><b>All that because I wasn't</b></i>\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

        orig = \
            "{Y:i}All that because I wasn't\n" \
            "in their shoes, but mine."
        new = \
            "<i>All that because I wasn't\n" \
            "in their shoes, but mine.</i>"
        assert converter.convert(orig) == new

    def test_mpl2_to_ass(self):

        converter = TagConverter(cons.Format.MPL2, cons.Format.ASS)

        orig = \
            "/\\All that because I wasn't\n" \
            "in {s:12}their shoes, {c:$0000ff}but mine."
        new = \
            "{\\i1}{\\b1}All that because I wasn't{\\i0}{\\b0}\n" \
            "in {\\fs12}their shoes, {\\c&H0000ff&}but mine."
        assert converter.convert(orig) == new

        orig = \
            "/All that because I wasn't\n" \
            "/in their shoes, but mine."
        new = \
            "{\\i1}All that because I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

    def test_mpl2_to_subrip(self):

        converter = TagConverter(cons.Format.MPL2, cons.Format.SUBRIP)

        orig = \
            "/\\All that because I wasn't\n" \
            "in {s:12}their shoes, {c:$0000ff}but mine."
        new = \
            "<i><b>All that because I wasn't</i></b>\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

        orig = \
            "/All that because I wasn't\n" \
            "/in their shoes, but mine."
        new = \
            "<i>All that because I wasn't\n" \
            "in their shoes, but mine.</i>"
        assert converter.convert(orig) == new

    def test_subrip_to_ass(self):

        converter = TagConverter(cons.Format.SUBRIP, cons.Format.ASS)

        orig = \
            "<i><b>All</b></i> that because I wasn't\n" \
            "<i>in their shoes, but mine.</i>"
        new = \
            "{\\i1}{\\b1}All{\\b0}{\\i0} that because I wasn't\n" \
            "{\\i1}in their shoes, but mine."
        assert converter.convert(orig) == new

        orig = \
            "<i>All that because I wasn't\n" \
            "in their shoes, but mine.</i>"
        new = \
            "{\\i1}All that because I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new

    def test_subrip_to_microdvd(self):

        converter = TagConverter(cons.Format.SUBRIP, cons.Format.MICRODVD)

        orig = \
            "<i><b>All</b></i> that because I wasn't\n" \
            "<i>in their shoes, but mine.</i>"
        new = \
            "{y:i}{y:b}All that because I wasn't\n" \
            "{y:i}in their shoes, but mine."
        assert converter.convert(orig) == new

        orig = \
            "<i>All that because I wasn't\n" \
            "in their shoes, but mine.</i>"
        new = \
            "{Y:i}All that because I wasn't\n" \
            "in their shoes, but mine."
        assert converter.convert(orig) == new
