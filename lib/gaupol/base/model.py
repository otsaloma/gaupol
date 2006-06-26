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


"""Base class for models."""


class Model(object):

    """
    Base class for models.

    Class variables:

        _signals: List of signals

    Instance variables:

        _notifications:   Dictionary mapping signals to callback methods
        _blocked_signals: List of signals currently blocked

    Model is meant in the sense of model in Model/View/Controller design.
    Model's purpose is to contain the data edited by the application and send
    signals to the user interface when the data is changed.

    For an instance to be informed of changes, it needs to connect to a signal
    using the 'connect' method. When the model emits a signal, the provided
    method will be called.
    """

    _signals = []

    def __init__(self):

        self._notifications = {}
        self._blocked_signals = []

        for signal in self._signals:
            self._notifications[signal] = []

    def block(self, signal):
        """Block all emissions of signal."""

        if not signal in self._blocked_signals:
            self._blocked_signals.append(signal)

    def connect(self, signal, method):
        """Register to receive notifications of signal."""

        if not method in self._notifications[signal]:
            self._notifications[signal].append(method)

    def emit(self, signal, *args, **kwargs):
        """Send notification of signal to all registered observers."""

        if signal in self._blocked_signals:
            return

        for method in self._notifications[signal]:
            method(*args, **kwargs)

    def unblock(self, signal):
        """Unblock all emissions of signal."""

        try:
            self._blocked_signals.remove(signal)
        except ValueError:
            pass
