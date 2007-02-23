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


import urllib

from gaupol.unittest import TestCase
from .. import urls


class TestModule(TestCase):

    def test_attributes(self):

        urllib.urlopen(urls.BUG_REPORT)
        urllib.urlopen(urls.DOWNLOAD)
        urllib.urlopen(urls.HOMEPAGE)
        urllib.urlopen(urls.REGEX_HELP)
        urllib.urlopen(urls.VERSION)
