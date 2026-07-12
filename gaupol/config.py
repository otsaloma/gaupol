# -*- coding: utf-8 -*-

# Copyright (C) 2010 Osmo Salomaa
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

"""Reading, writing and storing configurations."""

import aeidon
import copy
import gaupol
import json
import sys

CONFIG_DEFAULTS = {
    "application_window": {
        "layout": gaupol.orientation.VERTICAL,
        "maximized": False,
        "size": [700, 433],
    },
    "capitalization": {
        "country": "",
        "language": "",
        "script": "Latn",
    },
    "common_error": {
        "classes": ["Human", "OCR"],
        "country": "",
        "language": "",
        "script": "Latn",
    },
    "duration_adjust": {
        "gap": 0.0,
        "lengthen": True,
        "maximum": 6.0,
        "minimum": 1.5,
        "speed": 15.0,
        "shorten": False,
        "target": gaupol.targets.CURRENT,
        "use_minimum": True,
        "use_gap": True,
        "use_maximum": False,
    },
    "general": {
        "dark_theme": False,
        "diff_color_change": "#ffff0033",
        "diff_color_delete": "#ff555533",
        "diff_color_insert": "#00ff0033",
        "version": None,
    },
    "editor": {
        "custom_font": ("Consolas 9" if sys.platform == "win32"
                        else "monospace"),

        "custom_framerates": [],
        "field_order": [
            gaupol.fields.NUMBER,
            gaupol.fields.START,
            gaupol.fields.END,
            gaupol.fields.DURATION,
            gaupol.fields.MAIN_TEXT,
            gaupol.fields.TRAN_TEXT,
        ],
        "framerate": aeidon.framerates.FPS_23_976,
        "length_unit": gaupol.length_units.EM,
        "mode": aeidon.modes.TIME,
        "show_lengths_cell": True,
        "show_lengths_edit": True,
        "stretch_length": 0.05,
        "use_custom_font": True,
        "use_zebra_stripes": True,
        "visible_fields": [
            gaupol.fields.NUMBER,
            gaupol.fields.START,
            gaupol.fields.END,
            gaupol.fields.DURATION,
            gaupol.fields.MAIN_TEXT,
        ],
    },
    "encoding": {
        "fallback": ["utf_8", "cp1252"],
        "try_auto": True,
        "try_locale": True,
        "visible": ["utf_8", "cp1252"],
    },
    "file": {
        "align_method": aeidon.align_methods.POSITION,
        "directory": "",
        "encoding": "utf_8",
        "format": aeidon.formats.SUBRIP,
        "newline": aeidon.util.get_default_newline(),
    },
    "framerate_convert": {
        "target": gaupol.targets.CURRENT,
    },
    "hearing_impaired": {
        "country": "",
        "language": "",
        "script": "Latn",
    },
    "join_split_words": {
        "join": True,
        "split": False,
    },
    "line_break": {
        "country": "",
        "language": "",
        "length_unit": gaupol.length_units.EM,
        "max_length": 24,
        "max_lines": 3,
        "script": "Latn",
        "skip_max_length": 24,
        "skip_max_lines": 3,
        "use_skip_max_length": True,
        "use_skip_max_lines": True,
    },
    "position_shift": {
        "target": gaupol.targets.CURRENT,
    },
    "position_transform": {
        "target": gaupol.targets.CURRENT,
    },
    "preview": {
        "custom_command": "",
        "force_utf_8": True,
        "offset": 1.0,
        "player": gaupol.util.get_default_player(),
        "use_custom_command": False,
    },
    "recent": {
        "show_not_found": False,
    },
    "search": {
        "fields": [gaupol.fields.MAIN_TEXT],
        "ignore_case": True,
        "regex": False,
        "target": gaupol.targets.CURRENT,
    },
    "spell_check": {
        "field": gaupol.fields.MAIN_TEXT,
        "inline": False,
        "language": "en",
        "size": [500, 309],
        "target": gaupol.targets.CURRENT,
    },
    "subtitle_insert": {
        "above": False,
    },
    "text_assistant": {
        "field": gaupol.fields.MAIN_TEXT,
        "maximized": False,
        "pages": [],
        "remove_blank": True,
        "size": [700, 433],
        "target": gaupol.targets.CURRENT,
    },
    "video_player": {
        "autoplay": True,
        "context_length": 1.0,
        "line_alignment": "center",
        "seek_length": 30.0,
        "subtitle_alpha": 1.0,
        "subtitle_background": True,
        "subtitle_color": "#ffffff",
        "subtitle_font": "Sans 18",
        "subtitle_position_horizontal": "center",
        "subtitle_position_vertical": "bottom",
        "time_alpha": 1.0,
        "time_background": True,
        "time_color": "#ffffff",
        "time_font": "Monospace 14",
        "time_position_horizontal": "right",
        "time_position_vertical": "top",
        "volume": None,
    },
}

