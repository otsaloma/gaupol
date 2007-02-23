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


"""Base class for observable objects."""


import functools

from ._mutables import ObservableDict, ObservableList, ObservableSet


def notify_frozen(function):
    """Decorator for methods to be run in notify frozen state."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        changed = args[0].freeze_notify()
        value = function(*args, **kwargs)
        args[0].thaw_notify(changed)
        return value

    return wrapper


class Observable(object):

    """Base class for observable objects.

    Class variables:

        _signals: List of emittable signals added automatically

    Instance variables:

        _blocked_signals: List of blocked signals
        _notify_frozen:   If True notify signals will be queued, not emitted
        _notify_queue:    List of queued notify signals
        _signal_handlers: Dictionary mapping signals to observers and data

    In addition to the signals defined in '_signals', all public instance
    variables will have a 'notify::name' signal generated automatically based
    on the name of the variable. 'notify::name' signals will be emitted
    whenever the value of the instance variable changes.

    Notify signals will be emitted for mutable variables as well, which means
    care should be taken not to emit thousands of signals when appending
    one-by-one to a large list. 'freeze_notify' and 'thaw_notify' methods as
    well as the 'notify_frozen' decorator will queue notify signals and emit
    only one of each once thawed.
    """

    # The Observable philosophy and API is highly inspired by (Py)GObject.
    # http://www.pygtk.org/docs/pygobject/class-gobject.html

    __slots__ = [
        "_blocked_signals",
        "_notify_frozen",
        "_notify_queue",
        "_signal_handlers",]

    _signals = []

    def __init__(self):

        self._blocked_signals = []
        self._notify_frozen   = False
        self._notify_queue    = []
        self._signal_handlers = {}

        for signal in self._signals:
            self._add_signal(signal)

    def __setattr__(self, name, value):

        if name in self.__slots__ or name.startswith("_"):
            return object.__setattr__(self, name, value)
        value = self._validate(name, value)
        signal = "notify::%s" % name
        if not signal in self._signal_handlers:
            self._add_signal(signal)
            return object.__setattr__(self, name, value)
        return_value = object.__setattr__(self, name, value)
        self.emit(signal, value)
        return return_value

    def _add_signal(self, signal):
        """Add signal to the list of signals."""

        if signal in self._signal_handlers:
            raise ValueError
        self._signal_handlers[signal] = []

    def _validate(self, name, value):
        """Return value or an observable version of mutable value."""

        if isinstance(value, dict):
            return ObservableDict(value, self, name)
        if isinstance(value, list):
            return ObservableList(value, self, name)
        if isinstance(value, set):
            return ObservableSet(value, self, name)
        return value

    def block(self, signal):
        """Block all emissions of signal.

        Return False if already blocked, otherwise True.
        """
        if not signal in self._blocked_signals:
            self._blocked_signals.append(signal)
            return True
        return False

    def connect(self, signal, method, *args):
        """Register to receive notifications of signal."""

        self._signal_handlers[signal].append((method, args))

    def disconnect(self, signal, method):
        """Remove registration to receive notifications of signal."""

        for i in reversed(range(len(self._signal_handlers[signal]))):
            if self._signal_handlers[signal][i][0] == method:
                self._signal_handlers[signal].pop(i)

    def emit(self, signal, *args):
        """Send notification of signal to all registered observers."""

        if signal.startswith("notify::") and self._notify_frozen:
            if signal not in self._notify_queue:
                self._notify_queue.append(signal)
            return

        if not signal in self._blocked_signals:
            # FIX: REMOVE WHEN NO EXCESSIVE SIGNALS EMITTED.
            print "%s.%s" % (self.__class__.__name__, signal)
            if signal.startswith("notify::"):
                name = signal.replace("notify::", "")
                args = (getattr(self, name),)
            for method, data in self._signal_handlers[signal]:
                method(*((self,) + args + data))

    def freeze_notify(self):
        """Queue notify signals instead of emitting them.

        Return False if already frozen, otherwise True.
        """
        if not self._notify_frozen:
            self._notify_frozen = True
            return True
        return False

    def notify(self, name):
        """Emit notification signal for variable."""

        return self.emit("notify::%s" % name)

    def thaw_notify(self, do=True):
        """Emit all queued notify signals and queue no more.

        The optional 'do' keyword argument should be the return value from
        'freeze_notify' to avoid problems with nested functions where
        notifications were frozen at a higher level. If 'do' is False, nothing
        will be done.
        Return False if already thawed, otherwise True.
        """
        if do and self._notify_frozen:
            self._notify_frozen = False
            for signal in self._notify_queue:
                name = signal.replace("notify::", "")
                self.emit(signal, getattr(self, name))
            self._notify_queue = []
            return True
        return False

    def unblock(self, signal, do=True):
        """Unblock all emissions of signal.

        The optional 'do' keyword argument should be the return value from
        'block' to avoid problems with nested functions where notifications
        were frozen at a higher level. If 'do' is False, nothing will be done.
        Return False if already unblocked, otherwise True.
        """
        if do and (signal in self._blocked_signals):
            self._blocked_signals.remove(signal)
            return True
        return False
