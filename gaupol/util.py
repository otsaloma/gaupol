# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Miscellaneous functions and decorators."""

import aeidon
import gaupol
import importlib.util
import inspect
import sys
import traceback
import webbrowser

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk


def char_to_px(nchar, font=None):
    """Convert characters to pixels."""
    if nchar < 0: return nchar
    label = Gtk.Label(label="etaoin shrdlu")
    gaupol.style.use_font(label, font)
    width = label.measure(Gtk.Orientation.HORIZONTAL, -1).natural
    return int(round(nchar * width/len(label.props.label)))

def delay_add(delay, function, *args, **kwargs):
    """Call `function` with `args` and `kwargs` once after `delay` (ms)."""
    def call_function(*args, **kwargs):
        function(*args, **kwargs)
        return False # to not be called again.
    return GLib.timeout_add(delay, call_function, *args, **kwargs)

def document_to_text_field(doc):
    """Return :attr:`gaupol.fields` item corresponding to `doc`."""
    if doc == aeidon.documents.MAIN:
        return gaupol.fields.MAIN_TEXT
    if doc == aeidon.documents.TRAN:
        return gaupol.fields.TRAN_TEXT
    raise ValueError("Invalid document: {!r}"
                     .format(doc))

def flash_dialog(dialog):
    """Run `dialog`, destroy it and return response."""
    response = run_dialog(dialog)
    dialog.destroy()
    return response

def get_content_size(widget, font=None):
    """Return the width and height desired by `widget`."""
    if isinstance(widget, Gtk.TextView):
        return get_text_view_size(widget, font)
    if isinstance(widget, Gtk.TreeView):
        return get_tree_view_size(widget, font)
    raise ValueError("Unsupported container type: {!r}"
                     .format(type(widget)))

def get_default_player():
    """Return the default video player to use for preview."""
    players = [aeidon.players.MPV, aeidon.players.MPLAYER, aeidon.players.VLC]
    players = [x for x in players if x.found]
    return players[0] if players else aeidon.players.MPV

def get_font():
    """Return custom font or blank string."""
    return (gaupol.conf.editor.custom_font if
            gaupol.conf.editor.use_custom_font and
            gaupol.conf.editor.custom_font else "")

def get_gst_version():
    """Return :mod:`Gst` version number as string or ``None``."""
    try:
        from gi.repository import Gst
        return ".".join(map(str, Gst.version()))
    except Exception:
        return None

def get_libspelling_version():
    """Return libspelling version number as string or ``None``."""
    try:
        from gi.repository import Spelling
        return str(Spelling._version)
    except Exception:
        return None

def get_preview_command():
    """Return command to use for lauching video player."""
    if gaupol.conf.preview.use_custom_command:
        return gaupol.conf.preview.custom_command
    if gaupol.conf.preview.force_utf_8:
        return gaupol.conf.preview.player.command_utf_8
    return gaupol.conf.preview.player.command

def get_text_view_size(text_view, font=None):
    """Return the width and height desired by `text_view`."""
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, False)
    label = Gtk.Label(label=text)
    gaupol.style.use_font(label, font)
    return (label.measure(Gtk.Orientation.HORIZONTAL, -1).natural
            + text_view.get_left_margin()
            + text_view.get_right_margin(),
            label.measure(Gtk.Orientation.VERTICAL, -1).natural)

def get_tree_view_size(tree_view, font=None):
    """Return the width and height desired by `tree_view`."""
    scroller = tree_view.get_parent()
    policy = scroller.get_policy()
    scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
    width = scroller.measure(Gtk.Orientation.HORIZONTAL, -1).natural
    height = scroller.measure(Gtk.Orientation.VERTICAL, -1).natural
    scroller.set_policy(*policy)
    return width, height

@aeidon.deco.once
def get_zebra_color(tree_view):
    """Return background color to use for tree view zebra-stripes."""
    # XXX: Zebra stripes would be faster and cleaner done with CSS
    # selectors :nth-child(odd) and :nth-child(even), but they don't
    # work: GtkTreeView has no per-row CSS nodes, the selectors match
    # the tree view widget itself among its siblings (tested 7/2026).
    # https://bugzilla.gnome.org/show_bug.cgi?id=709617#c1
    # Foreground color at low alpha composited over the background
    # gives a subtle stripe on any theme, light or dark.
    color = tree_view.get_color()
    color.alpha = 0.05
    return color

