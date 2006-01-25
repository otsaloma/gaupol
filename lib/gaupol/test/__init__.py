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

    def run(self):
        """Run all tests."""

        print 'Testing...'
        for name in dir(self):
            if name.startswith('test'):
                print name
                getattr(self, name)()

        self.destroy()
