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


"""Error classes."""


class GaupolBaseError(Exception):

    """Base class for error of gaupol.base module."""

    pass


class ExternalError(GaupolBaseError):

    """External command failed."""

    pass

class FileFormatError(GaupolBaseError):

    """Unrecognized subtitle file format."""

    pass


class FitError(GaupolBaseError):

    """Data does not fit in given space."""

    pass


class TimeoutError(GaupolBaseError):

    """Connection timed out."""

    pass

