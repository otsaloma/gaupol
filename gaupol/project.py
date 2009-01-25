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

"""Model for subtitle data."""

import gaupol

__all__ = ("Project",)


class Project(gaupol.Observable):

    """Model for subtitle data.

    Instance variables:
     * _delegations: Dictionary mapping method names to agent methods
     * calc: Position calculator
     * clipboard: Internal subtitle text clipboard
     * framerate: Framerate enumeration of the video file
     * main_changed: Integer, status of main document
     * main_file: Main subtitle file
     * redoables: Stack of redoable actions
     * subtitles: List of subtitles
     * tran_changed: Status of the translation document or None if inactive
     * tran_file: Translation subtitle file
     * undo_limit: Maximum size of undo/redo stacks or None for no limit
     * undoables: Stack of undoable actions
     * video_path: Path to the video file or None

    Signals (arguments):
     * action-done (project, action)
     * action-redone (project, action)
     * action-undone (project, action)
     * main-file-opened (project, main_file)
     * main-file-saved (project, main_file)
     * main-texts-changed (project, indices)
     * positions-changed (project, indices)
     * preview-started (project, video_path, sub_path, output_path)
     * subtitles-changed (project, indices)
     * subtitles-inserted (project, indices)
     * subtitles-removed (project, indices)
     * translation-file-opened (project, tran_file)
     * translation-file-saved (project, tran_file)
     * translation-texts-changed (project, indices)

    See gaupol.agents for project methods provided by agents.
    """

    __metaclass__ = gaupol.Contractual

    _signals = (
        "action-done",
        "action-redone",
        "action-undone",
        "main-file-opened",
        "main-file-saved",
        "main-texts-changed",
        "positions-changed",
        "preview-started",
        "subtitles-inserted",
        "subtitles-removed",
        "subtitles-changed",
        "translation-file-opened",
        "translation-file-saved",
        "translation-texts-changed",)

    def __getattr__(self, name):
        """Return methods delegated to an agent."""

        return self._delegations[name]

    def __init__(self, framerate=None, undo_limit=None):
        """Initialize a Project object."""

        gaupol.Observable.__init__(self)
        framerate = framerate or gaupol.framerates.FPS_24
        self._delegations = {}
        self.calc = gaupol.Calculator(framerate)
        self.clipboard = gaupol.Clipboard()
        self.framerate = framerate
        self.main_changed = 0
        self.main_file = None
        self.redoables = []
        self.subtitles = []
        self.tran_changed = None
        self.tran_file = None
        self.undo_limit = undo_limit
        self.undoables = []
        self.video_path = None

        self._init_delegations()

    def _init_delegations(self):
        """Initialize the delegation mappings."""

        for agent_class_name in gaupol.agents.__all__:
            agent = getattr(gaupol.agents, agent_class_name)(self)
            def is_delegate_method(name):
                if name.startswith("_"): return False
                return callable(getattr(agent, name))
            attr_names = filter(is_delegate_method, dir(agent))
            for attr_name in attr_names:
                attr_value = getattr(agent, attr_name)
                if attr_name in self._delegations:
                    raise ValueError("Agents overlap")
                self._delegations[attr_name] = attr_value
