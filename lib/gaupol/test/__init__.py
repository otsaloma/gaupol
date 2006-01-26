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


"""Base class for test classes."""


import tempfile


SUBRIP_TEXT = \
'''1
00:00:13,400 --> 00:00:17,400
ENERGIA presents

2
00:00:27,480 --> 00:00:31,480
A SAMULI TORSSONEN production

3
00:00:42,400 --> 00:00:45,880
A TIMO VUORENSOLA film

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
'''{321}{417}ENERGIA presents
{659}{755}A SAMULI TORSSONEN production
{1017}{1100}A TIMO VUORENSOLA film
{3763}{3883}I would like to suggest, Emperor,|that you reconsider your plan.
{3885}{4005}The scientists are comparing it to|Russian roulette.
{4008}{4128}What theories we have on phenomena|like the maggot hole -
{4144}{4264}indicate a tendency for continually|increasing disturbances.
'''


class Test(object):

    """
    Base class for test classes.

    Test classes should inherit from this class and prefix all test methods
    with "test_". "__init__" acts as the set-up method and "destroy" as the
    tear-down method. run() should be called right after the class definition.

    Example:

    if __name__ == '__main__':

        from gaupol.test import Test

        class TestFoo(Test):

            test_foo(self):
                value = foo()
                assert foo is ...

        TestFoo().run()
    """

    def destroy(self):
        """Destroy instance variables."""
        pass

    def get_micro_dvd_path(self):
        """Write data to a temporary file and return its path."""

        path = tempfile.mkstemp()[1]

        sub_file = open(path, 'w')
        sub_file.write(MICRODVD_TEXT)
        sub_file.close()

        return path

    def get_subrip_path(self):
        """Write data to a temporary file and return its path."""

        path = tempfile.mkstemp()[1]

        sub_file = open(path, 'w')
        sub_file.write(SUBRIP_TEXT)
        sub_file.close()

        return path

    def run(self):
        """Run all tests."""

        print 'Testing...'
        for name in dir(self):
            if name.startswith('test'):
                print name
                getattr(self, name)()

        self.destroy()
