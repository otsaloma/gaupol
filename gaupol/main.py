# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010,2012 Osmo Salomaa
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

"""GTK+ user interface initialization."""

import aeidon
import atexit
import gaupol
import gettext
import locale
import optparse
import os
import re
import sys
_ = aeidon.i18n._

from gi.repository import Gtk


def _init_application(opts, args):
    """Initialize application and open files from `args`."""
    application = gaupol.Application()
    paths = list(map(os.path.abspath, args))
    application.open_main(paths, opts.encoding)
    page = application.get_current_page()
    if page is None: return
    if opts.translation_file is not None:
        path = os.path.abspath(opts.translation_file)
        align_method = opts.align_method.upper()
        align_method = getattr(aeidon.align_methods, align_method)
        application.open_translation(path, opts.encoding, align_method)
    if opts.video_file is not None:
        path = os.path.abspath(opts.video_file)
        page.project.video_path = path
        application.update_gui()
    if opts.jump is not None:
        page.view.set_focus(opts.jump)
        page.view.scroll_to_row(opts.jump)

def _init_configuration(path):
    """Read configuration values from file at `path`."""
    path = path or os.path.join(aeidon.CONFIG_HOME_DIR, "gaupol.conf")
    gaupol.conf.path = path
    gaupol.conf.read_from_file()
    atexit.register(gaupol.conf.write_to_file)

def _init_gettext():
    """Initialize translation settings."""
    locale.setlocale(locale.LC_ALL, "")
    try:
        # Not available on all platforms.
        locale.bindtextdomain("gaupol", aeidon.LOCALE_DIR)
        locale.textdomain("gaupol")
    except AttributeError: pass
    gettext.bindtextdomain("gaupol", aeidon.LOCALE_DIR)
    gettext.textdomain("gaupol")

def _on_parser_list_encodings(*args):
    """List all available character encodings and exit."""
    encodings = [x[0] for x in aeidon.encodings.get_valid()]
    if aeidon.util.chardet_available():
        encodings.insert(0, "auto")
    print(", ".join(encodings))
    raise SystemExit(0)

def _on_parser_version(*args):
    """Show the version number and exit."""
    print("gaupol {}".format(gaupol.__version__))
    raise SystemExit(0)

def _parse_args(args):
    """Parse and return options and arguments from `args`."""
    parser = optparse.OptionParser(
        formatter=optparse.IndentedHelpFormatter(2, 42),
        usage=_("gaupol [OPTION...] [FILE...] [+[NUM]]"))

    parser.add_option(
        "--version",
        action="callback",
        callback=_on_parser_version,
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
        help=_("set the character encoding used to open files"),)

    parser.add_option(
        "--list-encodings",
        action="callback",
        callback=_on_parser_list_encodings,
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

    opts, args = parser.parse_args(args)
    # Translate encoding if an alias given.
    if not opts.encoding in (None, "auto"):
        try: opts.encoding = aeidon.encodings.translate_code(opts.encoding)
        except ValueError:
            raise SystemExit("Unrecognized encoding: {}"
                             .format(repr(opts.encoding)))

    # Parse row to jump to.
    opts.jump = None
    re_jump = re.compile(r"\+\d*")
    for arg in filter(re_jump.match, args):
        opts.jump = (max(0, int(arg[1:])-1) if arg[1:] else -1)
        args.remove(arg)
    return opts, args

def main(args):
    """Parse arguments from `args` and start application."""
    opts, args = _parse_args(args)
    sys.excepthook = gaupol.util.show_exception
    _init_gettext()
    _init_configuration(opts.config_file)
    _init_application(opts, args)
    Gtk.main()
