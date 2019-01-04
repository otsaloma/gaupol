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

"""
Codes, names and descriptions of character encodings.

For functions dealing with character encodings, see also :mod:`aeidon.util`.
"""

import aeidon
import codecs
import locale
import re

from aeidon.i18n import _


# Tuples of code, name and description for each supported character encoding.
# Codes are the official names used by Python. Names are mostly taken from
# IANA. Descriptions are mostly copied from gedit.

_encodings = (
    # TRANSLATORS: Most of the character encoding descriptions are copied from
    # gedit, which is translated to very many languages. Check the gedit .po
    # files for a reference: <https://gitlab.gnome.org/GNOME/gedit/tree/master/po>.
    ("ascii"          , "US-ASCII"        , _("English")),
    ("big5"           , "Big5"            , _("Chinese traditional")),
    ("big5hkscs"      , "Big5-HKSCS"      , _("Chinese traditional")),
    ("cp037"          , "IBM037"          , _("English")),
    ("cp273"          , "IBM273"          , _("German")),
    ("cp424"          , "IBM242"          , _("Hebrew")),
    ("cp437"          , "IBM437"          , _("English")),
    ("cp500"          , "IBM500"          , _("Western")),
    ("cp720"          , "IBM720"          , _("Arabic")),
    ("cp737"          , "IBM737"          , _("Greek")),
    ("cp775"          , "IBM775"          , _("Baltic")),
    ("cp850"          , "IBM850"          , _("Western")),
    ("cp852"          , "IBM852"          , _("Central European")),
    ("cp855"          , "IBM855"          , _("Cyrillic")),
    ("cp856"          , "IBM856"          , _("Hebrew")),
    ("cp857"          , "IBM857"          , _("Turkish")),
    ("cp860"          , "IBM860"          , _("Portuguese")),
    ("cp861"          , "IBM861"          , _("Icelandic")),
    ("cp862"          , "IBM862"          , _("Hebrew")),
    ("cp863"          , "IBM863"          , _("Canadian")),
    ("cp864"          , "IBM864"          , _("Arabic")),
    ("cp865"          , "IBM865"          , _("Nordic")),
    ("cp866"          , "IBM866"          , _("Russian")),
    ("cp869"          , "IBM869"          , _("Greek")),
    ("cp874"          , "IBM874"          , _("Thai")),
    ("cp875"          , "IBM875"          , _("Greek")),
    ("cp932"          , "IBM932"          , _("Japanese")),
    ("cp949"          , "IBM949"          , _("Korean")),
    ("cp950"          , "IBM950"          , _("Chinese traditional")),
    ("cp1006"         , "IBM1006"         , _("Urdu")),
    ("cp1026"         , "IBM1026"         , _("Turkish")),
    ("cp1125"         , "IBM1125"         , _("Ukrainian")),
    ("cp1140"         , "IBM1140"         , _("Western")),
    ("cp1250"         , "windows-1250"    , _("Central European")),
    ("cp1251"         , "windows-1251"    , _("Cyrillic")),
    ("cp1252"         , "windows-1252"    , _("Western")),
    ("cp1253"         , "windows-1253"    , _("Greek")),
    ("cp1254"         , "windows-1254"    , _("Turkish")),
    ("cp1255"         , "windows-1255"    , _("Hebrew")),
    ("cp1256"         , "windows-1256"    , _("Arabic")),
    ("cp1257"         , "windows-1257"    , _("Baltic")),
    ("cp1258"         , "windows-1258"    , _("Vietnamese")),
    ("euc_jp"         , "EUC-JP"          , _("Japanese")),
    ("euc_jis_2004"   , "EUC-JIS-2004"    , _("Japanese")),
    ("euc_jisx0213"   , "EUC-JISX0213"    , _("Japanese")),
    ("euc_kr"         , "EUC-KR"          , _("Korean")),
    ("gb2312"         , "GB2312"          , _("Chinese simplified")),
    ("gbk"            , "GBK"             , _("Chinese unified")),
    ("gb18030"        , "GB18030"         , _("Chinese unified")),
    ("hz"             , "HZ"              , _("Chinese simplified")),
    ("iso2022_jp"     , "ISO-2022-JP"     , _("Japanese")),
    ("iso2022_jp_1"   , "ISO-2022-JP-1"   , _("Japanese")),
    ("iso2022_jp_2"   , "ISO-2022-JP-2"   , _("Japanese")),
    ("iso2022_jp_2004", "ISO-2022-JP-2004", _("Japanese")),
    ("iso2022_jp_3"   , "ISO-2022-JP-3"   , _("Japanese")),
    ("iso2022_jp_ext" , "ISO-2022-JP-EXT" , _("Japanese")),
    ("iso2022_kr"     , "ISO-2022-KR"     , _("Korean")),
    ("latin_1"        , "ISO-8859-1"      , _("Western")),
    ("iso8859_2"      , "ISO-8859-2"      , _("Central European")),
    ("iso8859_3"      , "ISO-8859-3"      , _("South European")),
    ("iso8859_4"      , "ISO-8859-4"      , _("Baltic")),
    ("iso8859_5"      , "ISO-8859-5"      , _("Cyrillic")),
    ("iso8859_6"      , "ISO-8859-6"      , _("Arabic")),
    ("iso8859_7"      , "ISO-8859-7"      , _("Greek")),
    ("iso8859_8"      , "ISO-8859-8"      , _("Hebrew")),
    ("iso8859_9"      , "ISO-8859-9"      , _("Turkish")),
    ("iso8859_10"     , "ISO-8859-10"     , _("Nordic")),
    ("iso8859_13"     , "ISO-8859-13"     , _("Baltic")),
    ("iso8859_14"     , "ISO-8859-14"     , _("Celtic")),
    ("iso8859_15"     , "ISO-8859-15"     , _("Western")),
    ("johab"          , "Johab"           , _("Korean")),
    ("koi8_r"         , "KOI8-R"          , _("Russian")),
    ("koi8_t"         , "KOI8-T"          , _("Tajik")),
    ("koi8_u"         , "KOI8-U"          , _("Ukrainian")),
    ("kz1048"         , "KZ1048"          , _("Kazakh")),
    ("mac_cyrillic"   , "MacCyrillic"     , _("Cyrillic")),
    ("mac_greek"      , "MacGreek"        , _("Greek")),
    ("mac_iceland"    , "MacIceland"      , _("Icelandic")),
    ("mac_latin2"     , "MacCentralEurope", _("Central European")),
    ("mac_roman"      , "MacRoman"        , _("Western")),
    ("mac_turkish"    , "MacTurkish"      , _("Turkish")),
    ("ptcp154"        , "PTCP154"         , _("Cyrillic Asian")),
    ("shift_jis"      , "Shift_JIS"       , _("Japanese")),
    ("shift_jis_2004" , "Shift_JIS-2004"  , _("Japanese")),
    ("shift_jisx0213" , "Shift_JISX0213"  , _("Japanese")),
    ("utf_32"         , "UTF-32"          , _("Unicode")),
    ("utf_32_be"      , "UTF-32BE"        , _("Unicode")),
    ("utf_32_le"      , "UTF-32LE"        , _("Unicode")),
    ("utf_16"         , "UTF-16"          , _("Unicode")),
    ("utf_16_be"      , "UTF-16BE"        , _("Unicode")),
    ("utf_16_le"      , "UTF-16LE"        , _("Unicode")),
    ("utf_7"          , "UTF-7"           , _("Unicode")),
    ("utf_8"          , "UTF-8"           , _("Unicode")),
    ("utf_8_sig"      , "UTF-8-SIG"       , _("Unicode")),)

