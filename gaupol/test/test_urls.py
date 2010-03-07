# Copyright (C) 2006,2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import gaupol
import urllib


class TestModule(gaupol.TestCase):

    def test_bug_report_url(self):
        urllib.urlopen(gaupol.BUG_REPORT_URL)

    def test_homepage_url(self):
        urllib.urlopen(gaupol.HOMEPAGE_URL)

    def test_regex_help_url(self):
        urllib.urlopen(gaupol.REGEX_HELP_URL)

    def test_wiki_url(self):
        urllib.urlopen(gaupol.WIKI_URL)
