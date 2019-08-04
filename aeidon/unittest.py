# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Base class for unit test cases."""

import aeidon
import os

__all__ = ("TestCase",)


class TestCase:

    """Base class for unit test cases."""

    def assert_raises(self, exception, function, *args, **kwargs):
        """Assert that calling `function` raises `exception`."""
        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError(
            "{!r} failed to raise {!r}"
            .format(function, exception))

    def get_sample_text(self, format, name=None):
        """
        Return sample text for subtitle file `format`.

        `name` can be specified if different from ``format.name.lower()``.
        This is useful for variants of a format, e.g. "subrip-extended".
        """
        name = name or format.name.lower()
        basename = "".join((name, format.extension))
        path = os.path.join(aeidon.DATA_DIR, "samples", basename)
        with open(path, "r", encoding="ascii") as f:
            return f.read().strip()

    def get_spell_check_language(self, language):
        """Return spell-check language to use in unit tests."""
        # Allow any close-enough variant as different systems will have
        # different spell-check engines and dictionaries installed.
        for candidate in aeidon.SpellChecker.list_languages():
            if candidate.startswith(language):
                return candidate
        raise Exception("Spell-check dictionary {}* not found".format(language))

    def new_microdvd_file(self):
        """Return path to a new temporary MicroDVD file."""
        return self.new_temp_file(aeidon.formats.MICRODVD)

    def new_project(self):
        """Return a new project with both main and translation files."""
        project = aeidon.Project()
        project.open_main(self.new_subrip_file(), "ascii")
        project.open_translation(self.new_microdvd_file(), "ascii")
        return project

    def new_subrip_file(self):
        """Return path to a new temporary SubRip file."""
        return self.new_temp_file(aeidon.formats.SUBRIP)

    def new_temp_file(self, format, name=None):
        """Return path to a new temporary subtitle file."""
        text = self.get_sample_text(format, name)
        path = aeidon.temp.create(format.extension)
        with open(path, "w", encoding="ascii") as f:
            f.write(text)
        return path

    def setUp(self):
        """Compatibility alias for :meth:`setup_method`."""
        self.setup_method(None)

    def setup_method(self, method):
        """Set state for executing tests in `method`."""
        pass

    def tearDown(self):
        """Compatibility alias for :meth:`teardown_method`."""
        self.teardown_method(None)

    def teardown_method(self, method):
        """Remove state set for executing tests in `method`."""
        pass

    def test___init__(self):
        """Make sure that :meth:`setup_method` is always run."""
        pass
