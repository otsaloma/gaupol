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


"""Dialog for editing subtitle file headers."""


from gettext import gettext as _

import gtk

from gaupol.base.file.classes  import *
from gaupol.gtk                import cons
from gaupol.gtk.dialog.message import ErrorDialog
from gaupol.gtk.util           import gtklib


class _MPsubErrorDialog(ErrorDialog):

    """Dialog to inform that MPsub header is invalid."""

    def __init__(self, parent):

        ErrorDialog.__init__(
            self, parent,
            _('Invalid header'),
            _('MPsub header must contain a FORMAT line with a value of '
              '"TIME", "23.98", "25.00" or "29.97".')
        )


class HeaderDialog(object):

    """Dialog for editing subtitle file headers."""

    def __init__(self, parent, project):

        self._main_orig = None
        self._main_temp = None
        self._project   = project
        self._tran_orig = None
        self._tran_temp = None

        glade_xml = gtklib.get_glade_xml('header-dialog')
        self._copy_down_button   = glade_xml.get_widget('copy_down_button')
        self._copy_hbox          = glade_xml.get_widget('copy_hbox')
        self._copy_up_button     = glade_xml.get_widget('copy_up_button')
        self._dialog             = glade_xml.get_widget('dialog')
        self._main_clear_button  = glade_xml.get_widget('main_clear_button')
        self._main_revert_button = glade_xml.get_widget('main_revert_button')
        self._main_temp_button   = glade_xml.get_widget('main_temp_button')
        self._main_text_view     = glade_xml.get_widget('main_text_view')
        self._main_vbox          = glade_xml.get_widget('main_vbox')
        self._tran_clear_button  = glade_xml.get_widget('tran_clear_button')
        self._tran_revert_button = glade_xml.get_widget('tran_revert_button')
        self._tran_temp_button   = glade_xml.get_widget('tran_temp_button')
        self._tran_text_view     = glade_xml.get_widget('tran_text_view')
        self._tran_vbox          = glade_xml.get_widget('tran_vbox')

        self._init_signals()
        self._init_data()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_main_header(self):
        """Get main header."""

        text_buffer = self._main_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end)

    def _get_translation_header(self):
        """Get translation header."""

        text_buffer = self._tran_text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end)

    def _init_data(self):
        """Initialize header data."""

        main_file = self._project.main_file
        if main_file is not None and main_file.has_header:
            self._main_orig = main_file.header
            self._set_main_header(self._main_orig)
            self._main_temp = main_file.get_template_header()
        else:
            self._main_vbox.props.visible  = False
            self._copy_hbox.props.visible  = False

        tran_file = self._project.tran_file
        if tran_file is not None and tran_file.has_header:
            self._tran_orig = tran_file.header
            self._set_translation_header(self._tran_orig)
            self._tran_temp = tran_file.get_template_header()
        else:
            self._tran_vbox.props.visible  = False
            self._copy_hbox.props.visible  = False

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_copy_down_button'  , 'clicked' )
        gtklib.connect(self, '_copy_up_button'    , 'clicked' )
        gtklib.connect(self, '_dialog'            , 'response')
        gtklib.connect(self, '_main_clear_button' , 'clicked' )
        gtklib.connect(self, '_main_revert_button', 'clicked' )
        gtklib.connect(self, '_main_temp_button'  , 'clicked' )
        gtklib.connect(self, '_tran_clear_button' , 'clicked' )
        gtklib.connect(self, '_tran_revert_button', 'clicked' )
        gtklib.connect(self, '_tran_temp_button'  , 'clicked' )

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label('x' * 60)
        width = label.size_request()[0] + 166 + gtklib.EXTRA

        if self._main_vbox.props.visible and self._tran_vbox.props.visible:
            main_height = gtk.Label(self._main_orig).size_request()[1]
            tran_height = gtk.Label(self._tran_orig).size_request()[1]
            height = 2 * max(main_height, tran_height) + 205 + gtklib.EXTRA
        elif self._main_vbox.props.visible:
            height = gtk.Label(self._main_orig).size_request()[1]
            height = height + 90 + gtklib.EXTRA
        elif self._tran_vbox.props.visible:
            height = gtk.Label(self._tran_orig).size_request()[1]
            height = height + 90 + gtklib.EXTRA

        gtklib.resize_dialog(self._dialog, width, height)

    def _on_copy_down_button_clicked(self, *args):
        """Copy main header to translation header."""

        self._set_translation_header(self._get_main_header())

    def _on_copy_up_button_clicked(self, *args):
        """Copy translation header to main header."""

        self._set_main_header(self._get_translation_header())

    def _on_dialog_response(self, dialog, response):
        """Save headers."""

        if response != gtk.RESPONSE_OK:
            return

        for file_, header in (
            (self._project.main_file, self._get_main_header()       ),
            (self._project.tran_file, self._get_translation_header()),
        ):
            if file_ is None or not file_.has_header:
                continue
            if file_.format == cons.Format.MPSUB:
                try:
                    file_.set_header(header)
                except ValueError:
                    gtklib.run(_MPsubErrorDialog(self._dialog))
                    return self._dialog.run()
                if file_.framerate is not None:
                    self._project.set_framerate(file_.framerate, register=None)
            else:
                file_.header = header

    def _on_main_clear_button_clicked(self, *args):
        """Clear main header."""

        self._set_main_header(u'')

    def _on_main_temp_button_clicked(self, *args):
        """Set main header to template."""

        self._set_main_header(self._main_temp)

    def _on_main_revert_button_clicked(self, *args):
        """Revert main header."""

        self._set_main_header(self._main_orig)

    def _on_tran_clear_button_clicked(self, *args):
        """Clear translation header."""

        self._set_translation_header(u'')

    def _on_tran_temp_button_clicked(self, *args):
        """Set translation header to template."""

        self._set_translation_header(self._tran_temp)

    def _on_tran_revert_button_clicked(self, *args):
        """Revert translation header."""

        self._set_translation_header(self._tran_orig)

    def _set_main_header(self, header):
        """Set main header."""

        self._main_text_view.get_buffer().set_text(header)

    def _set_translation_header(self, header):
        """Set translation header."""

        self._tran_text_view.get_buffer().set_text(header)

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
