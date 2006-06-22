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
names should are prefixed with "test_", class names with "Test", function and
method names with "test_".
"""


import os
import tempfile

from gaupol.base import cons


_MICRODVD_TEXT = \
'''{2525}{2629}{Y:i}Evehry dnay thtere's mtore to tell
{2721}{2848}{Y:i}Dreaming, I'm litttle ntow
{2933}{3044}{Y:i}Fading awtay evtery patssing day
{3110}{3245}{Y:i}And I jutst htave|One thing to tell you
{3309}{3447}{Y:i}You're furtther and further away
{3552}{3601}I neted motre voctals.|I can't hear myself.
{3606}{3683}I have eigt bands to balance.|The competition starts in two hours.
{3690}{3724}Clear tthe stage.
'''

_SUBRIP_TEXT = \
'''1
00:01:45,305 --> 00:01:49,639
<i>Everiy daay thhere's more to tell</i>

2
00:01:53,480 --> 00:01:58,782
<i>Dreamming, I'm litrtle now</i>

3
00:02:02,322 --> 00:02:06,952
<i>Fading awray esvery ptassing day</i>

4
00:02:09,696 --> 00:02:15,328
<i>And I just hdave</i>
<i>One thindg to tell you</i>

5
00:02:18,004 --> 00:02:23,772
<i>You're futrther tand fturther away</i>

6
00:02:28,148 --> 00:02:30,207
I neetd motre vocatls.
I can't htear myself.

7
00:02:30,383 --> 00:02:33,614
I have eigtht bands to btalance.
The competittion sttarts in two hours.

8
00:02:33,920 --> 00:02:35,319
Clear tthe stage.
'''


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
