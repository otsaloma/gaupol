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

from .samples import MICRODVD_TEXT, SUBRIP_TEXT


class TestCase(object):

    """Base class for unit test cases.

    Instance variables:

        files: List of the paths of temporary files created
    """

    # pylint: disable-msg=C0103

    def __init__(self):

        self.files = []

    def get_microdvd_path(self):
        """Get path to a temporary MicroDVD file."""

        # pylint: disable-msg=E0602
        fd, path = tempfile.mkstemp(prefix="gaupol.", suffix=".sub")
        with os.fdopen(fd, "w") as fobj:
            fobj.write(MICRODVD_TEXT)
        self.files.append(path)
        return path

    def get_project(self):
        """Get a new project."""

        from gaupol.project import Project
        project = Project()
        project.open_main(self.get_subrip_path(), "ascii")
        project.open_translation(self.get_microdvd_path(), "ascii")
        return project

    def get_subrip_path(self):
        """Get path to a temporary SubRip file."""

        # pylint: disable-msg=E0602
        fd, path = tempfile.mkstemp(prefix="gaupol.", suffix=".srt")
        with os.fdopen(fd, "w") as fobj:
            fobj.write(SUBRIP_TEXT)
        self.files.append(path)
        return path

    def is_regex(self, obj):
        """Return True if obj is a regular expression object."""

        is_regex = True
        for name in ("pattern", "flags", "match", "sub"):
            is_regex = is_regex and hasattr(obj, name)
        return is_regex

    def setUp(self):
        """Compatibility alias for 'setup_method'."""

        self.setup_method(None)

    def setup_method(self, method):
        """Set proper state for executing tests in method."""

        pass

    def tearDown(self):
        """Compatibility alias for 'teardown_method'."""

        self.teardown_method(None)

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        for path in self.files:
            try:
                os.remove(path)
            except OSError:
                pass
        self.files = []
