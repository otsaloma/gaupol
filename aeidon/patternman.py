# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Managing regular expression substitutions for subtitle texts."""

import aeidon
import os
import re
import xml.etree.ElementTree as ET

__all__ = ("PatternManager",)


class PatternManager:

    """
    Managing regular expression substitutions for subtitle texts.

    :ivar _patterns: Dictionary mapping codes to pattern lists
    :ivar pattern_type: String to indentify what the pattern matches

    :attr:`pattern_type` should be a string with value "line-break",
    "common-error", "capitalization" or "hearing-impaired". Codes are of form
    ``Script[-language-[COUNTRY]]`` using the corresponding ISO codes.
    """
    _re_comment = re.compile(r"^\s*#.*$")

    def __init__(self, pattern_type):
        """Initialize a :class:`PatternManager` instance."""
        self.pattern_type = pattern_type
        self._patterns = {}
        self._read_patterns()

    def _filter_patterns(self, patterns):
        """
        Return `patterns` with name-clashes resolved.

        Patterns with a more specific code replace those with a less specific
        code if they have the same name and the more specific pattern's policy
        is explicitly set to ``Replace`` (instead of the implicit ``Append``).
        Order is maintained so that all patterns with the same name are always
        located in the position of the earliest of such patterns.
        """
        filtered_patterns = []
        for pattern in patterns:
            name = pattern.get_name(False)
            policy = pattern.get_field("Policy")
            last_index = len(filtered_patterns) - 1
            for j, filtered_pattern in enumerate(filtered_patterns):
                if filtered_pattern.get_name() == name:
                    last_index = j
                    if policy == "Replace":
                        filtered_patterns[j] = None
            filtered_patterns.insert(last_index + 1, pattern)
            while None in filtered_patterns:
                filtered_patterns.remove(None)
        return filtered_patterns

    def _get_codes(self, script=None, language=None, country=None):
        """Return a sequence of all codes to be used by arguments."""
        codes = ["Zyyy"]
        if not None in (script,):
            codes.append(script)
        if not None in (script, language):
            codes.append("{}-{}".format(script, language))
        if not None in (script, language, country):
            codes.append("{}-{}-{}".format(script, language, country))
        return tuple(codes)

    def get_countries(self, script, language):
        """Return a sequence of countries for which patterns exist."""
        codes = list(self._patterns.keys())
        start = "{}-{}-".format(script, language)
        codes = [x for x in codes if x.startswith(start)]
        countries = [x.split("-")[2] for x in codes]
        return tuple(aeidon.util.get_unique(countries))

    def get_languages(self, script):
        """Return a sequence of languages for which patterns exist."""
        codes = list(self._patterns.keys())
        start = "{}-".format(script)
        codes = [x for x in codes if x.startswith(start)]
        languages = [x.split("-")[1] for x in codes]
        return tuple(aeidon.util.get_unique(languages))

    def get_patterns(self, script=None, language=None, country=None):
        """Return patterns for `script`, `language` and `country`."""
        patterns = []
        codes = self._get_codes(script, language, country)
        for code in codes:
            for pattern in self._patterns.get(code, []):
                # Skip patterns that define exceptions to their use
                # that match a more speficic group being requested.
                skip = pattern.get_field_list("SkipIn", [])
                if set(skip) & set(codes): continue
                patterns.append(pattern)
        return self._filter_patterns(patterns)

    def get_scripts(self):
        """Return a sequence of scripts for which patterns exist."""
        codes = list(self._patterns.keys())
        while "Zyyy" in codes:
            codes.remove("Zyyy")
        scripts = [x.split("-")[0] for x in codes]
        return tuple(aeidon.util.get_unique(scripts))

    def _read_config_from_directory(self, directory, encoding):
        """Read configurations from files in `directory`."""
        if not os.path.isdir(directory): return
        extension = ".{}.conf".format(self.pattern_type)
        files = os.listdir(directory)
        for name in (x for x in files if x.endswith(extension)):
            path = os.path.join(directory, name)
            self._read_config_from_file(path, encoding)

    def _read_config_from_file(self, path, encoding):
        """Read configurations from file at `path`."""
        if not os.path.isfile(path): return
        basename = os.path.basename(path)
        extension = ".{}.conf".format(self.pattern_type)
        code = basename.replace(extension, "")
        if not code in self._patterns: return
        patterns = self._patterns[code]
        for element in ET.parse(path).findall("pattern"):
            name = element.get("name")
            name = name.replace("&quot;", '"')
            name = name.replace("&amp;", "&")
            enabled = (element.get("enabled") == "true")
            for pattern in patterns:
                if pattern.get_name(localize=False) == name:
                    pattern.enabled = enabled

    def _read_patterns(self):
        """Read all patterns of :attr:`pattern_type` from files."""
        data_dir = os.path.join(aeidon.DATA_DIR, "patterns")
        data_home_dir = os.path.join(aeidon.DATA_HOME_DIR, "patterns")
        config_home_dir = os.path.join(aeidon.CONFIG_HOME_DIR, "patterns")
        encoding = aeidon.util.get_default_encoding()
        self._read_patterns_from_directory(data_dir, "utf_8")
        self._read_patterns_from_directory(data_home_dir, encoding)
        self._read_config_from_directory(data_dir, "utf_8")
        self._read_config_from_directory(config_home_dir, encoding)

    def _read_patterns_from_directory(self, directory, encoding):
        """Read all patterns from files in `directory`."""
        if not os.path.isdir(directory): return
        extension = ".{}".format(self.pattern_type)
        extensions = (extension, "{}.in".format(extension))
        files = [x for x in os.listdir(directory)
                 if x.endswith(extensions)]

        for name in [x for x in files if x.endswith(".in")]:
            # If both untranslated and translated pattern files are found,
            # load patterns only from the translated one.
            if name[:-3] in files:
                files.remove(name)
        for name in files:
            path = os.path.join(directory, name)
            self._read_patterns_from_file(path, encoding)

    def _read_patterns_from_file(self, path, encoding):
        """Read all patterns from file at `path`."""
        if not os.path.isfile(path): return
        basename = os.path.basename(path)
        extension = ".{}".format(self.pattern_type)
        if basename.endswith(".in"):
            extension = ".{}.in".format(self.pattern_type)
        code = basename.replace(extension, "")
        local = path.startswith(aeidon.DATA_HOME_DIR)
        patterns = self._patterns.setdefault(code, [])
        lines = aeidon.util.readlines(path, encoding)
        lines = [self._re_comment.sub("", x) for x in lines]
        lines = [x.strip() for x in lines]
        for line in (x for x in lines if x):
            if line.startswith("["): # [HEADER]
                patterns.append(aeidon.Pattern())
                patterns[-1].local = local
            else: # [_]KEY=VALUE
                name, value = line.split("=", 1)
                # Translatable fields used to be marked with a leading
                # underscore prior to version 1.3. We continue to support that
                # syntax in case users have local pattern files.
                name = name[1:] if name.startswith("_") else name
                # Regular expression patterns and replacements use null
                # character to avoid syntax issues that go against the GKeyFile
                # spec and would be "fixed" by msgfmt when merging translations.
                # https://github.com/otsaloma/gaupol/issues/70
                value = re.sub(r"\\0(?!\d)", "", value)
                patterns[-1].set_field(name, value)

    def save_config(self, script=None, language=None, country=None):
        """Save pattern configurations to files."""
        codes = self._get_codes(script, language, country)
        for code in (x for x in codes if x in self._patterns):
            self._write_config_to_file(code, "utf_8")

    def _write_config_to_file(self, code, encoding):
        """Write configurations of all patterns to file."""
        local_dir = os.path.join(aeidon.CONFIG_HOME_DIR, "patterns")
        basename = "{}.{}.conf".format(code, self.pattern_type)
        path = os.path.join(local_dir, basename)
        lines = ['<?xml version="1.0" encoding="utf-8"?>']
        lines.append('<patterns>')
        written_names = set()
        for pattern in self._patterns[code]:
            name = pattern.get_name(localize=False)
            if name in written_names: continue
            written_names.add(name)
            name = name.replace("&", "&amp;")
            name = name.replace('"', "&quot;")
            enabled = "true" if pattern.enabled else "false"
            lines.append('  <pattern name="{}" enabled="{}"/>'
                         .format(name, enabled))

        lines.append('</patterns>')
        aeidon.util.writelines(path, lines, encoding)
