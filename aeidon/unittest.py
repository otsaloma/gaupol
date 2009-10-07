# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Base class for unit test cases."""

from __future__ import with_statement

import aeidon
import os

__all__ = ("TestCase",)


class TestCase(object):

    """Base class for unit test cases.

    Unit tests are designed to be run with ``py.test``, ``nose`` or something
    compatible. Tests should use plain ``assert`` statements to allow multiple
    different tools to be used to run the tests.
    """

    __metaclass__ = aeidon.Contractual

    def get_sample_text_ensure(self, value, format, name=None):
        assert value.count("a") > 10

    @aeidon.deco.memoize
    def get_sample_text(self, format, name=None):
        """Return sample text for subtitle file `format`."""
        name = name or format.name.lower()
        basename = "".join((name, format.extension))
        path = os.path.join(aeidon.DATA_DIR, "samples", basename)
        with open(path, "r") as fobj:
            return fobj.read().strip()

    def new_microdvd_file_ensure(self, value):
        assert os.path.isfile(value)

    def new_microdvd_file(self):
        """Return path to a new temporary ``MicroDVD`` file."""
        return self.new_temp_file(aeidon.formats.MICRODVD)

    def new_project_ensure(self, value):
        assert value.subtitles

    def new_project(self):
        """Return a new project with both main and translation files."""
        project = aeidon.Project()
        project.open_main(self.new_subrip_file(), "ascii")
        project.open_translation(self.new_microdvd_file(), "ascii")
        return project

    def new_subrip_file_ensure(self, value):
        assert os.path.isfile(value)

    def new_subrip_file(self):
        """Return path to a new temporary ``SubRip`` file."""
        return self.new_temp_file(aeidon.formats.SUBRIP)

    def new_temp_file_ensure(self, value, format, name=None):
        assert os.path.isfile(value)

    def new_temp_file(self, format, name=None):
        """Return path to a new temporary subtitle file."""
        text = self.get_sample_text(format, name)
        path = aeidon.temp.create(format.extension)
        aeidon.temp.close(path)
        with open(path, "w") as fobj:
            fobj.write(text)
        return path

    def raises(self, exception, function, *args, **kwargs):
        """Assert that calling `function` raises `exception`."""
        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError("Function '%s' failed to raise exception '%s'"
                             % (repr(function), repr(exception)))

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
