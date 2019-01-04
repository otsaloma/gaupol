# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Data store and basic position manipulation of a single subtitle."""

import aeidon
import copy

__all__ = ("Subtitle",)


class Subtitle:

    """
    Data store and basic position manipulation of a single subtitle.

    :ivar start: Start position in native units
    :ivar start_time: Start time as string
    :ivar start_frame: Start frame as integer
    :ivar start_seconds: Start seconds as float
    :ivar end: End position in native units
    :ivar end_time: End time as string
    :ivar end_frame: End frame as integer
    :ivar end_seconds: End seconds as float
    :ivar duration: Duration in native units
    :ivar duration_time: Duration in time as string
    :ivar duration_frame: Duration in frames as integer
    :ivar duration_seconds: Duration in seconds as float
    :ivar main_text: Main text
    :ivar tran_text: Translation text
    :ivar calc: :class:`aeidon.Calculator` instance used
    :ivar framerate: :attr:`aeidon.framerates` item
    :ivar mode: :attr:`aeidon.modes` item

    Positions can be set as times, frames or seconds.
    Use :func:`aeidon.as_time`, :func:`aeidon.as_frame` or
    :func:`aeidon.as_seconds` if necessary to ensure correct type.

    Additional format-specific attributes are kept under separate containers,
    e.g. ``ssa`` for Sub Station Alpha formats, accessed as ``subtitle.ssa.*``.
    These containers are lazily created upon first use in order to avoid slow
    instantiation and excessive memory use when handling simpler formats.
    """

    def __init__(self, mode=None, framerate=None):
        """Initialize a :class:`Subtitle` instance."""
        self._start = None
        self._end = None
        self._main_text = ""
        self._tran_text = ""
        self._mode = mode or aeidon.modes.TIME
        self._framerate = framerate or aeidon.framerates.FPS_23_976
        self.calc = aeidon.Calculator(self._framerate)
        self.start = "00:00:00.000"
        self.end = "00:00:00.000"

    def __eq__(self, other):
        """Compare subtitle equality by value."""
        if not isinstance(other, Subtitle):
            raise NotImplementedError
        return (self.start == other.start and
                self.end == other.end and
                self.main_text == other.main_text and
                self.tran_text == other.tran_text and
                self.framerate == other.framerate and
                self.mode == other.mode)

    def __getattr__(self, name):
        """Return lazily instantiated format-specific attribute container."""
        if name in (x.container for x in aeidon.formats):
            # Lazily instantiate a new container.
            container = aeidon.containers.new(name)
            object.__setattr__(self, name, container)
            return container
        raise AttributeError("Invalid container name: {!r}"
                             .format(name))

    def __ge__(self, other):
        """Compare start positions."""
        if self._mode == aeidon.modes.TIME:
            return self.start_seconds >= other.start_seconds
        if self._mode == aeidon.modes.FRAME:
            return self.start_frame >= other.start_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    def __gt__(self, other):
        """Compare start positions."""
        if self._mode == aeidon.modes.TIME:
            return self.start_seconds > other.start_seconds
        if self._mode == aeidon.modes.FRAME:
            return self.start_frame > other.start_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    def __le__(self, other):
        """Compare start positions."""
        if self._mode == aeidon.modes.TIME:
            return self.start_seconds <= other.start_seconds
        if self._mode == aeidon.modes.FRAME:
            return self.start_frame <= other.start_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    def __lt__(self, other):
        """Compare start positions."""
        if self._mode == aeidon.modes.TIME:
            return self.start_seconds < other.start_seconds
        if self._mode == aeidon.modes.FRAME:
            return self.start_frame < other.start_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    def convert_framerate(self, framerate):
        """Set framerate and convert positions to it."""
        coefficient = framerate.value / self._framerate.value
        if self._mode == aeidon.modes.TIME:
            self.start_seconds = self.start_seconds / coefficient
            self.end_seconds = self.end_seconds / coefficient
        if self._mode == aeidon.modes.FRAME:
            self.start_frame = round(coefficient * self.start_frame)
            self.end_frame = round(coefficient * self.end_frame)
        self.framerate = framerate

    def _convert_position(self, value):
        """Return `value` of position in correct mode."""
        if aeidon.is_time(value):
            if self._mode == aeidon.modes.TIME:
                return value
            if self._mode == aeidon.modes.FRAME:
                return self.calc.time_to_frame(value)
        if aeidon.is_frame(value):
            if self._mode == aeidon.modes.TIME:
                return self.calc.frame_to_time(value)
            if self._mode == aeidon.modes.FRAME:
                return value
        if aeidon.is_seconds(value):
            if self._mode == aeidon.modes.TIME:
                return self.calc.seconds_to_time(value)
            if self._mode == aeidon.modes.FRAME:
                return self.calc.seconds_to_frame(value)
        raise ValueError("Invalid type for value: {!r}"
                         .format(type(value)))

    def copy(self):
        """Return a new subtitle instance with the same values."""
        subtitle = Subtitle(self._mode, self._framerate)
        subtitle._start = self._start
        subtitle._end = self._end
        subtitle._main_text = self._main_text
        subtitle._tran_text = self._tran_text
        # Copy all containers that have been instantiated.
        containers = (x.container for x in aeidon.formats)
        for name in set(dir(self)) & set(containers):
            container = copy.deepcopy(getattr(self, name))
            setattr(subtitle, name, container)
        return subtitle

    @property
    def duration(self):
        """Return duration in correct mode."""
        if self._mode == aeidon.modes.TIME:
            return self.duration_time
        if self._mode == aeidon.modes.FRAME:
            return self.duration_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    @duration.setter
    def duration(self, value):
        """Set duration from `value`."""
        value = self._convert_position(value)
        self._end = self.calc.add(self._start, value)

    @property
    def duration_frame(self):
        """Return duration as frames."""
        return self.end_frame - self.start_frame

    @duration_frame.setter
    def duration_frame(self, value):
        """Set duration from `value`."""
        self.duration = aeidon.as_frame(value)

    @property
    def duration_seconds(self):
        """Return duration as seconds."""
        return self.end_seconds - self.start_seconds

    @duration_seconds.setter
    def duration_seconds(self, value):
        """Set duration from `value`."""
        self.duration = aeidon.as_seconds(value)

    @property
    def duration_time(self):
        """Return duration as time."""
        return self.calc.seconds_to_time(self.duration_seconds)

    @duration_time.setter
    def duration_time(self, value):
        """Set duration from `value`."""
        self.duration = aeidon.as_time(value)

    @property
    def end(self):
        """Return end position in correct mode."""
        return self._end

    @end.setter
    def end(self, value):
        """Set end position from `value`."""
        self._end = self._convert_position(value)

    @property
    def end_frame(self):
        """Return end position as frames."""
        if self._mode == aeidon.modes.TIME:
            return self.calc.time_to_frame(self._end)
        if self._mode == aeidon.modes.FRAME:
            return self._end
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    @end_frame.setter
    def end_frame(self, value):
        """Set end position from `value`."""
        self.end = aeidon.as_frame(value)

    @property
    def end_seconds(self):
        """Return end position as seconds."""
        return self.calc.time_to_seconds(self.end_time)

    @end_seconds.setter
    def end_seconds(self, value):
        """Set end position from `value`."""
        self.end = aeidon.as_seconds(value)

    @property
    def end_time(self):
        """Return end position as time."""
        if self._mode == aeidon.modes.TIME:
            return self._end
        if self._mode == aeidon.modes.FRAME:
            return self.calc.frame_to_time(self._end)
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    @end_time.setter
    def end_time(self, value):
        """Set end position from `value`."""
        self.end = aeidon.as_time(value)

    @property
    def framerate(self):
        """Return framerate."""
        return self._framerate

    @framerate.setter
    def framerate(self, value):
        """Set framerate from `value`."""
        self._framerate = value
        self.calc = aeidon.Calculator(value)

    def get_duration(self, mode):
        """Return duration in `mode`."""
        if mode == aeidon.modes.TIME:
            return self.duration_time
        if mode == aeidon.modes.FRAME:
            return self.duration_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(mode))

    def get_end(self, mode):
        """Return end position in `mode`."""
        if mode == aeidon.modes.TIME:
            return self.end_time
        if mode == aeidon.modes.FRAME:
            return self.end_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(mode))

    def get_start(self, mode):
        """Return start position in `mode`."""
        if mode == aeidon.modes.TIME:
            return self.start_time
        if mode == aeidon.modes.FRAME:
            return self.start_frame
        raise ValueError("Invalid mode: {!r}"
                         .format(mode))

    def get_text(self, doc):
        """Return text corresponding to `doc`."""
        if doc == aeidon.documents.MAIN:
            return self._main_text
        if doc == aeidon.documents.TRAN:
            return self._tran_text
        raise ValueError("Invalid document: {!r}"
                         .format(doc))

    def has_container(self, name):
        """Return ``True`` if container has been instantiated."""
        return name in dir(self)

    @property
    def main_text(self):
        """Return main text."""
        return self._main_text

    @main_text.setter
    def main_text(self, value):
        """Set main text from `value`."""
        self._main_text = value

    @property
    def mode(self):
        """Return current position mode."""
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Set current position mode."""
        if mode == aeidon.modes.TIME:
            self._start = self.start_time
            self._end = self.end_time
        if mode == aeidon.modes.FRAME:
            self._start = self.start_frame
            self._end = self.end_frame
        self._mode = mode

    def scale_positions(self, value):
        """Multiply start and end positions by `value`."""
        if self._mode == aeidon.modes.TIME:
            self.start_seconds = self.start_seconds * value
            self.end_seconds = self.end_seconds * value
        if self._mode == aeidon.modes.FRAME:
            self.start_frame = round(self._start * value)
            self.end_frame = round(self._end * value)

    def set_text(self, doc, value):
        """Set text corresponding to `doc` to `value`."""
        if doc == aeidon.documents.MAIN:
            self.main_text = value
        if doc == aeidon.documents.TRAN:
            self.tran_text = value

    def shift_positions(self, value):
        """Add `value` to start and end positions."""
        self._start = self.calc.add(self._start, value)
        self._end = self.calc.add(self._end, value)

    @property
    def start(self):
        """Return start position in correct mode."""
        return self._start

    @start.setter
    def start(self, value):
        """Set start position from `value`."""
        self._start = self._convert_position(value)

    @property
    def start_frame(self):
        """Return start position as frames."""
        if self._mode == aeidon.modes.TIME:
            return self.calc.time_to_frame(self._start)
        if self._mode == aeidon.modes.FRAME:
            return self._start
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    @start_frame.setter
    def start_frame(self, value):
        """Set start position from `value`."""
        self.start = aeidon.as_frame(value)

    @property
    def start_seconds(self):
        """Return start position as seconds."""
        return self.calc.time_to_seconds(self.start_time)

    @start_seconds.setter
    def start_seconds(self, value):
        """Set start position from `value`."""
        self.start = aeidon.as_seconds(value)

    @property
    def start_time(self):
        """Return start position as time."""
        if self._mode == aeidon.modes.TIME:
            return self._start
        if self._mode == aeidon.modes.FRAME:
            return self.calc.frame_to_time(self._start)
        raise ValueError("Invalid mode: {!r}"
                         .format(self._mode))

    @start_time.setter
    def start_time(self, value):
        """Set start position from `value`."""
        self.start = aeidon.as_time(value)

    @property
    def tran_text(self):
        """Return translation text."""
        return self._tran_text

    @tran_text.setter
    def tran_text(self, value):
        """Set translation text from `value`."""
        self._tran_text = value
