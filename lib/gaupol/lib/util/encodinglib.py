# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
Encodings and encoding names.

Python name     : Encoding name used in code
Display name    : Somewhat standards compliant encoding name
Description     : Short description of language, character set or region
Descriptive name: A more informative name - "Description (Display name)"

Description and descriptive names are translation dependent. Also, the format
of descriptive name is translation dependent.
"""

# Display names mostly from
# http://www.iana.org/assignments/character-sets


import codecs
import locale


PY_NAME, DISP_NAME, DESC = 0, 1, 2

# This list cannot be used directly because some encodings might require
# additional modules installed to be available. Hence the functions should be
# used to acquire a list of available encodings.
ENCODINGS = (
    # Python name     , Display name      , Description
    ('ascii'          , 'US-ASCII'        , _('English')),
    ('big5'           , 'Big5'            , _('Chinese traditional')),
    ('big5hkscs'      , 'Big5-HKSCS'      , _('Chinese traditional')),
    ('cp037'          , 'IBM037'          , _('English')),
    ('cp424'          , 'IBM242'          , _('Hebrew')),
    ('cp437'          , 'IBM437'          , _('English')),
    ('cp500'          , 'IBM500'          , _('Western')),
    ('cp737'          , 'IBM737'          , _('Greek')),
    ('cp775'          , 'IBM775'          , _('Baltic')),
    ('cp850'          , 'IBM850'          , _('Western')),
    ('cp852'          , 'IBM852'          , _('Central European')),
    ('cp855'          , 'IBM855'          , _('Cyrillic')),
    ('cp856'          , 'IBM856'          , _('Hebrew')),
    ('cp857'          , 'IBM857'          , _('Turkish')),
    ('cp860'          , 'IBM860'          , _('Portugese')),
    ('cp861'          , 'IBM861'          , _('Icelandic')),
    ('cp862'          , 'IBM862'          , _('Hebrew')),
    ('cp863'          , 'IBM863'          , _('Canadian')),
    ('cp864'          , 'IBM864'          , _('Arabic')),
    ('cp865'          , 'IBM865'          , _('Nordic')),
    ('cp866'          , 'IBM866'          , _('Russian')),
    ('cp869'          , 'IBM869'          , _('Greek')),
    ('cp874'          , 'IBM874'          , _('Thai')),
    ('cp875'          , 'IBM875'          , _('Greek')),
    ('cp932'          , 'IBM932'          , _('Japanese')),
    ('cp949'          , 'IBM949'          , _('Korean')),
    ('cp950'          , 'IBM950'          , _('Chinese traditional')),
    ('cp1006'         , 'IBM1006'         , _('Urdu')),
    ('cp1026'         , 'IBM1026'         , _('Turkish')),
    ('cp1140'         , 'IBM1140'         , _('Western')),
    ('cp1250'         , 'windows-1250'    , _('Central European')),
    ('cp1251'         , 'windows-1251'    , _('Cyrillic')),
    ('cp1252'         , 'windows-1252'    , _('Western')),
    ('cp1253'         , 'windows-1253'    , _('Greek')),
    ('cp1254'         , 'windows-1254'    , _('Turkish')),
    ('cp1255'         , 'windows-1255'    , _('Hebrew')),
    ('cp1256'         , 'windows-1256'    , _('Arabic')),
    ('cp1257'         , 'windows-1257'    , _('Baltic')),
    ('cp1258'         , 'windows-1258'    , _('Vietnamese')),
    ('euc_jp'         , 'EUC-JP'          , _('Japanese')),
    ('euc_jis_2004'   , 'EUC-JIS-2004'    , _('Japanese')),
    ('euc_jisx0213'   , 'EUC-JISX0213'    , _('Japanese')),
    ('euc_kr'         , 'EUC-KR'          , _('Korean')),
    ('gb2312'         , 'GB2312'          , _('Chinese simplified')),
    ('gbk'            , 'GBK'             , _('Chinese unified')),
    ('gb18030'        , 'GB18030'         , _('Chinese unified')),
    ('hz'             , 'HZ'              , _('Chinese simplified')),
    ('iso2022_jp'     , 'ISO-2022-JP'     , _('Japanese')),
    ('iso2022_jp_1'   , 'ISO-2022-JP-1'   , _('Japanese')),
    ('iso2022_jp_2'   , 'ISO-2022-JP-2'   , _('Japanese')),
    ('iso2022_jp_2004', 'ISO-2022-JP-2004', _('Japanese')),
    ('iso2022_jp_3'   , 'ISO-2022-JP-3'   , _('Japanese')),
    ('iso2022_jp_ext' , 'ISO-2022-JP-EXT' , _('Japanese')),
    ('iso2022_kr'     , 'ISO-2022-KR'     , _('Korean')),
    ('latin_1'        , 'ISO-8859-1'      , _('Western')),
    ('iso8859_2'      , 'ISO-8859-2'      , _('Central European')),
    ('iso8859_3'      , 'ISO-8859-3'      , _('South European')),
    ('iso8859_4'      , 'ISO-8859-4'      , _('Baltic')),
    ('iso8859_5'      , 'ISO-8859-5'      , _('Cyrillic')),
    ('iso8859_6'      , 'ISO-8859-6'      , _('Arabic')),
    ('iso8859_7'      , 'ISO-8859-7'      , _('Greek')),
    ('iso8859_8'      , 'ISO-8859-8'      , _('Hebrew')),
    ('iso8859_9'      , 'ISO-8859-9'      , _('Turkish')),
    ('iso8859_10'     , 'ISO-8859-10'     , _('Nordic')),
    ('iso8859_13'     , 'ISO-8859-13'     , _('Baltic')),
    ('iso8859_14'     , 'ISO-8859-14'     , _('Celtic')),
    ('iso8859_15'     , 'ISO-8859-15'     , _('Western')),
    ('johab'          , 'Johab'           , _('Korean')),
    ('koi8_r'         , 'KOI8-R'          , _('Russian')),
    ('koi8_u'         , 'KOI8-U'          , _('Ukrainian')),
    ('mac_cyrillic'   , 'MacCyrillic'     , _('Cyrillic')),
    ('mac_greek'      , 'MacGreek'        , _('Greek')),
    ('mac_iceland'    , 'MacIceland'      , _('Icelandic')),
    ('mac_latin2'     , 'MacCentralEurope', _('Central European')),
    ('mac_roman'      , 'MacRoman'        , _('Western')),
    ('mac_turkish'    , 'MacTurkish'      , _('Turkish')),
    ('ptcp154'        , 'PTCP154'         , _('Cyrillic Asian')),
    ('shift_jis'      , 'Shift_JIS'       , _('Japanese')),
    ('shift_jis_2004' , 'Shift_JIS-2004'  , _('Japanese')),
    ('shift_jisx0213' , 'Shift_JISX0213'  , _('Japanese')),
    ('utf_16'         , 'UTF-16'          , _('Unicode')),
    ('utf_16_be'      , 'UTF-16BE'        , _('Unicode')),
    ('utf_16_le'      , 'UTF-16LE'        , _('Unicode')),
    ('utf_7'          , 'UTF-7'           , _('Unicode')),
    ('utf_8'          , 'UTF-8'           , _('Unicode'))
)


def get_description(python_name):
    """
    Get description of an encoding.
    
    Return value is translation dependent.
    Raise ValueError if not found.
    """
    for entry in ENCODINGS:
        if entry[PY_NAME] == python_name:
            return entry[PY_NAME]

    raise ValueError('Invalid encoding Python name "%s".' % python_name)

def get_descriptive_name(python_name):
    """
    Get descriptive name for encoding.
    
    Raise ValueError if not found.
    Return value and its format are translation dependent.
    Return: "description (display name)" or None
    """
    for entry in ENCODINGS:
        if entry[PY_NAME] == python_name:
            # TRANSLATORS: Encoding descriptive name - e.g. "Unicode (UTF-8)".
            return _('%s (%s)') % (entry[DESC], entry[DISP_NAME])

    raise ValueError('Invalid encoding Python name "%s".' % python_name)
                    
def get_display_name(python_name):
    """
    Get display name of an encoding.
    
    Raise ValueError if not found.
    """
    for entry in ENCODINGS:
        if entry[PY_NAME] == python_name:
            return entry[DISP_NAME]
    
    raise ValueError('Invalid encoding Python name "%s".' % python_name)

def get_locale_encoding():
    """
    Get locale encoding.
    
    Return: (Python name, display name, description) or None
    """
    python_name = locale.getdefaultlocale()[1]

    try:
        locale_tuple = codecs.lookup(python_name)
    except (TypeError, LookupError):
        return None

    for entry in ENCODINGS:
        if codecs.lookup(entry[PY_NAME]) == locale_tuple:
            return entry

    return None

def get_locale_descriptive_name():
    """
    Get descriptive name for locale encoding.
    
    Return value and its format are translation dependent.
    Return: "Current locale (display name)" or None
    """
    locale_tuple = get_locale_encoding()

    if locale_tuple is None:
        return None

    return _('Current locale (%s)') % locale_tuple[DISP_NAME]

def get_python_name(display_name):
    """
    Get Python name of an encoding.
    
    Raise ValueError if not found.
    """
    for entry in ENCODINGS:
        if entry[DISP_NAME] == display_name:
            return entry[PY_NAME]

    raise ValueError('Invalid encoding display name "%s".' % display_name)

def get_valid_encodings():
    """
    Get a list of valid encodings.
    
    Return: list with elements (Python name, display name, description)
    """
    valid_encodings = []
    
    for entry in ENCODINGS:
        if is_valid_python_name(entry[PY_NAME]):
            valid_encodings.append(entry)
    
    return valid_encodings
    
def get_valid_descriptive_names():
    """
    Get a list of valid descriptive names.

    Return value and its format are translation dependent.
    Return: list with elements "description (display name)"
    """
    valid_names = []
    
    for entry in ENCODINGS:
        if is_valid_python_name(entry[PY_NAME]):
            # TRANSLATORS: Encoding descriptive name - e.g. "Unicode (UTF-8)".
            valid_names.append(_('%s (%s)') % (entry[DESC], entry[DISP_NAME]))
    
    return valid_names

def get_valid_python_names():
    """Get a list of valid encoding Python names."""

    valid_names = []
    
    for entry in ENCODINGS:
        if is_valid_python_name(entry[PY_NAME]):
            valid_names.append(entry[PY_NAME])
    
    return valid_names

def is_valid_python_name(python_name):
    """Return whether encoding is valid or not."""

    # Empty string lookup returns tuple for UCS-4LE!
    if not python_name:
        return False

    try:
        codecs.lookup(python_name)
        return True
    except (LookupError, TypeError):
        return False
