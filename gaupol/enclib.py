# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Encodings and encoding names.

Module variables:

    _encodings:  Tuple of tuples of python name, display name, description
    _re_illegal: Regular expression for illegal characters in encoding names
"""

# Python names are the official names used by Python [1]. Display names are
# mostly taken from IANA [2]. Descriptions are mostly copied from Gedit [3].
#
# [1] http://docs.python.org/dev/lib/standard-encodings.html
# [2] http://www.iana.org/assignments/character-sets
# [3] http://svn.gnome.org/viewcvs/gedit/trunk/gedit/gedit-encodings.c


from __future__ import with_statement

import codecs
import locale
import re

from gaupol import util
from gaupol.i18n import _


_encodings = (
    # Translators: Most of the character encoding descriptions are copied from
    # Gedit, which is translated to very many languages. Check the Gedit .po
    # files for a reference: http://svn.gnome.org/viewcvs/gedit/trunk/po/.
    ("ascii"          , "US-ASCII"        , _("English")            ),
    ("big5"           , "Big5"            , _("Chinese traditional")),
    ("big5hkscs"      , "Big5-HKSCS"      , _("Chinese traditional")),
    ("cp037"          , "IBM037"          , _("English")            ),
    ("cp424"          , "IBM242"          , _("Hebrew")             ),
    ("cp437"          , "IBM437"          , _("English")            ),
    ("cp500"          , "IBM500"          , _("Western")            ),
    ("cp737"          , "IBM737"          , _("Greek")              ),
    ("cp775"          , "IBM775"          , _("Baltic")             ),
    ("cp850"          , "IBM850"          , _("Western")            ),
    ("cp852"          , "IBM852"          , _("Central European")   ),
    ("cp855"          , "IBM855"          , _("Cyrillic")           ),
    ("cp856"          , "IBM856"          , _("Hebrew")             ),
    ("cp857"          , "IBM857"          , _("Turkish")            ),
    ("cp860"          , "IBM860"          , _("Portugese")          ),
    ("cp861"          , "IBM861"          , _("Icelandic")          ),
    ("cp862"          , "IBM862"          , _("Hebrew")             ),
    ("cp863"          , "IBM863"          , _("Canadian")           ),
    ("cp864"          , "IBM864"          , _("Arabic")             ),
    ("cp865"          , "IBM865"          , _("Nordic")             ),
    ("cp866"          , "IBM866"          , _("Russian")            ),
    ("cp869"          , "IBM869"          , _("Greek")              ),
    ("cp874"          , "IBM874"          , _("Thai")               ),
    ("cp875"          , "IBM875"          , _("Greek")              ),
    ("cp932"          , "IBM932"          , _("Japanese")           ),
    ("cp949"          , "IBM949"          , _("Korean")             ),
    ("cp950"          , "IBM950"          , _("Chinese traditional")),
    ("cp1006"         , "IBM1006"         , _("Urdu")               ),
    ("cp1026"         , "IBM1026"         , _("Turkish")            ),
    ("cp1140"         , "IBM1140"         , _("Western")            ),
    ("cp1250"         , "windows-1250"    , _("Central European")   ),
    ("cp1251"         , "windows-1251"    , _("Cyrillic")           ),
    ("cp1252"         , "windows-1252"    , _("Western")            ),
    ("cp1253"         , "windows-1253"    , _("Greek")              ),
    ("cp1254"         , "windows-1254"    , _("Turkish")            ),
    ("cp1255"         , "windows-1255"    , _("Hebrew")             ),
    ("cp1256"         , "windows-1256"    , _("Arabic")             ),
    ("cp1257"         , "windows-1257"    , _("Baltic")             ),
    ("cp1258"         , "windows-1258"    , _("Vietnamese")         ),
    ("euc_jp"         , "EUC-JP"          , _("Japanese")           ),
    ("euc_jis_2004"   , "EUC-JIS-2004"    , _("Japanese")           ),
    ("euc_jisx0213"   , "EUC-JISX0213"    , _("Japanese")           ),
    ("euc_kr"         , "EUC-KR"          , _("Korean")             ),
    ("gb2312"         , "GB2312"          , _("Chinese simplified") ),
    ("gbk"            , "GBK"             , _("Chinese unified")    ),
    ("gb18030"        , "GB18030"         , _("Chinese unified")    ),
    ("hz"             , "HZ"              , _("Chinese simplified") ),
    ("iso2022_jp"     , "ISO-2022-JP"     , _("Japanese")           ),
    ("iso2022_jp_1"   , "ISO-2022-JP-1"   , _("Japanese")           ),
    ("iso2022_jp_2"   , "ISO-2022-JP-2"   , _("Japanese")           ),
    ("iso2022_jp_2004", "ISO-2022-JP-2004", _("Japanese")           ),
    ("iso2022_jp_3"   , "ISO-2022-JP-3"   , _("Japanese")           ),
    ("iso2022_jp_ext" , "ISO-2022-JP-EXT" , _("Japanese")           ),
    ("iso2022_kr"     , "ISO-2022-KR"     , _("Korean")             ),
    ("latin_1"        , "ISO-8859-1"      , _("Western")            ),
    ("iso8859_2"      , "ISO-8859-2"      , _("Central European")   ),
    ("iso8859_3"      , "ISO-8859-3"      , _("South European")     ),
    ("iso8859_4"      , "ISO-8859-4"      , _("Baltic")             ),
    ("iso8859_5"      , "ISO-8859-5"      , _("Cyrillic")           ),
    ("iso8859_6"      , "ISO-8859-6"      , _("Arabic")             ),
    ("iso8859_7"      , "ISO-8859-7"      , _("Greek")              ),
    ("iso8859_8"      , "ISO-8859-8"      , _("Hebrew")             ),
    ("iso8859_9"      , "ISO-8859-9"      , _("Turkish")            ),
    ("iso8859_10"     , "ISO-8859-10"     , _("Nordic")             ),
    ("iso8859_13"     , "ISO-8859-13"     , _("Baltic")             ),
    ("iso8859_14"     , "ISO-8859-14"     , _("Celtic")             ),
    ("iso8859_15"     , "ISO-8859-15"     , _("Western")            ),
    ("johab"          , "Johab"           , _("Korean")             ),
    ("koi8_r"         , "KOI8-R"          , _("Russian")            ),
    ("koi8_u"         , "KOI8-U"          , _("Ukrainian")          ),
    ("mac_cyrillic"   , "MacCyrillic"     , _("Cyrillic")           ),
    ("mac_greek"      , "MacGreek"        , _("Greek")              ),
    ("mac_iceland"    , "MacIceland"      , _("Icelandic")          ),
    ("mac_latin2"     , "MacCentralEurope", _("Central European")   ),
    ("mac_roman"      , "MacRoman"        , _("Western")            ),
    ("mac_turkish"    , "MacTurkish"      , _("Turkish")            ),
    ("ptcp154"        , "PTCP154"         , _("Cyrillic Asian")     ),
    ("shift_jis"      , "Shift_JIS"       , _("Japanese")           ),
    ("shift_jis_2004" , "Shift_JIS-2004"  , _("Japanese")           ),
    ("shift_jisx0213" , "Shift_JISX0213"  , _("Japanese")           ),
    ("utf_16"         , "UTF-16"          , _("Unicode")            ),
    ("utf_16_be"      , "UTF-16BE"        , _("Unicode")            ),
    ("utf_16_le"      , "UTF-16LE"        , _("Unicode")            ),
    ("utf_7"          , "UTF-7"           , _("Unicode")            ),
    ("utf_8"          , "UTF-8"           , _("Unicode")            ),)

_re_illegal = re.compile(r"[^a-z0-9_]")


def _translate_ensure(value, name):
    assert is_valid(value)

@util.contractual
def _translate(name):
    """Translate weird encoding name.

    Raise ValueError if not found.
    Return python name.
    """
    from encodings.aliases import aliases
    name = _re_illegal.sub("_", name.lower())
    if name in aliases:
        name = aliases[name]
    for seq in _encodings:
        if seq[0] == name:
            return seq[0]
    raise ValueError

def _detect_ensure(value, path):
    assert is_valid(value)

@util.contractual
def detect(path):
    """Detect the character encoding in file.

    Raise IOError if reading fails.
    Raise ValueError if not found.
    Return python name.
    """
    from chardet import universaldetector
    detector = universaldetector.UniversalDetector()
    with open(path, "r") as fobj:
        for line in fobj:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    encoding = detector.result["encoding"]
    if encoding is None:
        raise ValueError
    return _translate(encoding)

def get_display_name(python_name):
    """Get the display name for encoding.

    Raise ValueError if not found.
    """
    for seq in _encodings:
        if seq[0] == python_name:
            return seq[1]
    raise ValueError

def get_locale_long_name_require():
    assert get_locale_python_name() is not None

@util.once
@util.contractual
def get_locale_long_name():
    """Get the long name for locale encoding.

    Raise ValueError if not found.
    Return 'Current locale (Display name)'.
    """
    encoding = get_locale_python_name()
    return _("Current locale (%s)") % get_display_name(encoding)

def get_locale_python_name_ensure(value):
    if value is not None:
        assert is_valid(value)

@util.once
@util.contractual
def get_locale_python_name():
    """Get the python name of the locale encoding or None."""

    from encodings.aliases import aliases
    encoding = locale.getpreferredencoding()
    if encoding is None:
        return None
    encoding = _re_illegal.sub("_", encoding.lower())
    if encoding in aliases:
        encoding = aliases[encoding]
    return encoding

def get_long_name(python_name):
    """Get the long name for encoding.

    Raise ValueError if not found.
    Return 'Description (Display name)'.
    """
    for seq in _encodings:
        if seq[0] == python_name:
            fields = {"description": seq[2], "encoding": seq[1]}
            return _("%(description)s (%(encoding)s)") % fields
    raise ValueError

def get_python_name(display_name):
    """Get the python name for encoding.

    Raise ValueError if not found.
    """
    for seq in _encodings:
        if seq[1] == display_name:
            return seq[0]
    raise ValueError

def get_valid_encodings():
    """Get a list of valid encodings.

    Return list of tuples of python name, display name, description.
    """
    valid_encodings = list(_encodings)
    for i, seq in enumerate(reversed(valid_encodings)):
        if not is_valid(seq[0]):
            valid_encodings.pop(i)
    return valid_encodings

def is_valid(python_name):
    """Return True is encoding is valid."""

    try:
        codecs.lookup(python_name)
        return True
    except LookupError:
        return False
