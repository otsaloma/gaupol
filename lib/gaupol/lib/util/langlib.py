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


"""Language names and their two-letter ISO 639 codes."""


LANGS = {
    # TRANSLATORS: Search the web for a list of ISO 639 two-letter language
    # codes in your language. Entries are in alphabetical order according to
    # the language code.
    'aa': _('Afar'),
    'ab': _('Abkhazian'),
    'af': _('Afrikaans'),
    'am': _('Amharic'),
    'ar': _('Arabic'),
    'as': _('Assamese'),
    'ay': _('Aymara'),
    'az': _('Azerbaijani'),
    'ba': _('Bashkir'),
    'be': _('Byelorussian'),
    'bg': _('Bulgarian'),
    'bh': _('Bihari'),
    'bi': _('Bislama'),
    'bn': _('Bengali, Bangla'),
    'bo': _('Tibetan'),
    'br': _('Breton'),
    'ca': _('Catalan'),
    'co': _('Corsican'),
    'cs': _('Czech'),
    'cy': _('Welsh'),
    'da': _('Danish'),
    'de': _('German'),
    'dz': _('Bhutani'),
    'el': _('Greek'),
    'en': _('English'),
    'eo': _('Esperanto'),
    'es': _('Spanish'),
    'et': _('Estonian'),
    'eu': _('Basque'),
    'fa': _('Persian'),
    'fi': _('Finnish'),
    'fj': _('Fiji'),
    'fo': _('Faeroese'),
    'fr': _('French'),
    'fy': _('Frisian'),
    'ga': _('Irish'),
    'gd': _('Scots Gaelic'),
    'gl': _('Galician'),
    'gn': _('Guarani'),
    'gu': _('Gujarati'),
    'ha': _('Hausa'),
    'hi': _('Hindi'),
    'hr': _('Croatian'),
    'hu': _('Hungarian'),
    'hy': _('Armenian'),
    'ia': _('Interlingua'),
    'ie': _('Interlingue'),
    'ik': _('Inupiak'),
    'in': _('Indonesian'),
    'is': _('Icelandic'),
    'it': _('Italian'),
    'iw': _('Hebrew'),
    'ja': _('Japanese'),
    'ji': _('Yiddish'),
    'jw': _('Javanese'),
    'ka': _('Georgian'),
    'kk': _('Kazakh'),
    'kl': _('Greenlandic'),
    'km': _('Cambodian'),
    'kn': _('Kannada'),
    'ko': _('Korean'),
    'ks': _('Kashmiri'),
    'ku': _('Kurdish'),
    'ky': _('Kirghiz'),
    'la': _('Latin'),
    'ln': _('Lingala'),
    'lo': _('Laothian'),
    'lt': _('Lithuanian'),
    'lv': _('Latvian, Lettish'),
    'mg': _('Malagasy'),
    'mi': _('Maori'),
    'mk': _('Macedonian'),
    'ml': _('Malayalam'),
    'mn': _('Mongolian'),
    'mo': _('Moldavian'),
    'mr': _('Marathi'),
    'ms': _('Malay'),
    'mt': _('Maltese'),
    'my': _('Burmese'),
    'na': _('Nauru'),
    'ne': _('Nepali'),
    'nl': _('Dutch'),
    'no': _('Norwegian'),
    'oc': _('Occitan'),
    'om': _('(Afan) Oromo'),
    'or': _('Oriya'),
    'pa': _('Punjabi'),
    'pl': _('Polish'),
    'ps': _('Pashto, Pushto'),
    'pt': _('Portuguese'),
    'qu': _('Quechua'),
    'rm': _('Rhaeto-Romance'),
    'rn': _('Kirundi'),
    'ro': _('Romanian'),
    'ru': _('Russian'),
    'rw': _('Kinyarwanda'),
    'sa': _('Sanskrit'),
    'sd': _('Sindhi'),
    'sg': _('Sangro'),
    'sh': _('Serbo-Croatian'),
    'si': _('Singhalese'),
    'sk': _('Slovak'),
    'sl': _('Slovenian'),
    'sm': _('Samoan'),
    'sn': _('Shona'),
    'so': _('Somali'),
    'sq': _('Albanian'),
    'sr': _('Serbian'),
    'ss': _('Siswati'),
    'st': _('Sesotho'),
    'su': _('Sundanese'),
    'sv': _('Swedish'),
    'sw': _('Swahili'),
    'ta': _('Tamil'),
    'te': _('Tegulu'),
    'tg': _('Tajik'),
    'th': _('Thai'),
    'ti': _('Tigrinya'),
    'tk': _('Turkmen'),
    'tl': _('Tagalog'),
    'tn': _('Setswana'),
    'to': _('Tonga'),
    'tr': _('Turkish'),
    'ts': _('Tsonga'),
    'tt': _('Tatar'),
    'tw': _('Twi'),
    'uk': _('Ukrainian'),
    'ur': _('Urdu'),
    'uz': _('Uzbek'),
    'vi': _('Vietnamese'),
    'vo': _('Volapuk'),
    'wo': _('Wolof'),
    'xh': _('Xhosa'),
    'yo': _('Yoruba'),
    'zh': _('Chinese'),
    'zu': _('Zulu'),
}


def get_language(code):
    """
    Get language based on language code.
    
    Only the first two letters of the language code will be considered, so
    giving e.g. "en_US" will return the same as giving "en".
    
    Raise KeyError is language not found.
    """
    return LANGS[code[:2]]
