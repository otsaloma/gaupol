# Copyright (C) 2005 Osmo Salomaa
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


"""Test functions and classes."""


import inspect
import os
import tempfile
import time
import traceback

from gaupol.base.project import Project
from gaupol.constants    import Mode


SUBRIP_TEXT = \
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

MICRODVD_TEXT = \
'''{321}{417}{Y:i}ENERGIA presents
{659}{755}{Y:i}A SAMULI TORSSONEN production
{1017}{1100}{Y:i}A TIMO VUORENSOLA film
{3763}{3883}I would like to suggest, Emperor,|that you reconsider your plan.
{3885}{4005}The scientists are comparing it to|Russian roulette.
{4008}{4128}What theories we have on phenomena|like the maggot hole -
{4144}{4264}indicate a tendency for continually|increasing disturbances.
'''


def timefunction(function):
    """Decorator for functions to be timed."""

    def wrapper(*args, **kwargs):

        start = time.time()
        function(*args, **kwargs)
        end = time.time()

        print '%.3f %s' % (end - start, function.__name__)

    return wrapper

def timemethod(function):
    """Decorator for methods to be timed."""

    def wrapper(*args, **kwargs):

        start = time.time()
        function(*args, **kwargs)
        end = time.time()

        print '%.3f %s.%s.%s' % (
            end - start,
            args[0].__class__.__module__,
            args[0].__class__.__name__,
            function.__name__
        )

    return wrapper


class Test(object):

    """
    Base class for test classes.

    Test classes should inherit from this class and prefix all test methods
    with "test_". "__init__" acts as the set-up method and "destroy" as the
    tear-down method. run() should be called right after the class definition.

    All temporary file creations should also add the temporary file path to
    self.files. These files will be deleted at the end of the run() method.

    Example:

    if __name__ == '__main__':

        from gaupol.test import Test

        class TestFoo(Test):

            def test_foo(self):

                value = foo()
                assert foo is True

        TestFoo().run()
    """

    def __init__(self):

        self.files = []

    def destroy(self):
        """Destroy instance variables (teardown)."""
        pass

    def get_micro_dvd_path(self):
        """Write data to a temporary Micro DVD file and return its path."""

        path = tempfile.mkstemp(prefix='gaupol.', suffix='.sub')[1]

        sub_file = open(path, 'w')
        sub_file.write(MICRODVD_TEXT)
        sub_file.close()

        self.files.append(path)
        return path

    def get_project(self):
        """Initialize a project and return it."""

        project = Project(0)

        path = self.get_subrip_path()
        project.open_main_file(path, 'utf_8')
        self.files.append(path)

        path = self.get_micro_dvd_path()
        project.open_translation_file(path, 'utf_8')
        self.files.append(path)

        return project

    def get_subrip_path(self):
        """Write data to a temporary SubRip file and return its path."""

        path = tempfile.mkstemp(prefix='gaupol.', suffix='.srt')[1]

        sub_file = open(path, 'w')
        sub_file.write(SUBRIP_TEXT)
        sub_file.close()

        self.files.append(path)
        return path

    def remove_files(self):
        """Remove temporary files."""

        for path in self.files:
            try:
                os.remove(path)
            except OSError:
                pass

        self.files = []

    def run(self):
        """Run all tests and do clean-up."""

        print '  ' + self.__class__.__name__
        for name, value in inspect.getmembers(self):
            if not name.startswith('test'):
                continue
            if not inspect.ismethod(value):
                continue
            print '    ' + name
            try:
                value()
            except:
                traceback.print_exc()
                break

        self.destroy()
        self.remove_files()
