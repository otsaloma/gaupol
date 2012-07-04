# -*- coding: utf-8-unix -*-

# Copyright (C) 2010 Osmo Salomaa
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

"""Reading, writing and storing configurations."""

import aeidon
import gaupol
import json
import os
import sys

__all__ = ("ConfigurationStore",)


config_defaults = {
    "application_window": {
        "maximized": False,
        "position": [0, 0],
        "show_main_toolbar": True,
        "show_statusbar": True,
        "show_video_toolbar": False,
        "size": [700, 433],
        "toolbar_style": gaupol.toolbar_styles.DEFAULT,
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
    "debug": {
        "text_editor": "gedit +$LINENO $FILE",
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
        "version": None,
        },
    "editor": {
        "custom_font": "",
        "field_order": [gaupol.fields.NUMBER,
                        gaupol.fields.START,
                        gaupol.fields.END,
                        gaupol.fields.DURATION,
                        gaupol.fields.MAIN_TEXT,
                        gaupol.fields.TRAN_TEXT],

        "framerate": aeidon.framerates.FPS_23_976,
        "length_unit": gaupol.length_units.EM,
        "mode": aeidon.modes.TIME,
        "show_lengths_cell": True,
        "show_lengths_edit": True,
        "undo_limit": 50,
        "use_custom_font": False,
        "use_undo_limit": False,
        "visible_fields": [gaupol.fields.NUMBER,
                           gaupol.fields.START,
                           gaupol.fields.END,
                           gaupol.fields.DURATION,
                           gaupol.fields.MAIN_TEXT],
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
        "encoding": aeidon.util.get_default_encoding() or "utf_8",
        "format": aeidon.formats.SUBRIP,
        "max_recent": 10,
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
        "max_deviation": 0.16,
        "max_length": 28,
        "max_lines": 2,
        "script": "Latn",
        "skip_max_length": 28,
        "skip_max_lines": 3,
        "use_skip_max_length": True,
        "use_skip_max_lines": True,
        },
    "output_window": {
        "maximized": False,
        "position": [0, 0],
        "show": False,
        "size": [600, 371],
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
        "offset": 5.0,
        "player": (aeidon.players.VLC if sys.platform == "win32"
                   else aeidon.players.MPLAYER),

        "use_custom_command": False,
        },
    "search": {
        "fields": [gaupol.fields.MAIN_TEXT],
        "ignore_case": True,
        "max_history": 10,
        "regex": False,
        "target": gaupol.targets.CURRENT,
        },
    "speech_recognition": {
        "acoustic_model": "",
        "advance_length": 100,
        "lang_model": "",
        "noise_level": 256,
        "phonetic_dict": "",
        "silence_length": 300,
        "use_custom_models": False,
        },
    "spell_check": {
        "field": gaupol.fields.MAIN_TEXT,
        "inline": False,
        "language": aeidon.locales.get_system_code() or "en",
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
    }

config_enums = {
    "application_window": {
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
        Initialize a :class:`EnumDecoder` object.

        `kwargs` should contain an "enum" key with a value of ``None`` if not
        decoding an enumeration or the corresponding
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


class ConfigurationStore(gaupol.AttributeDictionary):

    """
    Reading, writing and storing configurations.

    :cvar _defaults: Dictionary of default values of options
    :cvar _enums: Dictionary of :class:`aeidon.Enumeration` instances
    :ivar path: Path to user's local configuration file
    """

    _defaults = config_defaults
    _enums = config_enums

    def __init__(self):
        """Initialize a :class:`ConfigurationStore` object."""
        root = aeidon.util.copy_dict(self._defaults)
        gaupol.AttributeDictionary.__init__(self, root)
        self.path = None

    def _flatten(self, values):
        """Return a flattened version of `values` dictionary."""
        def flatten(deep, parent):
            flat_dict = {parent: {}}
            deep = aeidon.util.copy_dict(deep)
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
        values = aeidon.util.copy_dict(values)
        for key, value in values.items():
            if isinstance(value, dict):
                final_dict.update(flatten(value, key))
            else: # Non-dictionary key.
                final_dict[key] = value
        return final_dict

    def connect_notify(self, sections, option, obj, *args):
        """Connect `option`'s notify signal to `obj`'s callback method."""
        if isinstance(sections, str):
            sections = (sections,)
        container = self
        for section in sections:
            container = getattr(container, section)
        signal = "notify::{}".format(option)
        method_name = "_on_conf_{}_{}".format("_".join(sections),
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
        method_name = "_on_conf_{}_{}".format("_".join(sections),
                                              signal.replace("::", "_"))

        if not hasattr(obj, method_name):
            method_name = method_name[1:]
        method = getattr(obj, method_name)
        container.disconnect(signal, method)

    def query_default(self, sections, option):
        """
        Return default value of configuration option.

        Raise :exc:`KeyError` if section or option not found.
        """
        if isinstance(sections, str):
            sections = (sections,)
        container = self._defaults
        for section in sections:
            container = container[section]
        return container[option]

    def read_from_file(self):
        """
        Read values of configuration options from file.

        Raise :exc:`IOError` if reading file fails.
        Raise :exc:`UnicodeError` if decoding file fails.
        Fail silently if :attr:`path` is not set.
        """
        if self.path is None: return
        if not os.path.isfile(self.path): return
        encoding = aeidon.util.get_default_encoding()
        try:
            # Ignore all decoding errors, since all keys and all standard
            # values are all ASCII. This will only mangle recent etc.
            # filenames, which are always checked for existance anyway.
            lines = open(self.path,
                         "r",
                         encoding=encoding,
                         errors="ignore").readlines()

        except IOError:
            aeidon.util.print_read_io(sys.exc_info(), self.path)
            raise # IOError
        except UnicodeError:
            aeidon.util.print_read_unicode(sys.exc_info(), self.path, encoding)
            raise # UnicodeError
        lines = [x.strip() for x in lines]
        lines = [x for x in lines if x and not x.startswith("#")]
        for line in lines:
            if line.startswith("[") and line.endswith("]"):
                sections = line[1:-1].strip().split("::")
                container = self
                enums = self._enums
                for section in sections:
                    if not hasattr(container, section):
                        container.add_attribute(section, {})
                    container = getattr(container, section)
                    enums = enums.get(section, {})
            else: # OPTION = VALUE
                option, value = line.split("=", 1)
                option = option.strip()
                value = value.strip()
                enum = enums.get(option, None)
                try: value = json.loads(value, cls=EnumDecoder, enum=enum)
                except (AttributeError, ValueError):
                    print(("Failed to parse value '{}' of option '{}.{}' "
                           "from configuration file '{}'."
                           .format(value,
                                   "::".join(sections),
                                   option,
                                   self.path)),

                          file=sys.stderr)

                    continue
                if hasattr(container, option) and value is None:
                    # Discard a None-value for all non-extension options.
                    # None-values are not used for any options, but might
                    # accidentally bet set in some corner or error cases.
                    # By discarding them here, we ensure a clean start.
                    print ("Discarding value '{}' of option '{}.{}' "
                           "from configuration file '{}'."
                           .format(value,
                                   "::".join(sections),
                                   option,
                                   self.path),

                           file=sys.stderr)

                    continue
                if not hasattr(container, option):
                    # Add attribute if it does not exist in container, which
                    # has been initialized from config_defaults. This is needed
                    # for extensions, defaults of options of which are not
                    # known until later. Any possible obsolete non-extension
                    # options created here will be removed before writing in
                    # write_to_file.
                    container.add_attribute(option, value)
                setattr(container, option, value)

    def register_extension(self, name, defaults, enums=None):
        """
        Add section and options for extension.

        `name` should be preferrably the module name of the extension and it
        will appear in the section name as ``extensions::name``. `defaults`
        should be a dictionary of default values for options. `enums` should be
        a dictionary of :class:`aeidon.Enumeration` instances corresponding to
        enumeration items that appear in options.
        """
        self._defaults["extensions"].update({name: defaults})
        self.extensions.extend({name: aeidon.util.copy_dict(defaults)})
        self._enums["extensions"].update({name: enums or {}})

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        self.update(self._defaults)

    def write_to_file(self):
        """
        Write values of configuration options to file.

        Raise :exc:`IOError` or :exc:`OSError` if unable to create
        configuration directory or unable to write configuration file.
        Fail silently if :attr:`path` is not set.
        """
        if self.path is None: return
        self.general.version = gaupol.__version__
        if not os.path.isdir(os.path.dirname(self.path)):
            try: aeidon.util.makedirs(os.path.dirname(self.path))
            except (IOError, OSError):
                aeidon.util.print_write_io(sys.exc_info(), self.path)
                raise # IOError, OSError
        encoding = aeidon.util.get_default_encoding()
        try: fobj = open(self.path, "w", encoding=encoding)
        except (IOError, OSError):
            aeidon.util.print_write_io(sys.exc_info(), self.path)
            raise # IOError, OSError
        root = self._flatten(self._root)
        defaults = self._flatten(self._defaults)
        for section in sorted(root):
            fobj.write(os.linesep)
            fobj.write("[{}]".format(section))
            fobj.write(os.linesep)
            for option in sorted(root[section]):
                value = root[section][option]
                json_value = json.dumps(value, ensure_ascii=False)
                if (not section.startswith("extensions::") and
                    (not section in defaults or
                     not option in defaults[section])):
                    # Discard removed options, but always keep
                    # all options of all extensions.
                    continue
                if (section in defaults) and (option in defaults[section]):
                    if value == defaults[section][option]:
                        fobj.write("# ")
                try: fobj.write("{} = {}".format(option, json_value))
                except UnicodeError:
                    print(("Failed to write value '{}' of option '{}.{}' "
                           "to configuration file '{}'."
                           .format(value, section, option, self.path)),
                          file=sys.stderr)

                fobj.write(os.linesep)
