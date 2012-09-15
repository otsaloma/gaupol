# -*- coding: utf-8 -*-

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
import urllib.request


class TestModule(gaupol.TestCase):

    def open(self, url):
        return urllib.request.urlopen(url, timeout=10)

    def test_bug_report_url(self):
        self.open(gaupol.BUG_REPORT_URL)

    def test_extensions_url(self):
        self.open(gaupol.EXTENSIONS_URL)

    def test_homepage_url(self):
        self.open(gaupol.HOMEPAGE_URL)

    def test_preview_help_url(self):
        self.open(gaupol.PREVIEW_HELP_URL)

    def test_regex_help_url(self):
        self.open(gaupol.REGEX_HELP_URL)

    def test_speech_recognition_help_url(self):
        self.open(gaupol.SPEECH_RECOGNITION_HELP_URL)

    def test_wiki_url(self):
        self.open(gaupol.WIKI_URL)
