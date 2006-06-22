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


from gaupol.base.util import enclib
from gaupol.test      import Test


class TestModule(Test):

    def test_translate(self):

        entry = enclib._translate('ISO-8859-1')
        assert entry[0] == 'latin_1'

    def test_detect(self):

        name = enclib.detect(self.get_subrip_path())
        assert enclib.is_valid(name) is True

    def test_get_display_name(self):

        name = enclib.get_display_name('johab')
        assert name == 'Johab'

        try:
            enclib.get_display_name('xxxxx')
            raise AssertionError
        except ValueError:
            pass

    def test_get_locale_encoding(self):

        entry = enclib.get_locale_encoding()
        assert len(entry) == 3
        assert enclib.is_valid(entry[0]) is True

    def test_get_locale_long_name(self):

        name = enclib.get_locale_long_name()
        assert isinstance(name, basestring)

    def test_get_long_name(self):

        name = enclib.get_long_name('johab')
        assert isinstance(name, basestring)

        try:
            enclib.get_long_name('xxxxx')
            raise AssertionError
        except ValueError:
            pass

    def test_get_python_name(self):

        name = enclib.get_python_name('Johab')
        assert name == 'johab'

        try:
            enclib.get_python_name('xxxxx')
            raise AssertionError
        except ValueError:
            pass

    def test_get_valid_encodings(self):

        entries = enclib.get_valid_encodings()
        assert len(entries) > 10
        for entry in entries:
            assert len(entry) == 3
            assert enclib.is_valid(entry[0]) is True

    def test_is_valid(self):

        assert enclib.is_valid('johab') is True
        assert enclib.is_valid('xxxxx') is False
