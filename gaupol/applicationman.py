# -*- coding: utf-8 -*-

# Copyright (C) 2015 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Initializing and managing Gaupol windows."""

# For historical reasons gaupol.Application has been effectively
# a Gtk.Window. So, the later introduced Gtk.Application is for
# us a gaupol.ApplicationManager and it doesn't actually manage
# much, but is more of a main function in the form of a class.

import aeidon
import argparse
import gaupol
import os
import re
import sys

from aeidon.i18n   import _
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("ApplicationManager",)


class ApplicationManager(Gtk.Application):

    """Initializing and managing Gaupol windows."""

    def __init__(self, args):
        """Initialize an :class:`ApplicationManager` instance."""
        GObject.GObject.__init__(self)
        self.menubar_builder = None
        self.set_application_id("io.otsaloma.gaupol")
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE)
        self.connect("activate", self._on_activate, args)
        self.connect("shutdown", self._on_shutdown)

    def _init_application(self, opts, args):
        """Initialize application and open files from `args`."""
        application = gaupol.Application()
        paths = list(map(os.path.abspath, args))
        application.open_main(paths, opts.encoding)
        page = application.get_current_page()
        if page is None: return
        if opts.translation_file is not None:
            path = os.path.abspath(opts.translation_file)
            method = opts.align_method.upper()
            method = getattr(aeidon.align_methods, method)
            application.open_translation(path, opts.encoding, method)
        if opts.video_file is not None:
            path = os.path.abspath(opts.video_file)
            page.project.video_path = path
            application.update_gui()
            application.load_video(path)
        if opts.jump is not None:
            page.view.set_focus(opts.jump)
            page.view.scroll_to_row(opts.jump)

    def _init_configuration(self):
        """Read configuration values from file."""
        gaupol.conf.path = os.path.join(
            aeidon.CONFIG_HOME_DIR, "gaupol.conf")
        gaupol.conf.read_from_file()
        if (gaupol.conf.general.dark_theme or
            os.getenv("GTK_THEME", "").endswith(":dark")):
            Gtk.Settings.get_default().set_property(
                "gtk-application-prefer-dark_theme", True)

    def _init_menubar(self):
        """Initialize the window menubar."""
        path = os.path.join(aeidon.DATA_DIR, "ui", "menubar.ui")
        self.menubar_builder = Gtk.Builder.new_from_file(path)
        self.set_menubar(self.menubar_builder.get_object("menubar"))

    def _on_activate(self, manager, args):
        """Initialize application and open files from `args`."""
        opts, args = self._parse_args(args)
        sys.excepthook = gaupol.util.show_exception
        self._init_configuration()
        self._init_menubar()
        self._init_application(opts, args)

    def _on_shutdown(self, manager):
        """Terminate application."""
        gaupol.conf.write_to_file()

    def _parse_args(self, args):
        """Parse and return options and arguments from `args`."""
        parser = argparse.ArgumentParser(
            usage=_("gaupol [OPTION...] [FILE...] [+[NUM]]"))

        parser.add_argument(
            "files",
            metavar=_("FILE..."),
            nargs="*",
            default=[],
            help=_("subtitle files to open"))

        parser.add_argument(
            "--version",
            action="version",
            version="gaupol {}".format(gaupol.__version__))

        parser.add_argument(
            "-e", "--encoding",
            action="store",
            metavar=_("ENCODING"),
            dest="encoding",
            default=None,
            help=_("set the character encoding used to open files"))

        parser.add_argument(
            "--list-encodings",
            action="store_true",
            dest="list_encodings",
            default=False,
            help=_("list all available character encodings"))

        parser.add_argument(
            "-t", "--translation-file",
            action="store",
            metavar=_("FILE"),
            dest="translation_file",
            default=None,
            help=_("open translation file"))

        parser.add_argument(
            "-a", "--align-method",
            action="store",
            metavar=_("METHOD"),
            dest="align_method",
            default="position",
            choices=["number", "position"],
            help=_("method used to align translation subtitles: 'number' or 'position'"))

        parser.add_argument(
            "-v", "--video-file",
            action="store",
            metavar=_("FILE"),
            dest="video_file",
            default=None,
            help=_("select video file"))

        args = parser.parse_args()
        args.jump = None
        if args.list_encodings:
            return self._print_encodings()
        if not args.encoding in (None, "auto"):
            args.encoding = aeidon.encodings.translate_code(args.encoding)
        # Parse row to jump to. If found, remove from args.files.
        for arg in filter(re.compile(r"\+\d*").match, args.files):
            args.jump = max(0, int(arg[1:]) - 1) if arg[1:] else -1
            args.files.remove(arg)
        return args, args.files

    def _print_encodings(self):
        """Print available character encodings and exit."""
        encodings = [x[0] for x in aeidon.encodings.get_valid()]
        if aeidon.util.chardet_available():
            encodings.insert(0, "auto")
        print(", ".join(encodings))
        raise SystemExit(0)