CONFIG_ENUMS = {
    "application_window": {
        "layout": gaupol.orientation,
    },
    "duration_adjust": {
        "target": gaupol.targets,
    },
    "editor": {
        "field_order": gaupol.fields,
        "framerate": aeidon.framerates,
        "length_unit": gaupol.length_units,
        "mode": aeidon.modes,
        "visible_fields": gaupol.fields,
    },
    "file": {
        "align_method": aeidon.align_methods,
        "format": aeidon.formats,
        "newline": aeidon.newlines,
    },
    "framerate_convert": {
        "target": gaupol.targets,
    },
    "line_break": {
        "length_unit": gaupol.length_units,
    },
    "position_shift": {
        "target": gaupol.targets,
    },
    "position_transform": {
        "target": gaupol.targets,
    },
    "preview": {
        "player": aeidon.players,
    },
    "search": {
        "fields": gaupol.fields,
        "target": gaupol.targets,
    },
    "spell_check": {
        "field": gaupol.fields,
        "target": gaupol.targets,
    },
    "text_assistant": {
        "field": gaupol.fields,
        "target": gaupol.targets,
    },
}

class EnumDecoder(json.JSONDecoder):

    """JSON decoder for enumerations of :mod:`aeidon` and :mod:`gaupol`."""

    def __init__(self, *args, **kwargs):
        """
        Initialize an :class:`EnumDecoder` instance.

        `kwargs` should contain an "enum" key with a value of ``None``
        if not decoding an enumeration or the corresponding
        :class:`aeidon.Enumeration` instance if decoding an enumeration.
        """
        self.enum = kwargs["enum"]
        del kwargs["enum"]
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, string):
        """Return Python object matching JSON `string`."""
        if self.enum is None:
            return json.JSONDecoder.decode(self, string)
        if string.startswith("[") and string.endswith("]"):
            return [getattr(self.enum, x.strip())
                    for x in string[1:-1].split(",")]
        return getattr(self.enum, string)

class EnumEncoder(json.JSONEncoder):

    """JSON encoder for enumerations of :mod:`aeidon` and :mod:`gaupol`."""

    def encode(self, obj):
        """Return JSON string matching `obj`."""
        if isinstance(obj, aeidon.EnumerationItem):
            return str(obj)
        if isinstance(obj, (list, tuple)) and obj:
            if isinstance(obj[0], aeidon.EnumerationItem):
                items = ", ".join(map(str, obj))
                return f"[{items}]"
        return json.JSONEncoder.encode(self, obj)

