# Copyright (C) 2005-2006 Osmo Salomaa
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


"""GTK constants."""


from gettext import gettext as _

import gtk

from gaupol.base import cons


class Action(cons.Action):

    pass


class Column(cons.Section):

    NUMB = 0
    SHOW = 1
    HIDE = 2
    DURN = 3
    MTXT = 4
    TTXT = 5

    display_names = [
        _('No.'),
        _('Show'),
        _('Hide'),
        _('Duration'),
        _('Main Text'),
        _('Translation Text'),
    ]

    uim_action_names = [
        'toggle_number_column',
        'toggle_show_column',
        'toggle_hide_column',
        'toggle_duration_column',
        'toggle_main_text_column',
        'toggle_translation_text_column',
    ]

    uim_paths = [
        '/ui/menubar/view/columns/number',
        '/ui/menubar/view/columns/show',
        '/ui/menubar/view/columns/hide',
        '/ui/menubar/view/columns/duration',
        '/ui/menubar/view/columns/main_text',
        '/ui/menubar/view/columns/translation_text'
    ]


class Document(cons.Document):

    pass


class Format(cons.Format):

    pass


class Framerate(cons.Framerate):

    uim_action_names = [
        'view_framerate_23_976',
        'view_framerate_25',
        'view_framerate_29_97',
    ]

    uim_paths = [
        '/ui/menubar/view/framerate/23_976',
        '/ui/menubar/view/framerate/25',
        '/ui/menubar/view/framerate/29_97',
    ]


class Mode(cons.Mode):

    uim_action_names = [
        'show_times',
        'show_frames',
    ]

    uim_paths = [
        '/ui/menubar/view/times',
        '/ui/menubar/view/frames',
    ]


class Newlines(cons.Newlines):

    pass


class Target(cons.Section):

    ALL      = 0
    CURRENT  = 1
    SELECTED = 2


class Toolbar(cons.Section):

    DEFAULT    = 0
    ICONS      = 1
    TEXT       = 2
    BOTH       = 3
    BOTH_HORIZ = 4

    values = [
        -1,
        int(gtk.TOOLBAR_ICONS),
        int(gtk.TOOLBAR_TEXT),
        int(gtk.TOOLBAR_BOTH),
        int(gtk.TOOLBAR_BOTH_HORIZ),
    ]


class VideoPlayer(cons.VideoPlayer):

    pass
