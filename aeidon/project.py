# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Model for subtitle data."""

import aeidon

__all__ = ("Project",)


class ProjectMeta(type):

    """
    Project metaclass with delegated methods added.

    Public methods are added to the class dictionary during :meth:`__new__`
    in order to fool Sphinx (and perhaps other API documentation generators)
    into thinking that the resulting instantiated class actually contains those
    methods, which it does not since the methods are removed during
    :meth:`Project.__init__`.
    """

    def __new__(meta, class_name, bases, dic):
        new_dict = dic.copy()
        for agent_class_name in aeidon.agents.__all__:
            agent_class = getattr(aeidon.agents, agent_class_name)
            def is_delegate_method(name):
                value = getattr(agent_class, name)
                return (callable(value) and
                        hasattr(value, "export") and
                        value.export is True)

            attr_names = list(filter(is_delegate_method, dir(agent_class)))
            for attr_name in attr_names:
                new_dict[attr_name] = getattr(agent_class, attr_name)
        return type.__new__(meta, class_name, bases, new_dict)


class Project(aeidon.Observable, metaclass=ProjectMeta):

    """
    Model for subtitle data.

    :ivar calc: Instance of :class:`aeidon.Calculator` used
    :ivar clipboard: Instance of :class:`aeidon.Clipboard` used
    :ivar _delegations: Dictionary mapping method names to agent methods
    :ivar framerate: :attr:`aeidon.framerates` item corresponding to video
    :ivar main_changed: Integer, status of main document

       At unchanged state (i.e. file on disk corresponds to the state of the
       document) this value is zero. Doing and redoing increase the value by
       one and undoing decreases value by one.

    :ivar main_file: Main instance of :class:`aeidon.SubtitleFile`
    :ivar redoables: Stack of :class:`aeidon.RevertableAction` instances
    :ivar subtitles: List of :class:`aeidon.Subtitle` instances
    :ivar tran_changed: Integer, status of translation document

       At unchanged state (i.e. file on disk corresponds to the state of the
       document) this value is zero. Doing and redoing increase the value by
       one  and undoing decreases value by one.

    :ivar tran_file: Translation instance of :class:`aeidon.SubtitleFile`
    :ivar undo_limit: Maximum size of undo/redo stacks or None for no limit
    :ivar undoables: Stack of :class:`aeidon.RevertableAction` instances
    :ivar video_path: Full, absolute path to the video file on disk

    Signals and their arguments for callback functions:
     * ``action-done``: project, action
     * ``action-redone``: project, action
     * ``action-undone``: project, action
     * ``main-file-opened``: project, main_file
     * ``main-file-saved``: project, main_file
     * ``main-texts-changed``: project, indices
     * ``positions-changed``: project, indices
     * ``subtitles-changed``: project, indices
     * ``subtitles-inserted``: project, indices
     * ``subtitles-removed``: project, indices
     * ``translation-file-opened``: project, tran_file
     * ``translation-file-saved``: project, tran_file
     * ``translation-texts-changed``: project, indices
    """

    signals = (
        "action-done",
        "action-redone",
        "action-undone",
        "main-file-opened",
        "main-file-saved",
        "main-texts-changed",
        "positions-changed",
        "subtitles-inserted",
        "subtitles-removed",
        "subtitles-changed",
        "translation-file-opened",
        "translation-file-saved",
        "translation-texts-changed",
    )

    def __init__(self, framerate=None):
        """Initialize a :class:`Project` instance."""
        aeidon.Observable.__init__(self)
        framerate = framerate or aeidon.framerates.FPS_23_976
        self.calc = aeidon.Calculator(framerate)
        self.clipboard = aeidon.Clipboard()
        self._delegations = {}
        self.framerate = framerate
        self.main_changed = 0
        self.main_file = None
        self.redoables = []
        self.subtitles = []
        self.tran_changed = None
        self.tran_file = None
        self.undo_limit = 100000
        self.undoables = []
        self.video_path = None
        self._init_delegations()

    def __getattr__(self, name):
        """Return method delegated to an agent."""
        try:
            return self._delegations[name]
        except LookupError:
            raise AttributeError

    def _init_delegations(self):
        """Initialize the delegation mappings."""
        for agent_class_name in aeidon.agents.__all__:
            agent = getattr(aeidon.agents, agent_class_name)(self)
            def is_delegate_method(name):
                value = getattr(agent, name)
                return (callable(value) and
                        hasattr(value, "export") and
                        value.export is True)

            attr_names = list(filter(is_delegate_method, dir(agent)))
            for attr_name in attr_names:
                attr_value = getattr(agent, attr_name)
                if attr_name in self._delegations:
                    raise ValueError("Multiple definitions of {!r}"
                                     .format(attr_name))

                self._delegations[attr_name] = attr_value
                # Remove class-level function added by ProjectMeta.
                if hasattr(self.__class__, attr_name):
                    delattr(self.__class__, attr_name)
