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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Dialogs."""

from .about       import AboutDialog
from .debug       import DebugDialog
from .duration    import DurationAdjustDialog
from .encoding    import AdvEncodingDialog
from .encoding    import EncodingDialog
from .file        import AppendDialog
from .file        import OpenDialog
from .file        import SaveDialog
from .file        import VideoDialog
from .framerate   import FramerateConvertDialog
from .glade       import GladeDialog
from .header      import HeaderDialog
from .insert      import InsertDialog
from .language    import LanguageDialog
from .message     import ErrorDialog
from .message     import InfoDialog
from .message     import QuestionDialog
from .message     import WarningDialog
from .multiclose  import MultiCloseDialog
from .preferences import PreferencesDialog
from .previewerr  import PreviewErrorDialog
from .search      import SearchDialog
from .shift       import FrameShiftDialog
from .shift       import TimeShiftDialog
from .spellcheck  import SpellCheckDialog
from .split       import SplitDialog
from .textedit    import TextEditDialog
from .transform   import FrameTransformDialog
from .transform   import TimeTransformDialog

__all__ = [x for x in dir() if x.endswith("Dialog")]
