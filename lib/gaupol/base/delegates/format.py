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


"""Text formatting."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.base.tags.classes import *
from gaupol.base.util         import relib
from gaupol.constants         import Document, Format


class FormatDelegate(Delegate):

    """Text formatting."""

    def _get_format_class_name(self, document):
        """
        Get the class name of document's file format.

        Translation column will inherit original column's format if
        translation file does not exist.
        Return name or None.
        """
        if document == Document.MAIN:
            try:
                return Format.class_names[self.main_file.format]
            except AttributeError:
                return None

        elif document == Document.TRAN:
            try:
                return Format.class_names[self.tran_file.format]
            except AttributeError:
                return self._get_format_class_name(Document.MAIN)

    def get_regular_expression_for_tag(self, document):
        """
        Get the regular expression for a text tag for document.

        Return re pattern or None.
        """
        format_name = self._get_format_class_name(document)

        if format_name is None:
            return None

        regex, flags = eval(format_name).tag
        return relib.compile(regex, flags)
