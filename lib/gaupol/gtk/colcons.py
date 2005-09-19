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
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Column constants for gaupol.gtk."""


NO   = 0
SHOW = 1
HIDE = 2
DURN = 3
TEXT = 4
TRAN = 5

class COLUMN(object):

    ID_NAMES = [
        'number',
        'show',
        'hide',
        'duration',
        'text',
        'translation'
    ]
    
    UI_NAMES = [
        _('No.'),
        _('Show'),
        _('Hide'),
        _('Duration'),
        _('Text'),
        _('Translation'),
    ]
