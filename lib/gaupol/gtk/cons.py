# Copyright (C) 2005-2006 Osmo Salomaa
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
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""GTK constants."""


from gettext import gettext as _


__all__ = [
    'NO',
    'SHOW',
    'HIDE',
    'DURN',
    'MTXT',
    'TTXT',
    'Column',
    'Target',
]

NO   = 0
SHOW = 1
HIDE = 2
DURN = 3
MTXT = 4
TTXT = 5


class Column(object):

    id_names = [
        'number',
        'show',
        'hide',
        'duration',
        'main_text',
        'tran_text'
    ]

    display_names = [
        _('No.'),
        _('Show'),
        _('Hide'),
        _('Duration'),
        _('Main Text'),
        _('Translation Text'),
    ]


class Target(object):

    ALL_PROJECTS       = 0
    CURRENT_PROJECT    = 1
    SELECTED_SUBTITLES = 2

    id_names = [
        'all_projects',
        'current_project',
        'selected_subtitles',
    ]
