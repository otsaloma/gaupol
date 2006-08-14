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


"""
Testing framework.

All testing is compatible with, but not dependent on py.test. All test module
names should are prefixed with 'test_', class names with 'Test', function and
method names with 'test_'.
"""


import os
import tempfile

from gaupol.base import cons


_MICRODVD_TEXT = \
"""{745}{784}I'm gonna get those fuckers!
{800}{911}This ain't the Bronx, right?|I'm gonna get the motherfuckers!
{927}{1007}I'm gonna corner him,|the motherfucker!
{1012}{1104}First one we see, straight up,|we whack the fucker!
{1108}{1141}Kneecap the fucker!
{1145}{1199}People just stood and watched.
{1205}{1264}- He stared at me.|- They're fuckin' losers.
{1272}{1318}The twins were there.
{1322}{1390}I swear on the Koran|I'll kill 'em both.
{1400}{1452}Who are these motherfuckers?
"""

_SUBRIP_TEXT = \
"""1
00:00:31,079 --> 00:00:32,706
I'm gonna get those fuckers!

2
00:00:33,382 --> 00:00:38,012
This ain't the Bronx, right?
I'm gonna get the motherfuckers!

3
00:00:38,654 --> 00:00:42,021
I'm gonna corner him,
the motherfucker!

4
00:00:42,224 --> 00:00:46,058
First one we see, straight up,
we whack the fucker!

5
00:00:46,228 --> 00:00:47,593
Kneecap the fucker!

6
00:00:47,763 --> 00:00:49,993
People just stood and watched.

7
00:00:50,265 --> 00:00:52,699
- He stared at me.
- They're fuckin' losers.

8
00:00:53,035 --> 00:00:54,969
The twins were there.

9
00:00:55,137 --> 00:00:57,970
I swear on the Koran
I'll kill 'em both.

10
00:00:58,407 --> 00:01:00,568
Who are these motherfuckers?
"""


class Test(object):

    """
    Base class for test classes.

    Instance variables:

        files: List of temporary filepaths

    All temporary file creations should add the temporary file path to
    self.files. These files will be deleted once teardown_method is run.
    """

    def __init__(self):

        self.files = []

    def get_microdvd_path(self):
        """Get path to a temporary MicroDVD file."""

        fd, path = tempfile.mkstemp(prefix='gaupol.', suffix='.sub')
        fobj = os.fdopen(fd, 'w')
        fobj.write(_MICRODVD_TEXT)
        fobj.close()

        self.files.append(path)
        return path

    def get_project(self):
        """Get a new project."""

        from gaupol.base.project import Project
        project = Project(cons.Framerate.FR_23_976)

        path = self.get_subrip_path()
        project.open_main_file(path, 'utf_8')
        self.files.append(path)

        path = self.get_microdvd_path()
        project.open_translation_file(path, 'utf_8')
        self.files.append(path)

        return project

    def get_subrip_path(self):
        """Get path to a temporary SubRip file."""

        fd, path = tempfile.mkstemp(prefix='gaupol.', suffix='.srt')
        fobj = os.fdopen(fd, 'w')
        fobj.write(_SUBRIP_TEXT)
        fobj.close()

        self.files.append(path)
        return path

    def setup_method(self, method):
        """Set proper state for executing tests in method."""

        pass

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        for path in self.files:
            try:
                os.remove(path)
            except OSError:
                pass
        self.files = []
