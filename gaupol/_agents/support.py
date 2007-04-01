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


import re
from gettext import gettext as _

from gaupol import cons, util
from gaupol.base import Delegate, notify_frozen
from gaupol.tags import *
from .register import revertable


class SupportAgent(Delegate):

    """Support methods for subtitle data editing."""

    # pylint: disable-msg=E0203,W0201

    def expand_frames(self, show, hide):
        """Expand single subtitle position data to all items.

        Return time, frame.
        """
        frame = [show, hide, self.calc.get_frame_duration(show, hide)]
        time = [self.calc.frame_to_time(x) for x in (show, hide)]
        time.append(self.calc.get_time_duration(time[0], time[1]))
        return time, frame

    def expand_positions(self, show, hide):
        """Expand single subtitle position data to all items.

        Return time, frame.
        """
        if isinstance(show, basestring):
            return self.expand_times(show, hide)
        if isinstance(show, int):
            return self.expand_frames(show, hide)
        if isinstance(show, float):
            return self.expand_seconds(show, hide)
        raise ValueError

    def expand_seconds(self, show, hide):
        """Expand single subtitle position data to all items.

        Return time, frame.
        """
        time = [self.calc.seconds_to_time(x) for x in (show, hide)]
        time.append(self.calc.get_time_duration(time[0], time[1]))
        frame = [self.calc.seconds_to_frame(x) for x in (show, hide)]
        frame.append(self.calc.get_frame_duration(frame[0], frame[1]))
        return time, frame

    def expand_times(self, show, hide):
        """Expand single subtitle position data to all items.

        Return time, frame.
        """
        time = [show, hide, self.calc.get_time_duration(show, hide)]
        frame = [self.calc.time_to_frame(x) for x in (show, hide)]
        frame.append(self.calc.get_frame_duration(frame[0], frame[1]))
        return time, frame

    def get_file(self, doc):
        """Get the file corresponding to document."""

        return (self.main_file, self.tran_file)[doc]

    def get_format_class_name(self, doc):
        """Get the class name of document's file format or None."""

        if doc == cons.DOCUMENT.MAIN:
            try:
                return self.main_file.format.class_name
            except AttributeError:
                return None
        if doc == cons.DOCUMENT.TRAN:
            try:
                return self.tran_file.format.class_name
            except AttributeError:
                return self.get_format_class_name(cons.DOCUMENT.MAIN)
        raise ValueError

    def get_line_lengths(self, row, doc):
        """Get a list of line lengths in text without tags."""

        text = self.get_texts(doc)[row]
        re_tag = self.get_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return [len(x) for x in text.split("\n")]

    def get_mode(self):
        """Get the mode of the main file or default."""

        if self.main_file is not None:
            return self.main_file.mode
        return cons.MODE.TIME

    def get_positions(self, mode=None):
        """Get either times or frames depending the mode."""

        if mode is None:
            mode = self.get_mode()
        if mode == cons.MODE.TIME:
            return self.times
        if mode == cons.MODE.FRAME:
            return self.frames
        raise ValueError

    @util.ignore_exceptions(AssertionError)
    def get_tag_regex(self, doc):
        """Get the regular expression for a tag in document or None."""

        name = self.get_format_class_name(doc)
        assert name is not None
        cls = eval(name)
        assert cls.tag is not None
        return re.compile(*cls.tag)

    def get_text_length(self, row, doc):
        """Get the legth of text without tags."""

        text = self.get_texts(doc)[row]
        re_tag = self.get_tag_regex(doc)
        if re_tag is not None:
            text = re_tag.sub("", text)
        return len(text)

    def get_texts(self, doc):
        """Get the texts corresponding to document."""

        return (self.main_texts, self.tran_texts)[doc]

    @revertable
    @notify_frozen
    def insert_subtitles(
        self, rows, times, frames, main_texts, tran_texts, register=-1):
        """Insert subtitles.

        Subtitles are inserted in ascending order by simply inserting items of
        data in positions defined by items of rows. This means that the
        addition of subtitles must be taken into account beforehand in the
        'rows' argument. Data is not resorted, so this method must be called
        with ordered positions.
        """
        for i, row in enumerate(rows):
            self.times.insert(row, times[i])
            self.frames.insert(row, frames[i])
            self.main_texts.insert(row, main_texts[i])
            self.tran_texts.insert(row, tran_texts[i])

        self.register_action(
            register=register,
            docs=[cons.DOCUMENT.MAIN, cons.DOCUMENT.TRAN],
            description=_("Inserting subtitles"),
            revert_method=self.remove_subtitles,
            revert_args=[sorted(rows)],)

        self.emit("subtitles-inserted", rows)

    @revertable
    @util.ignore_exceptions(AssertionError)
    def replace_both_texts(self, rows, new_texts, register=-1):
        """Replace texts in both documents' rows with new_texts.

        rows should be a list of main rows, translation rows.
        new_texts should be a list of main texts, translation texts.
        """
        assert rows[0] or rows[1]
        main_args = [rows[0], cons.DOCUMENT.MAIN, new_texts[0]]
        tran_args = [rows[1], cons.DOCUMENT.TRAN, new_texts[1]]
        kwargs = {"register": register}
        if not rows[1]:
            return self.replace_texts(*main_args, **kwargs)
        if not rows[0]:
            return self.replace_texts(*tran_args, **kwargs)
        self.replace_texts(*main_args, **kwargs)
        self.replace_texts(*tran_args, **kwargs)
        self.group_actions(register, 2, _("Replacing texts"))

    @revertable
    @notify_frozen
    def replace_positions(self, rows, new_times, new_frames, register=-1):
        """Replace times and frames in rows with new_times and new_frames."""

        orig_times = []
        orig_frames = []
        for i, row in enumerate(rows):
            orig_times.append(self.times[row])
            orig_frames.append(self.frames[row])
            self.times[row] = new_times[i]
            self.frames[row] = new_frames[i]

        self.register_action(
            register=register,
            docs=[cons.DOCUMENT.MAIN, cons.DOCUMENT.TRAN],
            description=_("Replacing positions"),
            revert_method=self.replace_positions,
            revert_args=[rows, orig_times, orig_frames],)

        self.emit("positions-changed", rows)

    @revertable
    @notify_frozen
    def replace_texts(self, rows, doc, new_texts, register=-1):
        """Replace texts in document's rows with new_texts."""

        orig_texts = []
        texts = self.get_texts(doc)
        for i, row in enumerate(rows):
            orig_texts.append(texts[row])
            texts[row] = new_texts[i]

        self.register_action(
            register=register,
            docs=[doc],
            description=_("Replacing texts"),
            revert_method=self.replace_texts,
            revert_args=[rows, doc, orig_texts],)

        signal = ("main-texts-changed", "translation-texts-changed")[doc]
        self.emit(signal, rows)
