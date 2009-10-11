# Copyright (C) 2005-2007,2009 Osmo Salomaa
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

import aeidon


class TestError(aeidon.TestCase):

    def test_raise__error(self):
        try:
            raise aeidon.Error
        except aeidon.Error:
            pass


class TestAffirmationError(aeidon.TestCase):

    def test_raise__affirmation_error(self):
        try:
            raise aeidon.AffirmationError
        except aeidon.AffirmationError:
            pass

    def test_raise__error(self):
        try:
            raise aeidon.AffirmationError
        except aeidon.Error:
            pass


class TestFormatError(aeidon.TestCase):

    def test_raise__format_error(self):
        try:
            raise aeidon.FormatError
        except aeidon.FormatError:
            pass

    def test_raise__error(self):
        try:
            raise aeidon.FormatError
        except aeidon.Error:
            pass


class TestParseError(aeidon.TestCase):

    def test_raise__parse_error(self):
        try:
            raise aeidon.ParseError
        except aeidon.ParseError:
            pass

    def test_raise__error(self):
        try:
            raise aeidon.ParseError
        except aeidon.Error:
            pass


class TestProcessError(aeidon.TestCase):

    def test_raise__process_error(self):
        try:
            raise aeidon.ProcessError
        except aeidon.ProcessError:
            pass

    def test_raise__error(self):
        try:
            raise aeidon.ProcessError
        except aeidon.Error:
            pass
