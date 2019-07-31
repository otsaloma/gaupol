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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""CSS styles and helper functions for styling."""

import aeidon
import gaupol
import os

from gi.repository import Gtk
from gi.repository import Pango

CSS_FILE = os.path.join(aeidon.DATA_DIR, "ui", "gaupol.css")
with open(CSS_FILE, "r") as f:
    CSS = f.read()


def _get_editor_font_css():
    """Return CSS for custom editor font."""
    font_desc = Pango.FontDescription("monospace")
    if (gaupol.conf.editor.custom_font and
        gaupol.conf.editor.use_custom_font):
        font_desc = Pango.FontDescription(gaupol.conf.editor.custom_font)
    # They fucking broke theming again with GTK 3.22.
    unit = "pt" if Gtk.check_version(3, 22, 0) is None else "px"
    css = """
    .gaupol-custom-font {{
        font-family: {family},monospace;
        font-size: {size}{unit};
        font-weight: {weight};
    }}""".format(
        family=font_desc.get_family().split(",")[0],
        size=int(round(font_desc.get_size() / Pango.SCALE)),
        unit=unit,
        weight=int(font_desc.get_weight()))
    css = css.replace("font-size: 0{unit};".format(unit=unit), "")
    css = css.replace("font-weight: 0;", "")
    css = "\n".join(filter(lambda x: x.strip(), css.splitlines()))
    return css

def load_css(widget):
    """Load CSS rules from file and conf for `widget`."""
    provider = Gtk.CssProvider()
    css = "\n".join((CSS, _get_editor_font_css()))
    provider.load_from_data(bytes(css.encode()))
    style = widget.get_style_context()
    priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    style.add_provider_for_screen(widget.get_screen(),
                                  provider,
                                  priority)

def _update_css(*args, **kwargs):
    """Update CSS rules for the default provider."""
    provider = Gtk.CssProvider()
    provider.load_from_data(bytes(_get_editor_font_css().encode()))

def use_font(widget, font):
    """Use `font` ("custom" or "monospace") for `widget`."""
    if not font: return
    load_css(widget)
    style = widget.get_style_context()
    style.add_class({
        "custom": "gaupol-custom-font",
        "monospace": "monospace",
    }[font])


gaupol.conf.editor.connect("notify::custom_font", _update_css)
gaupol.conf.editor.connect("notify::use_custom_font", _update_css)
