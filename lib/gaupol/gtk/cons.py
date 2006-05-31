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

from gaupol.base.cons import Section
from gaupol.base.cons import Action
from gaupol.base.cons import Document
from gaupol.base.cons import Format
from gaupol.base.cons import Framerate   as BaseFramerate
from gaupol.base.cons import Mode        as BaseMode
from gaupol.base.cons import Newlines
from gaupol.base.cons import VideoPlayer


NO   = 0
SHOW = 1
HIDE = 2
DURN = 3
MTXT = 4
TTXT = 5


class Column(Section):

    """Data columns."""

    NO   = 0
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

    uim_paths = [
        '/ui/menubar/view/columns/number',
        '/ui/menubar/view/columns/show',
        '/ui/menubar/view/columns/hide',
        '/ui/menubar/view/columns/duration',
        '/ui/menubar/view/columns/main_text',
        '/ui/menubar/view/columns/tran_text',
    ]


class Framerate(BaseFramerate):

    """Valid framerates."""

    uim_paths = [
        '/ui/menubar/view/framerate/23_976',
        '/ui/menubar/view/framerate/25',
        '/ui/menubar/view/framerate/29_97',
    ]


class Mode(BaseMode):

    """Position modes."""

    uim_paths = [
        '/ui/menubar/view/times',
        '/ui/menubar/view/frames',
    ]


class Target(Section):

    """Targets where actions can be applied."""

    ALL_PROJECTS       = 0
    CURRENT_PROJECT    = 1
    SELECTED_SUBTITLES = 2
