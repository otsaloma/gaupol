# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
Base class for test classes.

All testing is to remain compatible with, but not dependent on py.test. All
test module names should be prefixed with "test_", class names with "Test",
function and method names with "test_".
"""


import os
import tempfile

from gaupol.base.cons import Framerate, Mode


TEXT_SUBRIP = \
'''1
00:00:13,400 --> 00:00:17,400
<i>ENERGIA presents</i>

2
00:00:27,480 --> 00:00:31,480
<i>A SAMULI TORSSONEN production</i>

3
00:00:42,400 --> 00:00:45,880
<i>A TIMO VUORENSOLA film</i>

4
00:02:36,960 --> 00:02:41,960
I would like to suggest, Emperor,
that you reconsider your plan.

5
00:02:42,040 --> 00:02:47,040
The scientists are comparing it to
Russian roulette.

6
00:02:47,160 --> 00:02:52,160
What theories we have on phenomena
like the maggot hole -

7
00:02:52,840 --> 00:02:57,840
indicate a tendency for continually
increasing disturbances.
'''

TEXT_MICRODVD = \
'''{321}{417}{Y:i}ENERGIA presents
{659}{755}{Y:i}A SAMULI TORSSONEN production
{1017}{1100}{Y:i}A TIMO VUORENSOLA film
{3763}{3883}I would like to suggest, Emperor,|that you reconsider your plan.
{3885}{4005}The scientists are comparing it to|Russian roulette.
{4008}{4128}What theories we have on phenomena|like the maggot hole -
{4144}{4264}indicate a tendency for continually|increasing disturbances.
'''


class Test(object):

    """
    Base class for test classes.

    All temporary file creations should add the temporary file path to
    self.files. These files will be deleted at the end of the test run.
    """

    def __init__(self):

        self.files = []

    def get_microdvd_path(self):
        """Get path to a temporary MicroDVD file."""

        fd, path = tempfile.mkstemp(prefix='gaupol.', suffix='.sub')
        fobj = os.fdopen(fd, 'w')
        fobj.write(TEXT_MICRODVD)
        fobj.close()

        self.files.append(path)
        return path

    def get_project(self):
        """Get a new project."""

        from gaupol.base.project import Project
        project = Project(Framerate.FR_23_976)

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
        fobj.write(TEXT_SUBRIP)
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

