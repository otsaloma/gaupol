# -*- coding: utf-8 -*-

# Copyright (C) 2016 Osmo Salomaa
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""CSS styles and helper functions for styling."""

import aeidon
import gaupol
import os

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango

CSS_FILE = os.path.join(aeidon.DATA_DIR, "ui", "gaupol.css")
with open(CSS_FILE, "r") as f:
    CSS = f.read()

css_provider = None

def _get_editor_font_css():
    """Return CSS for custom editor font."""
    font_desc = Pango.FontDescription("monospace")
    if (gaupol.conf.editor.custom_font and
        gaupol.conf.editor.use_custom_font):
        font_desc = Pango.FontDescription(gaupol.conf.editor.custom_font)
    css = """
    .gaupol-custom-font {{
        font-family: {family},monospace;
        font-size: {size}pt;
        font-weight: {weight};
    }}""".format(
        family=font_desc.get_family().split(",")[0],
        size=int(round(font_desc.get_size() / Pango.SCALE)),
        weight=int(font_desc.get_weight()))
    css = css.replace("font-size: 0pt;", "")
    css = css.replace("font-weight: 0;", "")
    css = "\n".join(filter(lambda x: x.strip(), css.splitlines()))
    return css

def load_css(widget):
    """Load CSS rules from file and conf for `widget`."""
    global css_provider
    if css_provider is None:
        css_provider = Gtk.CssProvider()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, priority)
    _update_css()

def _update_css(*args, **kwargs):
    """Reload CSS rules from file and conf into the shared provider."""
    if css_provider is None: return
    css = "\n".join((CSS, _get_editor_font_css()))
    # load_from_string is new in GTK-4.12; load_from_data
    # is deprecated since 4.12 and its signature changed.
    css_provider.load_from_string(css)

def use_font(widget, font):
    """Use `font` ("custom" or "monospace") for `widget`."""
    if not font: return
    load_css(widget)
    widget.add_css_class({
        "custom": "gaupol-custom-font",
        "monospace": "monospace",
    }[font])


gaupol.conf.editor.connect("notify::custom_font", _update_css)
gaupol.conf.editor.connect("notify::use_custom_font", _update_css)
