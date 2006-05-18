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


"""Starting Gaupol GTK user interface."""


import gettext
import locale
import optparse
import os
import sys


def check_dependencies():
    """Check existance and versions of dependencies."""

    if sys.version_info[:3] < (2, 4, 0):
        print 'Python 2.4 or later is required to run Gaupol.'
        raise SystemExit(1)

    try:
        import gtk
        if gtk.pygtk_version < (2, 8, 0):
            raise ImportError
    except ImportError:
        print 'PyGTK 2.8.0 or later is required to run Gaupol.'
        raise SystemExit(1)

    try:
        import gtk.glade
    except ImportError:
        print 'Glade support in PyGTK is required to run Gaupol.'
        raise SystemExit(1)

def _move_eggs():
    """Move eggs to sys.path so that they are importable."""

    try:
        import enchant
    except ImportError:
        try:
            import pkg_resources
            try:
                pkg_resources.require('pyenchant')
            except pkg_resources.DistributionNotFound:
                pass
        except ImportError:
            pass
    except enchant.Error:
        pass

def _parse_args(args):
    """
    Parse arguments.

    Return options, arguments.
    """
    usage = 'gaupol [options] [files]'
    formatter = optparse.IndentedHelpFormatter(2, 42, None, True)
    parser = optparse.OptionParser(usage=usage, formatter=formatter)

    parser.add_option(
        '-t',
        '--no-translation',
        action='store_false',
        dest='translate',
        default=True,
        help='ignore possible translation (use english)'
    )

    return parser.parse_args(args)

def _prepare_gettext(translate):
    """Assign gettext domains."""

    if not translate:
        locale.setlocale(locale.LC_ALL, 'C')
        return

    import gtk.glade
    from gaupol.gtk.paths import LOCALE_DIR

    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain('gaupol', LOCALE_DIR)
    gettext.textdomain('gaupol')
    gtk.glade.bindtextdomain('gaupol', LOCALE_DIR)
    gtk.glade.textdomain('gaupol')

def main(args):
    """Start Gaupol and open files given as arguments."""

    check_dependencies()
    opts, args = _parse_args(args)
    _move_eggs()
    _prepare_gettext(opts.translate)

    import gobject
    gobject.threads_init()

    from gaupol.gtk.dialogs import debug
    sys.excepthook = debug.show

    from gaupol.gtk.application import Application
    application = Application()

    paths = []
    for arg in args[1:]:
        path = os.path.abspath(arg)
        if os.path.isfile(path):
            paths.append(path)
    if paths:
        application.open_main_files(paths)

    import gtk
    gtk.main()
