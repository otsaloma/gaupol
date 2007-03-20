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


"""Dialogs."""


from .about      import AboutDialog
from .debug      import DebugDialog
from .duradjust  import DurationAdjustDialog
from .encoding   import AdvEncodingDialog
from .encoding   import EncodingDialog
from .file       import AppendDialog
from .file       import OpenDialog
from .file       import SaveDialog
from .file       import VideoDialog
from .glade      import GladeDialog
from .header     import HeaderDialog
from .insert     import InsertDialog
from .language   import LanguageDialog
from .message    import ErrorDialog
from .message    import InfoDialog
from .message    import QuestionDialog
from .message    import WarningDialog
from .multiclose import MultiCloseDialog
from .posadjust  import FrameAdjustDialog
from .posadjust  import TimeAdjustDialog
from .posshift   import FrameShiftDialog
from .posshift   import TimeShiftDialog
from .pref       import PreferencesDialog
from .previewerr import PreviewErrorDialog
from .search     import SearchDialog
from .split      import SplitDialog
from .textedit   import TextEditDialog


__all__ = [
    "AboutDialog",
    "AdvEncodingDialog",
    "AppendDialog",
    "DebugDialog",
    "DurationAdjustDialog",
    "EncodingDialog",
    "ErrorDialog",
    "FrameAdjustDialog",
    "FrameShiftDialog",
    "GladeDialog",
    "HeaderDialog",
    "InfoDialog",
    "InsertDialog",
    "LanguageDialog",
    "MultiCloseDialog",
    "OpenDialog",
    "PreferencesDialog",
    "PreviewErrorDialog",
    "QuestionDialog",
    "SaveDialog",
    "SearchDialog",
    "SplitDialog",
    "TextEditDialog",
    "TimeAdjustDialog",
    "TimeShiftDialog",
    "VideoDialog",
    "WarningDialog",]
