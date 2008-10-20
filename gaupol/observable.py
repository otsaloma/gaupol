# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Base class for observable objects."""

import gaupol

__all__ = ("Observable",)


class Observable(object):

    """Base class for observable objects.

    Class variables:
     * _signals: Tuple of emittable signals added automatically

    Instance variables:
     * _blocked_signals: List of blocked signals
     * _blocked_state: True if all signals are blocked
     * _notify_frozen: If True notify signals will be queued, not emitted
     * _notify_queue: List of queued notify signals
     * _signal_handlers: Dictionary mapping signals to observers and data

    In addition to the signals defined in '_signals', all public instance
    variables will have a 'notify::name' signal generated automatically based
    on the name of the variable. 'notify::name' signals will be emitted
    whenever the value of the instance variable changes.

    Notify signals will be emitted for mutable variables as well, which means
    that care should be taken not to emit thousands of signals when appending
    one-by-one to a large list. 'freeze_notify' and 'thaw_notify' methods will
    queue notify signals and emit only one of each once thawed.
    """

    # The Observable philosophy and API is highly inspired by (Py)GObject.
    # <http://www.pygtk.org/docs/pygobject/class-gobject.html>

    __metaclass__ = gaupol.Contractual

    __slots__ = (
        "_blocked_signals",
        "_blocked_state",
        "_notify_frozen",
        "_notify_queue",
        "_signal_handlers",)

    _signals = ()

    def __init__(self):

        self._blocked_signals = []
        self._blocked_state = False
        self._notify_frozen = False
        self._notify_queue = []
        self._signal_handlers = {}

        for signal in self._signals:
            self._add_signal(signal)

    def __setattr__(self, name, value):

        if (name in self.__slots__) or name.startswith("_"):
            return object.__setattr__(self, name, value)
        value = self._validate(name, value)
        signal = "notify::%s" % name
        if not signal in self._signal_handlers:
            self._add_signal(signal)
            return object.__setattr__(self, name, value)
        return_value = object.__setattr__(self, name, value)
        self.emit(signal, value)
        return return_value

    def _add_signal_require(self, signal):
        assert not signal in self._signal_handlers

    def _add_signal(self, signal):
        """Add signal to the list of signals."""

        self._signal_handlers[signal] = []

    def _validate_ensure(self, return_value, name, value):
        assert return_value == value

    def _validate(self, name, value):
        """Return value or an observable version of mutable value."""

        args = (value, self, name)
        if isinstance(value, dict):
            return gaupol.ObservableDict(*args)
        if isinstance(value, list):
            return gaupol.ObservableList(*args)
        if isinstance(value, set):
            return gaupol.ObservableSet(*args)
        return value

    def block_require(self, signal):
        assert signal in self._signal_handlers

    def block(self, signal):
        """Block all emissions of signal.

        Return False if already blocked, otherwise True.
        """
        if not signal in self._blocked_signals:
            self._blocked_signals.append(signal)
            return True
        return False

    def block_all(self):
        """Block all emissions of all signals.

        Return False if already blocked, otherwise True.
        """
        if not self._blocked_state:
            self._blocked_state = True
            return True
        return False

    def connect_require(self, signal, method, *args):
        assert signal in self._signal_handlers
        assert callable(method)

    def connect(self, signal, method, *args):
        """Register to receive notifications of signal."""

        self._signal_handlers[signal].append((method, args))

    def disconnect_require(self, signal, method):
        assert signal in self._signal_handlers

    def disconnect(self, signal, method):
        """Remove registration to receive notifications of signal."""

        for i in reversed(range(len(self._signal_handlers[signal]))):
            if self._signal_handlers[signal][i][0] == method:
                self._signal_handlers[signal].pop(i)

    def emit_require(self, signal, *args):
        assert signal in self._signal_handlers

    def emit(self, signal, *args):
        """Send notification of signal to all registered observers."""

        if signal.startswith("notify::") and self._notify_frozen:
            if not signal in self._notify_queue:
                self._notify_queue.append(signal)
            return

        if (not self._blocked_state) and (not signal in self._blocked_signals):
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

    def notify_require(self, name):
        assert hasattr(self, name)

    def notify(self, name):
        """Emit notification signal for variable."""

        return self.emit("notify::%s" % name)

    def thaw_notify_ensure(self, value, do=True):
        assert (not do) or (not self._notify_queue)

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

    def unblock_require(self, signal, do=True):
        assert signal in self._signal_handlers

    def unblock(self, signal, do=True):
        """Unblock all emissions of signal.

        The optional 'do' keyword argument should be the return value from
        'block' to avoid problems with nested functions where signals were
        blocked at a higher level. If 'do' is False, nothing will be done.
        Return False if already unblocked, otherwise True.
        """
        if do and (signal in self._blocked_signals):
            self._blocked_signals.remove(signal)
            return True
        return False

    def unblock_all(self, do=True):
        """Unblock all emissions of all signals.

        The optional 'do' keyword argument should be the return value from
        'block_all' to avoid problems with nested functions where signals were
        blocked at a higher level. If 'do' is False, nothing will be done.
        Return False if already unblocked, otherwise True.
        """
        if do and self._blocked_state:
            self._blocked_state = False
            return True
        return False