CODE, NAME, DESC = range(3)

# Illegal characters in encoding codes.
_re_illegal = re.compile(r"[^a-z0-9_]")


def code_to_description(code):
    """Convert encoding `code` to localized description."""
    for item in _encodings:
        if item[CODE] == code:
            return item[DESC]
    raise ValueError("Code {!r} not found"
                     .format(code))

def code_to_long_name(code):
    """Convert encoding `code` to localized long name."""
    for item in _encodings:
        if item[CODE] == code:
            return (_("{description} ({name})")
                    .format(name=item[NAME],
                            description=item[DESC]))

    raise ValueError("Code {!r} not found"
                     .format(code))

def code_to_name(code):
    """Convert encoding `code` to name."""
    for item in _encodings:
        if item[CODE] == code:
            return item[NAME]
    raise ValueError("Code {!r} not found"
                     .format(code))

def detect(path):
    """
    Detect the encoding of file at `path` and return code or ``None``.

    Raise :exc:`IOError` if reading fails.
    """
    bom_encoding = detect_bom(path)
    if bom_encoding is not None:
        return bom_encoding
    from chardet import universaldetector
    detector = universaldetector.UniversalDetector()
    with open(path, "rb") as f:
        detector.reset()
        for line in f:
            detector.feed(line)
            if detector.done: break
    detector.close()
    code = detector.result["encoding"]
    if code is None: return None
    try:
        # chardet returns what seem to be IANA names. They need to be
        # translated to their Python equivalents. Some of the encodings
        # returned by chardet are not supported by Python.
        return translate_code(code)
    except ValueError:
        return None

def detect_bom(path):
    """Return corresponding encoding if BOM found, else ``None``."""
    with open(path, "rb") as f:
        line = f.readline()
    if (line.startswith(codecs.BOM_UTF32_BE) and
        is_valid_code("utf_32_be")):
        return "utf_32_be"
    if (line.startswith(codecs.BOM_UTF32_LE) and
        is_valid_code("utf_32_le")):
        return "utf_32_le"
    if (line.startswith(codecs.BOM_UTF8) and
        is_valid_code("utf_8_sig")):
        return "utf_8_sig"
    if (line.startswith(codecs.BOM_UTF16_BE) and
        is_valid_code("utf_16_be")):
        return "utf_16_be"
    if (line.startswith(codecs.BOM_UTF16_LE) and
        is_valid_code("utf_16_le")):
        return "utf_16_le"
    return None

@aeidon.deco.once
def get_locale_code():
    """Return code of the locale encoding or ``None``."""
    code = locale.getpreferredencoding()
    if code is None: return None
    code = _re_illegal.sub("_", code.lower())
    code = aeidon.util.get_encoding_alias(code)
    return code

@aeidon.deco.once
def get_locale_long_name():
    """Return localized long name for locale encoding."""
    name = code_to_name(get_locale_code())
    return _("Current locale ({})").format(name)

@aeidon.deco.once
def get_valid():
    """Return a list of code, name, description of valid encodings."""
    valid_encodings = []
    for i, item in enumerate(_encodings):
        if is_valid_code(item[CODE]):
            valid_encodings.append(item)
    return valid_encodings

def is_valid_code(code):
    """Return ``True`` if encoding `code` is valid."""
    try:
        codecs.lookup(code)
        return True
    except LookupError:
        return False

def name_to_code(name):
    """Convert encoding `name` to code."""
    for item in _encodings:
        if item[NAME] == name:
            return item[CODE]
    raise ValueError("Name {!r} not found"
                     .format(name))

def translate_code(code):
    """Return normalized encoding `code`."""
    code = _re_illegal.sub("_", code.lower())
    code = aeidon.util.get_encoding_alias(code)
    for item in _encodings:
        if item[CODE] == code:
            return item[CODE]
    raise ValueError("Code {!r} not found"
                     .format(code))