@aeidon.deco.once
def gst_available():
    """Return ``True`` if :mod:`Gst` and needed plugins are available."""
    try:
        from gi.repository import Gst
    except Exception:
        return False
    if not Gst.ElementFactory.find("playbin"):
        print("GStreamer found, but playbin missing.",
              "Try installing gst-plugins-base.",
              file=sys.stderr)
        return False
    if not Gst.ElementFactory.find("textoverlay"):
        print("GStreamer found, but textoverlay missing.",
              "Try installing gst-plugins-base.",
              file=sys.stderr)
        return False
    if not Gst.ElementFactory.find("timeoverlay"):
        print("GStreamer found, but timeoverlay missing.",
              "Try installing gst-plugins-base.",
              file=sys.stderr)
        return False
    if not Gst.ElementFactory.find("gtk4paintablesink"):
        print("GStreamer found, but gtk4paintablesink missing.",
              "Try installing gst-plugins-rs.",
              file=sys.stderr)
        return False
    if Gst.ElementFactory.find("vaapisink"):
        print("GStreamer-vaapi found, known to sometimes cause trouble.",
              "If video doesn't play, please try uninstalling it.",
              "See https://github.com/otsaloma/gaupol/issues/79",
              file=sys.stderr)
    return True

def hex_to_rgba(string):
    """Return a :class:`Gdk.RGBA` for hexadecimal `string`."""
    rgba = Gdk.RGBA()
    success = rgba.parse(string)
    if not success:
        raise ValueError("Parsing string {!r} failed".format(string))
    return rgba

def idle_add(function, *args, **kwargs):
    """Call `function` with `args` and `kwargs` when idle."""
    def call_function(*args, **kwargs):
        function(*args, **kwargs)
        return False # to not be called again.
    return GLib.idle_add(call_function, *args, **kwargs)

def install_module(name, obj):
    """
    Install `obj`'s module into the :mod:`gaupol` namespace.

    Typical call is of form::

        gaupol.util.install_module("foo", lambda: None)
    """
    gaupol.__dict__[name] = inspect.getmodule(obj)

def iterate_main():
    """Iterate the GLib main loop while events are pending."""
    context = GLib.MainContext.default()
    while context.pending():
        context.iteration(False)

def lines_to_px(nlines, font=None):
    """Convert lines to pixels."""
    if nlines < 0: return nlines
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    label = Gtk.Label(label=text)
    gaupol.style.use_font(label, font)
    height = label.measure(Gtk.Orientation.VERTICAL, -1).natural
    return int(round(nlines * height))

def load_module_from_file(name, path):
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def new_hbox(spacing):
    """Return a new horizontal :class:`Gtk.Box`."""
    return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                   spacing=spacing)

def new_vbox(spacing):
    """Return a new vertical :class:`Gtk.Box`."""
    return Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                   spacing=spacing)

def pack_start(box, widget):
    """Pack widget to box without expand."""
    box.append(widget)

def pack_start_expand(box, widget):
    """Pack widget to box with expand."""
    if box.get_orientation() == Gtk.Orientation.HORIZONTAL:
        widget.set_hexpand(True)
    else:
        widget.set_vexpand(True)
    box.append(widget)

def prepare_text_view(text_view):
    """Set spell-check, line-length margin and font properties."""
    if (gaupol.SpellChecker.available() and
        gaupol.conf.spell_check.inline):
        language = gaupol.conf.spell_check.language
        with aeidon.util.silent(Exception):
            checker = gaupol.SpellChecker(language)
            checker.attach(text_view)
    connect = gaupol.conf.editor.connect
    def update_margin(section, value, text_view):
        if gaupol.conf.editor.show_lengths_edit:
            return gaupol.ruler.connect_text_view(text_view)
        return gaupol.ruler.disconnect_text_view(text_view)
    connect("notify::show_lengths_edit", update_margin, text_view)
    update_margin(None, None, text_view)
    gaupol.style.use_font(text_view, "custom")

def raise_default(expression):
    """Raise :exc:`gaupol.Default` if `expression` evaluates to ``True``."""
    if expression:
        raise gaupol.Default

def rgba_to_hex(color):
    """Return hexadecimal string for :class:`Gdk.RGBA` `color`."""
    return "#{:02x}{:02x}{:02x}".format(
        int(color.red   * 255),
        int(color.green * 255),
        int(color.blue  * 255),
    )

