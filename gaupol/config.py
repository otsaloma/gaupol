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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Reading, writing and storing configurations."""

import aeidon
import copy
import gaupol
import json
import os
import sys

__all__ = ("ConfigurationStore",)


CONFIG_DEFAULTS = {
    "application_window": {
        "layout": gaupol.orientation.VERTICAL,
        "maximized": False,
        "position": [0, 0],
        "show_main_toolbar": True,
        "size": [700, 433],
        "toolbar_style": gaupol.toolbar_styles.ICONS,
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
    "extensions": {
        "active": [],
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
        # mpv is the only player that supports precise seek, others need a longer offset.
        "offset": 1.0 if gaupol.util.get_default_player() == aeidon.players.MPV else 5.0,
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
        "time_alpha": 1.0,
        "time_background": True,
        "time_color": "#ffffff",
        "time_font": "Monospace 14",
        "volume": None,
    },
}

CONFIG_ENUMS = {
    "application_window": {
        "layout": gaupol.orientation,
        "toolbar_style": gaupol.toolbar_styles,
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
    "extensions": {
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
                return "[{}]".format(", ".join(map(str, obj)))
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
        signal = "notify::{}".format(option)
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
        signal = "notify::{}".format(option)
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
        if not os.path.isfile(self.path): return
        encoding = aeidon.util.get_default_encoding()
        # Ignore possible encoding errors, which are only related to
        # saved file and directory names and not in any way critical.
        with open(self.path, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
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
            print("Failed to read configuration file {}: {!s}"
                  .format(self.path, error),
                  file=sys.stderr)

    def _read_option_line(self, line, sections, container, enums):
        """Read option-value line from configuration file."""
        option, value = [x.strip() for x in line.split("=", 1)]
        enum = enums.get(option, None)
        try:
            value = json.loads(value, cls=EnumDecoder, enum=enum)
        except (AttributeError, ValueError):
            return print("Failed to parse value '{}' of option '{}.{}' from configuration file '{}'."
                         .format(value, "::".join(sections), option, self.path),
                         file=sys.stderr)

        if hasattr(container, option) and value is None:
            # Discard a None-value for all non-extension options.
            # None-values are not used for any options, but might
            # accidentally bet set in some corner or error cases.
            # By discarding them here, we ensure a clean start.
            return print("Discarding value '{}' of option '{}.{}' from configuration file '{}'."
                         .format(value, "::".join(sections), option, self.path),
                         file=sys.stderr)

        if not hasattr(container, option):
            # Add attribute if it does not exist in container, which
            # has been initialized from config_defaults. This is needed
            # for extensions, defaults of options of which are not
            # known until later. Any possible obsolete non-extension
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

    def register_extension(self, name, defaults, enums=None):
        """
        Add section and options for extension.

        `name` should be preferrably the module name of the extension and
        it will appear in the section name as ``extensions::name``. `defaults`
        should be a dictionary of default values for options. `enums` should be
        a dictionary of :class:`aeidon.Enumeration` instances corresponding
        to enumeration items that appear in options.
        """
        self._defaults["extensions"].update({name: defaults})
        self.extensions.extend({name: copy.deepcopy(defaults)})
        self._enums["extensions"].update({name: enums or {}})

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        self.update(self._defaults)

    def _write_to_file(self):
        """Write values of configuration options to file."""
        if self.path is None: return
        self.general.version = gaupol.__version__
        aeidon.util.makedirs(os.path.dirname(self.path))
        encoding = aeidon.util.get_default_encoding()
        # Ignore possible encoding errors, which are only related to
        # saved file and directory names and not in any way critical.
        f = open(self.path, "w", encoding=encoding, errors="replace")
        root = self._flatten(self._root)
        defaults = self._flatten(self._defaults)
        for section in sorted(root):
            f.write("\n[{}]\n".format(section))
            for option in sorted(root[section]):
                value = root[section][option]
                json_value = json.dumps(
                    value, cls=EnumEncoder, ensure_ascii=False)
                # Discard removed options, but always keep
                # all options of all extensions.
                if (not section.startswith("extensions::")
                    and (not section in defaults or
                         not option in defaults[section])): continue
                # Write options that remain at their default value
                # (perhaps, but not necessarily unset) as commented out.
                if (section in defaults
                    and option in defaults[section]
                    and value == defaults[section][option]):
                    f.write("# ")
                f.write("{} = {}\n".format(option, json_value))
        f.close()

    def write_to_file(self):
        """Write values of configuration options to file."""
        try:
            self._write_to_file()
        except Exception as error:
            print("Failed to write configuration file {}: {!s}"
                  .format(self.path, error),
                  file=sys.stderr)
