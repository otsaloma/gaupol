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

import gaupol
import os
import xml.etree.ElementTree as ET

__all__ = ["PatternManager"]


class PatternManager(object):

    """Manager of Regular expression based corrections to subtitle texts.

    Instance variables:
     * pattern_type: String to indentify what the pattern matches
     * _patterns: Dictionary mapping codes to pattern lists

    pattern_type should be a string with value 'line-break', 'common-error',
    'capitalization' or 'hearing-impaired'. Codes are of form
    Script[-language-[COUNTRY]] using the corresponding ISO codes.
    """

    __metaclass__ = gaupol.Contractual

    def __init___require(self, pattern_type):
        types = ("line-break", "common-error",
            "capitalization", "hearing-impaired")
        assert pattern_type in types

    def __init__(self, pattern_type):

        self.pattern_type = pattern_type
        self._patterns = {}
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

    def _get_codes_require(self, script=None, language=None, country=None):
        self._assert_indentifiers(script, language, country)

    def _get_codes(self, script=None, language=None, country=None):
        """Get a list of all codes to be used by arguments.

        Zyyy is the first code and the most specific one last.
        """
        codes = ["Zyyy"]
        if script is not None:
            codes.append(script)
        if language is not None:
            code = "%s-%s" % (script, language)
            codes.append(code)
        if country is not None:
            code = "%s-%s" % (code, country)
            codes.append(code)
        return codes

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
        code = basename.replace(extension, "")
        assert code in self._patterns
        patterns = self._patterns[code]
        for element in ET.parse(path).findall("pattern"):
            name = unicode(element.get("name"))
            name = name.replace("&quot;", '"')
            name = name.replace("&amp;", "&")
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
        code = basename.replace(extension, "")
        local = path.startswith(gaupol.PROFILE_DIR)
        patterns = self._patterns.setdefault(code, [])
        lines = gaupol.util.readlines(path, encoding)
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
    def _write_config_to_file(self, code, encoding):
        """Write configurations of all patterns to file."""

        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        assert os.path.isdir(local_dir)
        basename = "%s.%s.conf" % (code, self.pattern_type)
        path = os.path.join(local_dir, basename)
        text = '<?xml version="1.0" encoding="utf-8"?>'
        text += '%s<patterns>%s' % (os.linesep, os.linesep)
        for pattern in self._patterns[code]:
            name = pattern.get_name(False)
            name = name.replace("&", "&amp;")
            name = name.replace('"', "&quot;")
            enabled = ("false", "true")[pattern.enabled]
            text += '  <pattern name="%s" ' % name
            text += 'enabled="%s"/>' % enabled
            text += os.linesep
        text += "</patterns>%s" % os.linesep
        gaupol.util.write(path, text, encoding)

    @gaupol.util.asserted_return
    def _write_patterns_to_file(self, code, encoding):
        """Write all local pattern to file."""

        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        assert os.path.isdir(local_dir)
        basename = "%s.%s" % (code, self.pattern_type)
        path = os.path.join(local_dir, basename)
        pattern_texts = []
        for pattern in (x for x in self._patterns[code] if x.local):
            pattern_texts.append(self._get_pattern_text(pattern))
        blank_line = os.linesep + os.linesep
        text = blank_line.join(pattern_texts) + os.linesep
        gaupol.util.write(path, text, encoding)

    def get_countries(self, script, language):
        """Get a list of countries for which patterns exist."""

        codes = self._patterns.keys()
        start = "%s-%s-" % (script, language)
        codes = [x for x in codes if x.startswith(start)]
        countries = [x.split("-")[2] for x in codes]
        return gaupol.util.get_unique(countries)

    def get_languages(self, script):
        """Get a list of languages for which patterns exist."""

        codes = self._patterns.keys()
        start = "%s-" % script
        codes = [x for x in codes if x.startswith(start)]
        languages = [x.split("-")[1] for x in codes]
        return gaupol.util.get_unique(languages)

    def get_patterns_require(self, script=None, language=None, country=None):
        self._assert_indentifiers(script, language, country)

    def get_patterns(self, script=None, language=None, country=None):
        """Get patterns for script, language and country."""

        patterns = []
        for code in self._get_codes(script, language, country):
            for pattern in self._patterns.get(code, []):
                name = pattern.get_name(False)
                for i in range(len(patterns)):
                    # Allow patterns with a more specific code to override
                    # those with a less specific code if the names clash.
                    if patterns[i].get_name(False) == name:
                        patterns.pop(i)
                patterns.append(pattern)
        return patterns

    def get_scripts(self):
        """Get a list of scripts for which patterns exist."""

        codes = self._patterns.keys()
        while "Zyyy" in codes:
            codes.remove("Zyyy")
        scripts = [x.split("-")[0] for x in codes]
        return gaupol.util.get_unique(scripts)

    def save_require(self, script=None, language=None, country=None):
        self._assert_indentifiers(script, language, country)

    def save(self, script=None, language=None, country=None):
        """Save local patterns and configurations to files."""

        local_dir = os.path.join(gaupol.PROFILE_DIR, "patterns")
        gaupol.util.silent(OSError)(gaupol.util.makedirs)(local_dir)
        encoding = gaupol.util.get_default_encoding()
        codes = self._get_codes(script, language, country)
        for code in (x for x in codes if x in self._patterns):
            # TODO: Uncomment when patterns can be added by a method.
            # self._write_patterns_to_file(code, encoding)
            self._write_config_to_file(code, "utf_8")
