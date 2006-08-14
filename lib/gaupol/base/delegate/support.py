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


"""Support methods for subtitle data editing."""


from gettext import gettext as _
import bisect
import copy
import re

from gaupol.base              import cons
from gaupol.base.icons        import *
from gaupol.base.delegate     import Delegate, revertablemethod
from gaupol.base.tags.classes import *


class SupportDelegate(Delegate):

    """Support methods for subtitle data editing."""

    def expand_frames(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        frames = [show, hide, self.calc.get_frame_duration(show, hide)]
        times = list(self.calc.frame_to_time(x) for x in (show, hide))
        times.append(self.calc.get_time_duration(times[0], times[1]))
        return times, frames

    def expand_positions(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        if isinstance(show, basestring):
            return self.expand_times(show, hide)
        if isinstance(show, int):
            return self.expand_frames(show, hide)
        raise ValueError

    def expand_times(self, show, hide):
        """
        Expand single subtitle position data to all quantities.

        Return times, frames.
        """
        times = [show, hide, self.calc.get_time_duration(show, hide)]
        frames = list(self.calc.time_to_frame(x) for x in (show, hide))
        frames.append(self.calc.get_frame_duration(frames[0], frames[1]))
        return times, frames

    def get_format_class_name(self, doc):
        """
        Get class name of document's file format.

        Translation document will inherit main document's format if needed.
        Return name or None.
        """
        if doc == MAIN:
            try:
                return cons.Format.class_names[self.main_file.format]
            except AttributeError:
                return None
        elif doc == TRAN:
            try:
                return cons.Format.class_names[self.tran_file.format]
            except AttributeError:
                return self._get_format_class_name(MAIN)

    def get_mode(self):
        """Get mode of main file or default."""

        try:
            return self.main_file.mode
        except AttributeError:
            return cons.Mode.TIME

    def get_positions(self):
        """Get either times or frames depending mode."""

        mode = self.get_mode()
        if mode == cons. Mode.TIME:
            return self.times
        if mode == cons.Mode.FRAME:
            return self.frames

    def get_tag_regex(self, document):
        """Get regular expression for tag in document or None."""

        name = self.get_format_class_name(document)
        if name is None:
            return None
        if eval(name).tag is None:
            return None

        return re.compile(*eval(name).tag)

    def not_really_do(self, method, args=[], kwargs={}):
        """
        Run method without keeping changes.

        Return times, frames, main texts, translation texts.
        """
        orig_times = copy.deepcopy(self.times)
        orig_frames = copy.deepcopy(self.frames)
        orig_main_texts = copy.deepcopy(self.main_texts)
        orig_tran_texts = copy.deepcopy(self.tran_texts)

        kwargs['register'] = None
        method(*args, **kwargs)

        new_times = copy.deepcopy(self.times)
        new_frames = copy.deepcopy(self.frames)
        new_main_texts = copy.deepcopy(self.main_texts)
        new_tran_texts = copy.deepcopy(self.tran_texts)

        self.times = orig_times
        self.frames = orig_frames
        self.main_texts = orig_main_texts
        self.tran_texts = orig_tran_texts

        return new_times, new_frames, new_main_texts, new_tran_texts

    @revertablemethod
    def replace_both_texts(self, rows, new_texts, register=-1):
        """
        Replace texts in both documents' rows with new_texts.

        rows: Main rows, tran rows
        new_texts: New main texts, new tran texts
        """
        if not rows[0] and not rows[1]:
            return
        if not rows[1]:
            return self.replace_texts(
                rows[0], MAIN, new_texts[0], register=register)
        if not rows[0]:
            return self.replace_texts(
                rows[1], TRAN, new_texts[1], register=register)

        self.replace_texts(rows[0], MAIN, new_texts[0], register=register)
        self.replace_texts(rows[1], TRAN, new_texts[1], register=register)
        self.group_actions(register, 2, _('Replacing texts'))

    @revertablemethod
    def replace_positions(self, rows, new_times, new_frames, register=-1):
        """Replace times and frames in rows with new_times and new_frames."""

        orig_times  = []
        orig_frames = []
        for i, row in enumerate(rows):
            orig_times.append(self.times[row])
            orig_frames.append(self.frames[row])
            self.times[row] = new_times[i]
            self.frames[row] = new_frames[i]

        self.register_action(
            register=register,
            docs=[MAIN, TRAN],
            description=_('Replacing positions'),
            revert_method=self.replace_positions,
            revert_args=[rows, orig_times, orig_frames],
            updated_positions=rows,
        )

    @revertablemethod
    def replace_texts(self, rows, doc, new_texts, register=-1):
        """Replace texts in document's rows with new_texts."""

        if doc == MAIN:
            texts = self.main_texts
            updated_main_texts = rows
            updated_tran_texts = []
        elif doc == TRAN:
            texts = self.tran_texts
            updated_main_texts = []
            updated_tran_texts = rows

        orig_texts = []
        for i, row in enumerate(rows):
            orig_texts.append(texts[row])
            texts[row] = new_texts[i]

        self.register_action(
            register=register,
            docs=[doc],
            description=_('Replacing texts'),
            revert_method=self.replace_texts,
            revert_args=[rows, doc, orig_texts],
            updated_main_texts=updated_main_texts,
            updated_tran_texts=updated_tran_texts
        )
