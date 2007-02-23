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


"""Sample subtitle files as strings.

Module variables:

    MICRODVD_TEXT: Sample MicroDVD text
    SUBRIP_TEXT:   Sample SubRip text
"""


MICRODVD_TEXT = \
"""{1419}{1515}I always wanted to leave my country|and go somewhere else.
{1548}{1607}I always wanted to come to France.
{1613}{1665}So, one day when I was 17, I left.
{1695}{1743}{Y:i}There I was in Paris.
{1815}{1915}{Y:i}Since I was a bit naive,
{1932}{2030}{Y:i}everyone seemed beautiful|and fabulous.
{2041}{2142}{Y:i}I couldn't tell cruelty from kindness.
{2147}{2250}{Y:i}For me, people were|the way they were.
{2259}{2345}{Y:i}You just worked with them|or talked with them.
{2368}{2448}{Y:i}Obviously, it was a big shock.
"""

SUBRIP_TEXT = \
"""1
00:00:59,188 --> 00:01:03,198
I always wanted to leave my country
and go somewhere else.

2
00:01:04,583 --> 00:01:07,012
I always wanted to come to France.

3
00:01:07,281 --> 00:01:09,439
So, one day when I was 17, I left.

4
00:01:10,716 --> 00:01:12,715
<i>There I was in Paris.</i>

5
00:01:15,708 --> 00:01:19,856
<i>Since I was a bit naive,</i>

6
00:01:20,568 --> 00:01:24,682
<i>everyone seemed beautiful</i>
<i>and fabulous.</i>

7
00:01:25,124 --> 00:01:29,341
<i>I couldn't tell cruelty from kindness.</i>

8
00:01:29,548 --> 00:01:33,833
<i>For me, people were</i>
<i>the way they were.</i>

9
00:01:34,240 --> 00:01:37,816
<i>You just worked with them</i>
<i>or talked with them.</i>

10
00:01:38,764 --> 00:01:42,111
<i>Obviously, it was a big shock.</i>
"""
