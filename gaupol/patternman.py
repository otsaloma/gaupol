# Copyright (C) 2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Manager of Regular expression based corrections to subtitle texts."""

from __future__ import with_statement

import codecs
import contextlib
import gaupol
import os
import xml.etree.ElementTree as ET

__all__ = ["PatternManager"]


class PatternManager(object):

    """Manager of Regular expression based corrections to subtitle texts.

    Instance variables:
     * pattern_type: String to indentify what the pattern matches
     * _country_patterns: Dictionary mapping country codes to pattern lists
     * _language_patterns: Dictionary mapping language codes to pattern lists
     * _script_patterns: Dictionary mapping script codes to pattern lists

    pattern_type should be a string with value 'line-break', 'error',
    'capitalization' or 'hearing-impaired'.
    """

    __metaclass__ = gaupol.Contractual

    def __init___require(self, pattern_type):
        types = ("line-break", "error", "capitalization", "hearing-impaired")
        assert pattern_type in types

    def __init__(self, pattern_type):

        self.pattern_type = pattern_type
        self._country_patterns = {}
        self._language_patterns = {}
        self._script_patterns = {}

        self._country_patterns[None] = []
        self._language_patterns[None] = []
        self._script_patterns[None] = []
        self._script_patterns["Zyyy"] = []
        self._read_patterns()

    def _assert_indentifiers(self, script, language, country):
        """Assert that codes are valid and parents are defined."""

        if script is not None:
            assert script in gaupol.scripts.scripts
        if language is not None:
            assert script is not None
            assert language in gaupol.languages.languages
        if country is not None:
            assert language is not None
            assert country in gaupol.countries.countries

    def _get_dictionary(self, name):
        """Return destination dictionary and key for name."""

        identifiers = name.split("-")
        key = identifiers[-1]
        if len(identifiers) == 1:
            return self._script_patterns, key
        if len(identifiers) == 2:
            return self._language_patterns, key
        if len(identifiers) == 3:
            return self._country_patterns, key
        raise ValueError

    def _get_pattern_text(self, pattern):
        """Get text representation of pattern to write to file."""

        words = ("%s-pattern" % self.pattern_type).split("-")
        words = [x.capitalize() for x in words]
        text = "[%s]%s" % ("".join(words), os.linesep)
        for key, value in pattern.fields.items():
            text += "%s=%s%s" % (key, value, os.linesep)
        return text.strip()

    def _read_config_from_directory_require(self, directory, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    @gaupol.util.asserted_return
    def _read_config_from_directory(self, directory, encoding):
        """Read configurations from files in directory."""

        assert os.path.isdir(directory)
        extension = ".%s.conf" % self.pattern_type
        common_file = os.path.join(directory, "Zyyy%s" % extension)
        self._read_config_from_file(common_file, encoding)
        files = os.listdir(directory)
        for name in (x for x in files if x.endswith(extension)):
            path = os.path.join(directory, name)
            self._read_config_from_file(path, encoding)

    def _read_config_from_file_require(self, path, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    @gaupol.util.asserted_return
    def _read_config_from_file(self, path, encoding):
        """Read configurations from file."""

        assert os.path.isfile(path)
        basename = os.path.basename(path)
        extension = ".%s.conf" % self.pattern_type
        name = basename.replace(extension, "")
        dictionary, key = self._get_dictionary(name)
        assert key in dictionary
        patterns = dictionary[key]
        for element in ET.parse(path).findall("pattern"):
            name = unicode(element.get("name"))
            enabled = (element.get("enabled") == "true")
            for pattern in patterns:
                if pattern.get_name(False) == name:
                    pattern.enabled = enabled

    def _read_patterns(self):
        """Read all patterns of self.pattern_type from files."""

        global_dir = os.path.join(gaupol.DATA_DIR, "patterns")
        self._read_patterns_from_directory(global_dir, "utf_8")
        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        encoding = gaupol.util.get_default_encoding()
        self._read_patterns_from_directory(local_dir, encoding)
        self._read_config_from_directory(global_dir, "utf_8")
        self._read_config_from_directory(local_dir, encoding)

    def _read_patterns_from_directory_require(self, directory, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    @gaupol.util.asserted_return
    def _read_patterns_from_directory(self, directory, encoding):
        """Read all patterns from files in directory."""

        assert os.path.isdir(directory)
        extension = ".%s" % self.pattern_type
        extensions = (extension, "%s.in" % extension)
        common_file = os.path.join(directory, "Zyyy%s" % extension)
        self._read_patterns_from_file(common_file, encoding)
        files = os.listdir(directory)
        for name in (x for x in files if x.endswith(extensions)):
            path = os.path.join(directory, name)
            self._read_patterns_from_file(path, encoding)

    def _read_patterns_from_file_require(self, directory, encoding):
        assert gaupol.encodings.is_valid_code(encoding)

    @gaupol.util.asserted_return
    def _read_patterns_from_file(self, path, encoding):
        """Read all patterns from file."""

        assert os.path.isfile(path)
        basename = os.path.basename(path)
        extension = ".%s" % self.pattern_type
        if basename.endswith(".in"):
            extension = ".%s.in" % self.pattern_type
        name = basename.replace(extension, "")
        local = path.startswith(gaupol.PROFILE_DIR)
        dictionary, key = self._get_dictionary(name)
        patterns = dictionary.setdefault(key, [])
        args = (path, "r", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            lines = fobj.readlines()
        lines = [x.strip() for x in lines]
        for line in (x for x in lines if x):
            if line.startswith("["):
                patterns.append(gaupol.Pattern())
                patterns[-1].local = local
                continue
            name, value = unicode(line).split("=", 1)
            name = (name[1:] if name.startswith("_") else name)
            patterns[-1].set_field(name, value)

    @gaupol.util.asserted_return
    def _write_config_to_file(self, name, encoding, patterns):
        """Write configurations of all patterns to file."""

        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        assert os.path.isdir(local_dir)
        basename = "%s.%s.conf" % (name, self.pattern_type)
        path = os.path.join(local_dir, basename)
        args = (path, "w", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            fobj.write('<?xml version="1.0" encoding="utf-8"?>')
            fobj.write('%s<patterns>%s' % (os.linesep, os.linesep))
            for pattern in patterns:
                name = pattern.get_name(False)
                enabled = ("false", "true")[pattern.enabled]
                fobj.write('  <pattern name="%s" ' % name)
                fobj.write('enabled="%s" />' % enabled)
                fobj.write(os.linesep)
            fobj.write("</patterns>%s" % (os.linesep))

    @gaupol.util.asserted_return
    def _write_patterns_to_file(self, name, encoding, patterns):
        """Write all local pattern to file."""

        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        assert os.path.isdir(local_dir)
        basename = "%s.%s" % (name, self.pattern_type)
        path = os.path.join(local_dir, basename)
        pattern_texts = []
        for pattern in (x for x in patterns if x.local):
            pattern_texts.append(self._get_pattern_text(pattern))
        args = (path, "w", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            blank_line = os.linesep + os.linesep
            fobj.write(blank_line.join(pattern_texts) + os.linesep)

    def get_patterns_require(self, script=None, language=None, country=None):
        self._assert_indentifiers(script, language, country)

    def get_patterns(self, script=None, language=None, country=None):
        """Get patterns for script, language and country."""

        patterns = self._script_patterns["Zyyy"][:]
        patterns += self._script_patterns[script]
        patterns += self._language_patterns[language]
        patterns += self._country_patterns[country]
        return patterns

    def save_require(self, script=None, language=None, country=None):
        self._assert_indentifiers(script, language, country)

    def save(self, script=None, language=None, country=None):
        """Save local patterns and configurations to files."""

        patterns = self.get_patterns(script, language, country)
        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        gaupol.util.silent(OSError)(gaupol.util.makedirs)(local_dir)
        name = "%s-%s-%s" % (script, language, country)
        name = name.replace("-None", "")
        encoding = gaupol.util.get_default_encoding()
        self._write_patterns_to_file(name, encoding, patterns)
        self._write_config_to_file(name, "utf_8", patterns)
