# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Base class for unit test cases."""


from __future__ import with_statement

import atexit
import gaupol
import os
import tempfile


class TestCase(object):

    """Base class for unit test cases.

    Class variables:
     * files: Set of the paths of temporary files created
    """

    __metaclass__ = gaupol.Contractual
    files = set()

    def get_file_path_ensure(self, value, format):
        assert os.path.isfile(value)

    def get_file_path(self, format):
        """Get path to a temporary subtitle file."""

        text = self.get_file_text(format)
        fd, path = tempfile.mkstemp(format.extension, "gaupol.")
        with os.fdopen(fd, "w") as fobj:
            fobj.write(text)
        self.files.add(path)
        return path

    @gaupol.util.memoize
    def get_file_text(self, format):
        """Get subtitle file text."""

        dirname = os.path.abspath(os.path.dirname(__file__))
        while not dirname.endswith("gaupol"):
            dirname = os.path.abspath(os.path.join(dirname, ".."))
        basename = "%s.sample" % format.name.lower()
        path = os.path.join(dirname, "..", "doc", "formats", basename)
        with open(path, "r") as fobj:
            return fobj.read().strip()

    def get_microdvd_path_ensure(self, value):
        assert os.path.isfile(value)

    def get_microdvd_path(self):
        """Get path to a temporary MicroDVD file."""

        return self.get_file_path(gaupol.FORMAT.MICRODVD)

    def get_project(self):
        """Get a new project."""

        project = gaupol.Project()
        project.open_main(self.get_subrip_path(), "ascii")
        project.open_translation(self.get_microdvd_path(), "ascii")
        return project

    def get_subrip_path_ensure(self, value):
        assert os.path.isfile(value)

    def get_subrip_path(self):
        """Get path to a temporary SubRip file."""

        return self.get_file_path(gaupol.FORMAT.SUBRIP)

    def raises(self, exception, function, *args, **kwargs):
        """Assert that calling function raises exception."""

        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError

    # pylint: disable-msg=C0103
    def setUp(self):
        """Compatibility alias for 'setup_method'."""

        self.setup_method(None)

    def setup_method(self, method):
        """Set proper state for executing tests in method."""

        pass

    # pylint: disable-msg=C0103
    def tearDown(self):
        """Compatibility alias for 'teardown_method'."""

        self.teardown_method(None)

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        pass


def remove_files():
    """Remove temporary files created."""

    remove = gaupol.util.silent(OSError)(os.remove)
    while TestCase.files:
        remove(TestCase.files.pop())

atexit.register(remove_files)
