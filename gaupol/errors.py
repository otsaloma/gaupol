# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""All error classes."""

__all__ = (
    "Error",
    "AffirmationError",
    "FormatError",
    "ParseError",
    "ProcessError",)


class Error(Exception):

    """Base class for all Gaupol errors."""

    pass


class AffirmationError(Error):

    """Something expected to be True was False.

    This is similar to AssertionError, but without the special reliance on
    __debug__ and given optimization options. AffirmationError is used to
    provide essential checks instead of optional debug checks.
    """

    pass


class FormatError(Error):

    """Unrecognized subtitle file format."""

    pass


class ParseError(Error):

    """Failed to parse a subtitle file into positions and texts.

    The error is either a syntax error in the file being parsed or a
    programming error in the code doing the parsing.
    """

    pass


class ProcessError(Error):

    """Error in an external process."""

    pass
