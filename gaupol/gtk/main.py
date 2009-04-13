# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""GTK user interface initialization."""

# pylint: disable-msg=W0612

import atexit
import gaupol.gtk
import optparse
import os
import re
import sys
_ = gaupol.i18n._


def _check_dependencies():
    """Check existance and versions of dependencies."""

    if sys.version_info[:3] < (2, 5, 1):
        print "Python 2.5.1 or greater is required to run Gaupol."
        raise SystemExit(1)

    try:
        import gtk
        if gtk.pygtk_version < (2, 12, 0):
            raise ImportError
    except ImportError:
        print "PyGTK 2.12.0 or greater is required to run Gaupol."
        raise SystemExit(1)

    try:
        import gtk.glade
    except ImportError:
        print "Glade support in PyGTK is required to run Gaupol."
        raise SystemExit(1)

    try:
        import enchant
    except ImportError:
        print "PyEnchant not found;"
        print "spell-checking not possible."

    try:
        import chardet
    except ImportError:
        print "Universal Encoding Detector not found;"
        print "character encoding auto-detection not possible."

def _init_application(opts, args):
    """Initialize application and open files given as arguments."""

    from gaupol.gtk import dialogs
    sys.excepthook = dialogs.debug.show
    application = gaupol.gtk.Application()
    jump_row = None
    re_jump = re.compile(r"\+\d*")
    for arg in (x for x in args if re_jump.match(x) is not None):
        jump_row = (max(0, int(arg[1:]) - 1) if arg[1:] else -1)
        args.remove(arg)
    paths = [os.path.abspath(x) for x in args]
    if not opts.encoding in (None, "auto"):
        try: opts.encoding = gaupol.encodings.translate_code(opts.encoding)
        except ValueError:
            raise SystemExit("Unrecognized encoding '%s'." % opts.encoding)
    application.open_main_files(paths, opts.encoding)
    page = application.get_current_page()
    if (page is not None) and opts.translation_file:
        path = os.path.abspath(opts.translation_file)
        align_method = opts.align_method.upper()
        align_method = getattr(gaupol.align_methods, align_method)
        application.open_translation_file(path, opts.encoding, align_method)
    if (page is not None) and opts.video_file:
        path = os.path.abspath(opts.video_file)
        page.project.video_path = path
        application.update_gui()
    if (page is not None) and (jump_row is not None):
        page.view.set_focus(jump_row)
        page.view.scroll_to_row(jump_row)

def _init_configuration(path):
    """Initialize the configuration module from saved values."""

    default = os.path.join(gaupol.CONFIG_HOME_DIR, "gaupol.gtk.conf")
    path = (default if path is None else path)
    gaupol.gtk.conf.config_file = os.path.abspath(path)
    gaupol.gtk.conf.read()
    atexit.register(gaupol.gtk.conf.write)

def _list_encodings():
    """List all available character encodings."""

    encodings = [x[0] for x in gaupol.encodings.get_valid()]
    if gaupol.util.chardet_available():
        encodings.insert(0, "auto")
    print "\n".join(encodings)

def _move_eggs():
    """Move eggs to sys.path so that they are importable."""

    try:
        import enchant
        return
    except Exception:
        pass
    try:
        import pkg_resources
        pkg_resources.require("pyenchant")
    except Exception:
        pass

def _parse_args(args):
    """Parse and return options and arguments."""

    parser = optparse.OptionParser(
        formatter=optparse.IndentedHelpFormatter(2, 42),
        usage=_("gaupol [OPTION...] [FILE...] [+[NUM]]"),)

    parser.add_option(
        "--version",
        action="store_true",
        dest="version",
        default=False,
        help=_("show version number and exit"),)

    parser.add_option(
        "-c", "--config-file",
        action="store",
        type="string",
        metavar=_("FILE"),
        dest="config_file",
        default=None,
        help=_("set the configuration file used"),)

    parser.add_option(
        "-e", "--encoding",
        action="store",
        type="string",
        metavar=_("ENCODING"),
        dest="encoding",
        default=None,
        help=_("set the encoding used to open files"),)

    parser.add_option(
        "--list-encodings",
        action="store_true",
        dest="list_encodings",
        default=False,
        help=_("list all available character encodings"),)

    parser.add_option(
        "-t", "--translation-file",
        action="store",
        type="string",
        metavar=_("FILE"),
        dest="translation_file",
        default=None,
        help=_("open translation file"),)

    parser.add_option(
        "-a", "--align-method",
        action="store",
        type="string",
        metavar=_("METHOD"),
        dest="align_method",
        default="position",
        help=_("method used to align translation subtitles: "
            "'number' or 'position'"),)

    parser.add_option(
        "-v", "--video-file",
        action="store",
        type="string",
        metavar=_("FILE"),
        dest="video_file",
        default=None,
        help=_("select video file"),)

    return parser.parse_args(args)

def _show_version():
    """Show the version number."""

    print "gaupol %s" % gaupol.__version__

def main(args):
    """Parse arguments and start application."""

    _move_eggs()
    _check_dependencies()
    opts, args = _parse_args(args)
    if opts.list_encodings:
        return _list_encodings()
    if opts.version:
        return _show_version()
    gaupol.paths.xdg_copy_if_applicable()
    _init_configuration(opts.config_file)
    _init_application(opts, args)
    import gtk
    gtk.main()