def run_dialog(dialog):
    """
    Run `dialog` in a nested main loop and return response.

    A stand-in for ``Gtk.Dialog.run``, which was removed in GTK 4. Blocks in a
    nested main loop until the "response" signal, keeping callers simple,
    synchronous code. Closing the dialog window emits response
    ``Gtk.ResponseType.DELETE_EVENT``.
    """
    response = Gtk.ResponseType.NONE
    loop = GLib.MainLoop()
    def on_response(dialog, response_id):
        nonlocal response
        response = response_id
        loop.quit()
    def on_unrealize(dialog):
        # Don't hang if dialog is destroyed without a response.
        loop.quit()
    response_id = dialog.connect("response", on_response)
    unrealize_id = dialog.connect("unrealize", on_unrealize)
    dialog.present()
    loop.run()
    for handler in [response_id, unrealize_id]:
        if dialog.handler_is_connected(handler):
            dialog.disconnect(handler)
    return response

def scale_to_content(widget, min_nchar=0,  max_nchar=32768,
                     min_nlines=0, max_nlines=32768, font=None):
    """Set `widget's` size by content, but limited by `min` and `max`."""
    width, height = get_content_size(widget, font)
    width  = max(width, char_to_px(min_nchar, font))
    width  = min(width, char_to_px(max_nchar, font))
    height = max(height, lines_to_px(min_nlines, font))
    height = min(height, lines_to_px(max_nlines, font))
    parent = widget.get_parent()
    if isinstance(parent, Gtk.ScrolledWindow):
        # Vaguely account for possible scrollbars.
        return parent.set_size_request(width + 24, height + 24)
    widget.set_size_request(width, height)

def scale_to_size(widget, nchar, nlines, font=None):
    """Set `widget`'s size to `nchar` and `nlines`."""
    width  = char_to_px(nchar, font)
    height = lines_to_px(nlines, font)
    parent = widget.get_parent()
    if isinstance(parent, Gtk.ScrolledWindow):
        # Vaguely account for possible scrollbars.
        return parent.set_size_request(width + 24, height + 24)
    widget.set_size_request(width, height)

def separate_combo(store, itr, data=None):
    """Separator function for combo box models."""
    return store.get_value(itr, 0) == gaupol.COMBO_SEPARATOR

def set_cursor_busy(window):
    """Set mouse pointer busy when above window."""
    window.set_cursor_from_name("wait")
    iterate_main()

def set_cursor_normal(window):
    """Set mouse pointer normal when above window."""
    window.set_cursor_from_name("default")
    iterate_main()

def set_widget_margins(widget, margin):
    """Set equal margins on all sides of `widget`."""
    widget.set_margin_top(margin)
    widget.set_margin_bottom(margin)
    widget.set_margin_start(margin)
    widget.set_margin_end(margin)

def show_exception(exctype, value, tb):
    """A :class:`gaupol.DebugDialog` :attr`sys.excepthook`."""
    traceback.print_exception(exctype, value, tb)
    if not isinstance(value, Exception): return
    try: # to avoid recursion.
        dialog = gaupol.DebugDialog()
        dialog.set_text(exctype, value, tb)
        response = flash_dialog(dialog)
        if response == Gtk.ResponseType.NO:
            raise SystemExit(1)
    except Exception:
        traceback.print_exc()

def show_uri(uri):
    """Open `uri` in default application."""
    try:
        return Gio.AppInfo.launch_default_for_uri(uri)
    except Exception:
        # Launching fails on Windows and some misconfigured installations.
        # GError: No application is registered as handling this file
        # Operation not supported
        if uri.startswith(("http://", "https://")):
            return webbrowser.open(uri)
        raise # Exception

def text_field_to_document(field):
    """Return :attr:`aeidon.documents` item corresponding to `field`."""
    if field == gaupol.fields.MAIN_TEXT:
        return aeidon.documents.MAIN
    if field == gaupol.fields.TRAN_TEXT:
        return aeidon.documents.TRAN
    raise ValueError("Invalid field: {!r}"
                     .format(field))

def tree_path_to_row(path):
    """
    Convert `path` to a list row integer.

    `path` can be either a :class:`Gtk.Treepath` instance or a string
    representation of it (as commonly used by various callbacks).
    """
    if path is None: return None
    if isinstance(path, Gtk.TreePath):
        return path.get_indices()[0]
    if isinstance(path, str):
        return int(path)
    raise TypeError("Bad type {!r} for path {!r}"
                    .format(type(path), path))

def tree_row_to_path(row):
    """Convert list row integer to a :class:`Gtk.TreePath`."""
    if row is None: return None
    return Gtk.TreePath.new_from_string(str(row))
