# Copyright (C) 2005-2008 Osmo Salomaa
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

import atexit
import gaupol
import os

__all__ = ("TestCase",)


class TestCase(object):

    """Base class for unit test cases."""

    __metaclass__ = gaupol.Contractual

    def get_file_path_ensure(self, value, format, name=None):
        assert os.path.isfile(value)

    def get_file_path(self, format, name=None):
        """Return path to a temporary subtitle file."""

        text = self.get_file_text(format, name)
        path = gaupol.temp.create(format.extension)
        gaupol.temp.close(path)
        with open(path, "w") as fobj:
            fobj.write(text)
        atexit.register(gaupol.temp.remove, path)
        return path

    def get_file_text_ensure(self, value, format, name=None):
        assert value.count("a") > 10

    @gaupol.deco.memoize
    def get_file_text(self, format, name=None):
        """Return sample subtitle file text."""

        name = name or format.name.lower()
        basename = "".join((name, format.extension))
        path = os.path.join(gaupol.DATA_DIR, "samples", basename)
        with open(path, "r") as fobj:
            return fobj.read().strip()

    def get_microdvd_path_ensure(self, value):
        assert os.path.isfile(value)

    def get_microdvd_path(self):
        """Return path to a temporary MicroDVD file."""

        return self.get_file_path(gaupol.formats.MICRODVD)

    def get_project_ensure(self, value):
        assert value.subtitles

    def get_project(self):
        """Return a new project with both files open."""

        project = gaupol.Project()
        project.open_main(self.get_subrip_path(), "ascii")
        project.open_translation(self.get_microdvd_path(), "ascii")
        return project

    def get_subrip_path_ensure(self, value):
        assert os.path.isfile(value)

    def get_subrip_path(self):
        """Return path to a temporary SubRip file."""

        return self.get_file_path(gaupol.formats.SUBRIP)

    def raises(self, exception, function, *args, **kwargs):
        """Assert that calling function raises exception."""

        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError

    def setUp(self):
        """Compatibility alias for 'setup_method'."""

        self.setup_method(None)

    def setup_method(self, method):
        """Set state for executing tests in method."""

        pass

    def tearDown(self):
        """Compatibility alias for 'teardown_method'."""

        self.teardown_method(None)

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        pass

    def test___init__(self):
        """Make sure setup_method is run even if no actual tests exist."""

        pass
