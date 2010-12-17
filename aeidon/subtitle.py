# Copyright (C) 2007-2009 Osmo Salomaa
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

"""Data store and basic position manipulation of a single subtitle."""

import aeidon
import copy

__all__ = ("Subtitle",)


class Subtitle(object):

    """Data store and basic position manipulation of a single subtitle.

    :ivar start: Start position in native units (read/write)
    :ivar start_time: Start time as string (read)
    :ivar start_frame: Start frame as integer (read)
    :ivar start_seconds: Start seconds as float (read)
    :ivar end: End position in native units (read/write)
    :ivar end_time: End time as string (read)
    :ivar end_frame: End frame as integer (read)
    :ivar end_seconds: End seconds as float (read)
    :ivar duration: Duration in native units (read/write)
    :ivar duration_time: Duration in time as string (read)
    :ivar duration_frame: Duration in frames as integer (read)
    :ivar duration_seconds: Duration in seconds as float (read)
    :ivar main_text: Main text (read/write)
    :ivar tran_text: Translation text (read/write)
    :ivar calc: :class:`aeidon.Calculator` instance used (read/write)
    :ivar framerate: :attr:`aeidon.framerates` item (read/write)
    :ivar mode: :attr:`aeidon.modes` item (read/write)

    Positions can be set as strings for times, integers for frames or floats
    for seconds. Positions are saved internally in only one mode.

    Additional format-specific attributes are kept under separate containers,
    e.g. ``ssa`` for Sub Station Alpha formats, accessed as ``subtitle.ssa.*``.
    These containers are lazily created upon first use in order to avoid slow
    instantiation and excessive memory use when handling simpler formats.
    """

    def __cmp__(self, other):
        """Compare start positions in this subtitle's mode.

        Return 1 if this subtitle appears later, 0 if they appear at the same
        time and -1 if `other` appears later.
        """
        if self._mode == aeidon.modes.TIME:
            times = (self._start, other.start_time)
            return self.calc.compare_times(*times)
        if self._mode == aeidon.modes.FRAME:
            return cmp(self._start, other.start_frame)
        raise ValueError("Invalid mode: %s" % repr(self._mode))

    def __getattr__(self, name):
        """Return lazily instantiated format-specific attribute container."""
        if name in (x.container for x in aeidon.formats):
            # Lazily instantiate a new container.
            container = aeidon.containers.new(name)
            object.__setattr__(self, name, container)
            return container
        raise AttributeError("Invalid container name: %s" % repr(name))

    def __init__(self, mode=None, framerate=None):
        """Initialize a :class:`Subtitle` object."""
        self._start = "00:00:00.000"
        self._end = "00:00:00.000"
        self._main_text = ""
        self._tran_text = ""
        self._mode = mode or aeidon.modes.TIME
        self._framerate = framerate or aeidon.framerates.FPS_23_976
        self.calc = aeidon.Calculator(self._framerate)

    def _convert_position(self, value):
        """Return `value` of position in correct mode."""
        if isinstance(value, basestring):
            if self._mode == aeidon.modes.TIME:
                return value
            if self._mode == aeidon.modes.FRAME:
                return self.calc.time_to_frame(value)
        if isinstance(value, int):
            if self._mode == aeidon.modes.TIME:
                return self.calc.frame_to_time(value)
            if self._mode == aeidon.modes.FRAME:
                return value
        if isinstance(value, float):
            if self._mode == aeidon.modes.TIME:
                return self.calc.seconds_to_time(value)
            if self._mode == aeidon.modes.FRAME:
                return self.calc.seconds_to_frame(value)
        raise ValueError("Invalid type for value: %s" % repr(type(value)))

    def convert_framerate(self, framerate):
        """Set framerate and convert positions to it."""
        coefficient = framerate.value / self._framerate.value
        self.framerate = framerate
        if self._mode == aeidon.modes.TIME:
            self.start = self.start_seconds / coefficient
            self.end = self.end_seconds / coefficient
        if self._mode == aeidon.modes.FRAME:
            self.start = int(round(coefficient * self.start_frame, 0))
            self.end = int(round(coefficient * self.end_frame, 0))

    def copy(self):
        """Return a new subtitle instance with the same values."""
        subtitle = Subtitle(self._mode, self._framerate)
        subtitle._start = self._start
        subtitle._end = self._end
        subtitle._main_text = self._main_text
        subtitle._tran_text = self._tran_text
        # Copy all containers that have been instantiated.
        containers = (x.container for x in aeidon.formats)
        for name in (set(dir(self)) & set(containers)):
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
        raise ValueError("Invalid mode: %s" % repr(self._mode))

    @duration.setter
    def duration(self, value):
        """Set duration from `value`."""
        value = self._convert_position(value)
        if self._mode == aeidon.modes.TIME:
            times = (self.start_time, value)
            self._end = self.calc.add_times(*times)
        if self._mode == aeidon.modes.FRAME:
            self._end = self.start_frame + value

    @property
    def duration_frame(self):
        """Return duration as frames."""
        bounds = (self.start_frame, self.end_frame)
        return self.calc.get_frame_duration(*bounds)

    @property
    def duration_seconds(self):
        """Return duration as seconds."""
        time = self.duration_time
        return self.calc.time_to_seconds(time)

    @property
    def duration_time(self):
        """Return duration as time."""
        bounds = (self.start_time, self.end_time)
        return self.calc.get_time_duration(*bounds)

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
        raise ValueError("Invalid mode: %s" % repr(self._mode))

    @property
    def end_seconds(self):
        """Return end position as seconds."""
        time = self.end_time
        return self.calc.time_to_seconds(time)

    @property
    def end_time(self):
        """Return end position as time."""
        if self._mode == aeidon.modes.TIME:
            return self._end
        if self._mode == aeidon.modes.FRAME:
            return self.calc.frame_to_time(self._end)
        raise ValueError("Invalid mode: %s" % repr(self._mode))

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
        raise ValueError("Invalid mode: %s" % repr(mode))

    def get_end(self, mode):
        """Return end position in `mode`."""
        if mode == aeidon.modes.TIME:
            return self.end_time
        if mode == aeidon.modes.FRAME:
            return self.end_frame
        raise ValueError("Invalid mode: %s" % repr(mode))

    def get_start(self, mode):
        """Return start position in `mode`."""
        if mode == aeidon.modes.TIME:
            return self.start_time
        if mode == aeidon.modes.FRAME:
            return self.start_frame
        raise ValueError("Invalid mode: %s" % repr(mode))

    def get_text(self, doc):
        """Return text corresponding to `doc`."""
        if doc == aeidon.documents.MAIN:
            return self._main_text
        if doc == aeidon.documents.TRAN:
            return self._tran_text
        raise ValueError("Invalid document: %s" % repr(doc))

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
        self._main_text = unicode(value)

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
            self.start = self.start_seconds * value
            self.end = self.end_seconds * value
        if self._mode == aeidon.modes.FRAME:
            self.start = int(round(self._start * value, 0))
            self.end = int(round(self._end * value, 0))

    def set_text(self, doc, value):
        """Set text corresponding to `doc` to `value`."""
        if doc == aeidon.documents.MAIN:
            self.main_text = value
        if doc == aeidon.documents.TRAN:
            self.tran_text = value

    def shift_positions(self, value):
        """Add `value` to start and end positions."""
        if isinstance(value, basestring):
            start = self.calc.add_times(self.start_time, value)
            end = self.calc.add_times(self.end_time, value)
            self.start = start
            self.end = end
        elif isinstance(value, int):
            start = self.start_frame + value
            end = self.end_frame + value
            self.start = start
            self.end = end
        elif isinstance(value, float):
            start = self.start_seconds + value
            end = self.end_seconds + value
            self.start = start
            self.end = end

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
        raise ValueError("Invalid mode: %s" % repr(self._mode))

    @property
    def start_seconds(self):
        """Return start position as seconds."""
        time = self.start_time
        return self.calc.time_to_seconds(time)

    @property
    def start_time(self):
        """Return start position as time."""
        if self._mode == aeidon.modes.TIME:
            return self._start
        if self._mode == aeidon.modes.FRAME:
            return self.calc.frame_to_time(self._start)
        raise ValueError("Invalid mode: %s" % repr(self._mode))

    @property
    def tran_text(self):
        """Return translation text."""
        return self._tran_text

    @tran_text.setter
    def tran_text(self, value):
        """Set translation text from `value`."""
        self._tran_text = unicode(value)
