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
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""
Paths used by Gaupol.

The values of the paths default to their values in the source distribution.
When installing, this file should be overwritten with the correct paths during
installation process.
"""


import os


__all__ = [
    'DATA_DIR',
    'GLADE_DIR',
    'ICON_DIR',
    'UI_DIR',
    'LOCALE_DIR',
]

current_dir = os.path.dirname(os.path.abspath(__file__))
prefix = os.path.join(current_dir, '..', '..', '..')

DATA_DIR   = os.path.join(prefix  , 'data'  )
GLADE_DIR  = os.path.join(DATA_DIR, 'glade' )
ICON_DIR   = os.path.join(DATA_DIR, 'icons' )
UI_DIR     = os.path.join(DATA_DIR, 'ui'    )
LOCALE_DIR = os.path.join(prefix  , 'locale')
