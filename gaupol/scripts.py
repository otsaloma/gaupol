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

"""Names and ISO 15924 codes for scripts and conversions between them.

Module variable 'scripts' is a dictionary mapping four-letter ISO 15924 codes
to localized names scripts.
"""

# http://www.unicode.org/iso15924/codelists.html
# http://en.wikipedia.org/wiki/List_of_ISO_15924_codes

import gaupol
import re
_ = gaupol.i18n._

scripts = {
    # Translators: If some of the more bizarre of the following script names
    # are left untranslated, it's no big deal. You might find translations of
    # some of the script names in ICU project locale files.
    # http://source.icu-project.org/repos/icu/icu/trunk/source/data/locales/
    "Arab": _("Arabic"),
    "Armn": _("Armenian"),
    "Avst": _("Avestan"),
    "Bali": _("Balinese"),
    "Batk": _("Batak"),
    "Beng": _("Bengali"),
    "Blis": _("Blissymbols"),
    "Bopo": _("Bopomofo"),
    "Brah": _("Brahmi"),
    "Brai": _("Braille"),
    "Bugi": _("Buginese"),
    "Buhd": _("Buhid"),
    "Cans": _("Unified Canadian Aboriginal Syllabics"),
    "Cari": _("Carian"),
    "Cham": _("Cham"),
    "Cher": _("Cherokee"),
    "Cirt": _("Cirth"),
    "Copt": _("Coptic"),
    "Cprt": _("Cypriot"),
    "Cyrl": _("Cyrillic"),
    "Cyrs": _("Old Church Slavonic Cyrillic"),
    "Deva": _("Devanagari"),
    "Dsrt": _("Deseret"),
    "Egyd": _("Egyptian demotic"),
    "Egyh": _("Egyptian hieratic"),
    "Egyp": _("Egyptian hieroglyphs"),
    "Ethi": _("Ethiopic"),
    "Geor": _("Georgian"),
    "Geok": _("Khutsuri"),
    "Glag": _("Glagolitic"),
    "Goth": _("Gothic"),
    "Grek": _("Greek"),
    "Gujr": _("Gujarati"),
    "Guru": _("Gurmukhi"),
    "Hang": _("Hangul"),
    "Hani": _("Han"),
    "Hano": _("Hanunoo"),
    "Hans": _("Simplified Han"),
    "Hant": _("Traditional Han"),
    "Hebr": _("Hebrew"),
    "Hira": _("Hiragana"),
    "Hmng": _("Pahawh Hmong"),
    "Hrkt": _("Kana"),
    "Hung": _("Old Hungarian"),
    "Inds": _("Indus"),
    "Ital": _("Old Italic"),
    "Java": _("Javanese"),
    "Jpan": _("Japanese"),
    "Kali": _("Kayah Li"),
    "Kana": _("Katakana"),
    "Khar": _("Kharoshthi"),
    "Khmr": _("Khmer"),
    "Knda": _("Kannada"),
    "Kore": _("Korean"),
    "Lana": _("Lanna"),
    "Laoo": _("Lao"),
    "Latf": _("Fraktur Latin"),
    "Latg": _("Gaelic Latin"),
    "Latn": _("Latin"),
    "Lepc": _("Lepcha"),
    "Limb": _("Limbu"),
    "Lina": _("Linear A"),
    "Linb": _("Linear B"),
    "Lyci": _("Lycian"),
    "Lydi": _("Lydian"),
    "Mand": _("Mandaic"),
    "Mani": _("Manichaean"),
    "Maya": _("Mayan hieroglyphs"),
    "Mero": _("Meroitic"),
    "Mlym": _("Malayalam"),
    "Moon": _("Moon"),
    "Mong": _("Mongolian"),
    "Mtei": _("Meitei Mayek"),
    "Mymr": _("Myanmar"),
    "Nkoo": _("N'Ko"),
    "Ogam": _("Ogham"),
    "Olck": _("Ol Chiki"),
    "Orkh": _("Orkhon"),
    "Orya": _("Oriya"),
    "Osma": _("Osmanya"),
    "Perm": _("Old Permic"),
    "Phag": _("Phags-pa"),
    "Phlv": _("Book Pahlavi"),
    "Phnx": _("Phoenician"),
    "Plrd": _("Pollard Phonetic"),
    "Rjng": _("Rejang"),
    "Roro": _("Rongorongo"),
    "Runr": _("Runic"),
    "Samr": _("Samaritan"),
    "Sara": _("Sarati"),
    "Saur": _("Saurashtra"),
    "Sgnw": _("Sign Writing"),
    "Shaw": _("Shavian"),
    "Sinh": _("Sinhala"),
    "Sund": _("Sundanese"),
    "Sylo": _("Syloti Nagri"),
    "Syrc": _("Syriac"),
    "Syre": _("Estrangelo Syriac"),
    "Syrj": _("Western Syriac"),
    "Syrn": _("Eastern Syriac"),
    "Tagb": _("Tagbanwa"),
    "Tale": _("Tai Le"),
    "Talu": _("New Tai Lue"),
    "Taml": _("Tamil"),
    "Telu": _("Telugu"),
    "Teng": _("Tengwar"),
    "Tfng": _("Tifinagh"),
    "Tglg": _("Tagalog"),
    "Thaa": _("Thaana"),
    "Thai": _("Thai"),
    "Tibt": _("Tibetan"),
    "Ugar": _("Ugaritic"),
    "Vaii": _("Vai"),
    "Visp": _("Visible Speech"),
    "Xpeo": _("Old Persian"),
    "Xsux": _("Cuneiform"),
    "Yiii": _("Yi"),}


def code_to_name_require(code):
    assert re.match(r"^[A-Z][a-z]{3}$", code)

@gaupol.util.contractual
def code_to_name(code):
    """Convert ISO 15924 code to localized script name.

    Raise KeyError if code not found.
    """
    return scripts[code]