class ConfigurationStore(gaupol.AttributeDictionary):

    """
    Reading, writing and storing configurations.

    :cvar _defaults: Dictionary of default values of options
    :cvar _enums: Dictionary of :class:`aeidon.Enumeration` instances
    :ivar path: Path to user's local configuration file
    """

    _defaults = copy.deepcopy(CONFIG_DEFAULTS)
    _enums = copy.deepcopy(CONFIG_ENUMS)

    def __init__(self):
        """Initialize a :class:`ConfigurationStore` instance."""
        root = copy.deepcopy(self._defaults)
        gaupol.AttributeDictionary.__init__(self, root)
        self.path = None

    def __setattr__(self, name, value):
        """Avoid accidentally setting a tuple."""
        if isinstance(value, tuple):
            value = list(value)
        return gaupol.AttributeDictionary.__setattr__(self, name, value)

    def connect_notify(self, sections, option, obj, *args):
        """Connect `option`'s notify signal to `obj`'s callback method."""
        if isinstance(sections, str):
            sections = (sections,)
        container = self
        for section in sections:
            container = getattr(container, section)
        signal = f"notify::{option}"
        method_name = "_on_conf_{}_{}".format(
            "_".join(sections),
            signal.replace("::", "_"))
        if not hasattr(obj, method_name):
            method_name = method_name[1:]
        method = getattr(obj, method_name)
        container.connect(signal, method, *args)

    def disconnect_notify(self, sections, option, obj):
        """Disconnect `option`'s notify signal from `obj`'s callback method."""
        if isinstance(sections, str):
            sections = (sections,)
        container = self
        for section in sections:
            container = getattr(container, section)
        signal = f"notify::{option}"
        method_name = "_on_conf_{}_{}".format(
            "_".join(sections),
            signal.replace("::", "_"))
        if not hasattr(obj, method_name):
            method_name = method_name[1:]
        method = getattr(obj, method_name)
        container.disconnect(signal, method)

    def _flatten(self, values):
        """Return a flattened version of `values` dictionary."""
        def flatten(deep, parent):
            flat_dict = {parent: {}}
            deep = copy.deepcopy(deep)
            for key, value in deep.items():
                if isinstance(value, dict):
                    key = "::".join((parent, key))
                    value = flatten(value, key)
                    flat_dict.update(value)
                else: # Non-dictionary key.
                    flat_dict[parent][key] = value
            if not flat_dict[parent]:
                del flat_dict[parent]
            return flat_dict
        final_dict = {}
        values = copy.deepcopy(values)
        for key, value in values.items():
            if isinstance(value, dict):
                final_dict.update(flatten(value, key))
            else: # Non-dictionary key.
                final_dict[key] = value
        return final_dict

    def query_default(self, sections, option):
        """Return default value of configuration option."""
        if isinstance(sections, str):
            sections = (sections,)
        container = self._defaults
        for section in sections:
            container = container[section]
        return container[option]

    def _read_from_file(self):
        """Read values of configuration options from file."""
        if self.path is None: return
        if not self.path.is_file(): return
        encoding = aeidon.util.get_default_encoding()
        # Ignore possible encoding errors, which are only related to
        # saved file and directory names and not in any way critical.
        lines = self.path.read_text(encoding=encoding, errors="replace")
        lines = [x.strip() for x in lines.split("\n")]
        lines = [x for x in lines if x and not x.startswith("#")]
        sections, container, enums = None, None, None
        for line in lines:
            if line.startswith("[") and line.endswith("]"):
                sections, container, enums = self._read_section_line(line)
            else: # OPTION = VALUE
                if sections is None or container is None or enums is None:
                    raise ValueError("Missing section header?")
                self._read_option_line(line, sections, container, enums)

    def read_from_file(self):
        """Read values of configuration options from file."""
        try:
            self._read_from_file()
        except Exception as error:
            print(f"Failed to read configuration file {self.path}: {error!s}",
                  file=sys.stderr)

    def _read_option_line(self, line, sections, container, enums):
        """Read option-value line from configuration file."""
        option, value = [x.strip() for x in line.split("=", 1)]
        enum = enums.get(option, None)
        try:
            value = json.loads(value, cls=EnumDecoder, enum=enum)
        except (AttributeError, ValueError):
            section = "::".join(sections)
            return print(f"Failed to parse value '{value}' of option '{section}.{option}' from configuration file '{self.path}'.",
                         file=sys.stderr)

        if hasattr(container, option) and value is None:
            # Discard None-values. They are not used for any options,
            # but might accidentally bet set in some corner or error
            # cases. By discarding them here, we ensure a clean start.
            section = "::".join(sections)
            return print(f"Discarding value '{value}' of option '{section}.{option}' from configuration file '{self.path}'.",
                         file=sys.stderr)

        if not hasattr(container, option):
            # Add attribute if it does not exist in container, which
            # has been initialized from CONFIG_DEFAULTS. Any obsolete
            # options created here will be removed before writing in
            # write_to_file.
            container.add_attribute(option, value)
        setattr(container, option, value)

    def _read_section_line(self, line):
        """Read section header line from configuration file."""
        sections = line[1:-1].strip().split("::")
        container = self
        enums = self._enums
        for section in sections:
            if not hasattr(container, section):
                container.add_attribute(section, {})
            container = getattr(container, section)
            enums = enums.get(section, {})
        return sections, container, enums

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        self.update(self._defaults)

    def _write_to_file(self):
        """Write values of configuration options to file."""
        if self.path is None: return
        self.general.version = gaupol.__version__
        aeidon.util.makedirs(self.path.parent)
        encoding = aeidon.util.get_default_encoding()
        # Ignore possible encoding errors, which are only related to
        # saved file and directory names and not in any way critical.
        with open(self.path, "w", encoding=encoding, errors="replace") as f:
            root = self._flatten(self._root)
            defaults = self._flatten(self._defaults)
            for section in sorted(root):
                f.write(f"\n[{section}]\n")
                for option in sorted(root[section]):
                    value = root[section][option]
                    json_value = json.dumps(
                        value, cls=EnumEncoder, ensure_ascii=False)
                    # Discard removed options.
                    if (not section in defaults or
                        not option in defaults[section]): continue
                    # Write options that remain at their default value
                    # (perhaps, but not necessarily unset) as commented out.
                    if (section in defaults
                        and option in defaults[section]
                        and value == defaults[section][option]):
                        f.write("# ")
                    f.write(f"{option} = {json_value}\n")

    def write_to_file(self):
        """Write values of configuration options to file."""
        try:
            self._write_to_file()
        except Exception as error:
            print(f"Failed to write configuration file {self.path}: {error!s}",
                  file=sys.stderr)
