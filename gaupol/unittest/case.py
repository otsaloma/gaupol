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

import os
import tempfile


class TestCase(object):

    """Base class for unit test cases.

    Instance variables:

        files: List of the paths of temporary files created
    """

    def __init__(self):

        self.files = []

    def get_file_path(self, format):
        """Get path to a temporary subtitle file."""

        text = self.get_text(format)
        fd, path = tempfile.mkstemp(prefix="gaupol.", suffix=".sub")
        with os.fdopen(fd, "w") as fobj:
            fobj.write(text)
        self.files.append(path)
        return path

    def get_microdvd_path(self):
        """Get path to a temporary MicroDVD file."""

        from gaupol import cons
        return self.get_file_path(cons.FORMAT.MICRODVD)

    def get_project(self):
        """Get a new project."""

        from gaupol.project import Project
        project = Project()
        project.open_main(self.get_subrip_path(), "ascii")
        project.open_translation(self.get_microdvd_path(), "ascii")
        return project

    def get_subrip_path(self):
        """Get path to a temporary SubRip file."""

        from gaupol import cons
        return self.get_file_path(cons.FORMAT.SUBRIP)

    def get_text(self, format):
        """Get subtitle file text."""

        dirname = os.path.abspath(os.path.dirname(__file__))
        while not dirname.endswith("gaupol"):
            dirname = os.path.abspath(os.path.join(dirname, ".."))
        basename = format.name.lower() + ".sample"
        path = os.path.join(dirname, "..", "doc", "formats", basename)
        with open(path, "r") as fobj:
            return fobj.read().strip()

    def is_regex(self, obj):
        """Return True if obj is a regular expression object."""

        for name in ("flags", "match", "pattern", "sub"):
            if not hasattr(obj, name):
                return False
        return True

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

        from gaupol import util
        remove = util.ignore_exceptions(OSError)(os.remove)
        for path in self.files:
            remove(path)
        self.files = []
