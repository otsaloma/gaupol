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


"""GTK user interface."""


import gaupol
import inspect

module = inspect.getmodule(lambda: True)
gaupol.__dict__["gtk"] = module

from gaupol.gtk.const import *
from gaupol.gtk.errors import *
from gaupol.gtk import conf
from gaupol.gtk import ruler
from gaupol.gtk import util
from gaupol.gtk.meta import *
from gaupol.gtk.runner import *
from gaupol.gtk.tooltips import *
from gaupol.gtk.entries import *
from gaupol.gtk.renderers import *
from gaupol.gtk.output import *
from gaupol.gtk.view import *
from gaupol.gtk.page import *
from gaupol.gtk.dialogs import *
from gaupol.gtk import actions
from gaupol.gtk import agents
from gaupol.gtk.application import *
from gaupol.gtk import main
