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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""User-activatable actions for :class:`gaupol.Application`."""

from gaupol.actions import audio
from gaupol.actions import edit
from gaupol.actions import file
from gaupol.actions import help
from gaupol.actions import projects
from gaupol.actions import text
from gaupol.actions import tools
from gaupol.actions import video
from gaupol.actions import view

classes = (
    audio.SetAudioLanguageAction,
    audio.VolumeDownAction,
    audio.VolumeUpAction,
    edit.EditPreferencesAction,
    edit.EditNextValueAction,
    edit.EditValueAction,
    edit.EndEarlierAction,
    edit.EndLaterAction,
    edit.ExtendSelectionToBeginningAction,
    edit.ExtendSelectionToEndAction,
    edit.InsertSubtitleAtVideoPositionAction,
    edit.InsertSubtitlesAction,
    edit.InvertSelectionAction,
    edit.MergeSubtitlesAction,
    edit.RedoActionAction,
    edit.RemoveSubtitlesAction,
    edit.SelectAllAction,
    edit.SelectNextFromVideoPositionAction,
    edit.SelectPreviousFromVideoPositionAction,
    edit.SetEndFromVideoPositionAction,
    edit.SetStartFromVideoPositionAction,
    edit.SplitSubtitleAction,
    edit.StartEarlierAction,
    edit.StartLaterAction,
    edit.UndoActionAction,
    file.CloseProjectAction,
    file.NewProjectAction,
    file.OpenMainFilesAction,
    file.OpenTranslationFileAction,
    file.QuitAction,
    file.SaveMainDocumentAction,
    file.SaveMainDocumentAsAction,
    file.SaveTranslationDocumentAction,
    file.SaveTranslationDocumentAsAction,
    help.BrowseDocumentationAction,
    help.ReportABugAction,
    help.ViewAboutDialogAction,
    projects.ActivateNextProjectAction,
    projects.ActivatePreviousProjectAction,
    projects.ActivateProjectAction,
    projects.CloseAllProjectsAction,
    projects.SaveAllDocumentsAction,
    projects.SaveAllDocumentsAsAction,
    text.ClearTextsAction,
    text.CopyTextsAction,
    text.CutTextsAction,
    text.FindAndReplaceAction,
    text.FindNextAction,
    text.FindPreviousAction,
    text.PasteTextsAction,
    text.ToggleDialogDashesAction,
    text.ToggleItalicizationAction,
    text.UseLowerCaseAction,
    text.UseSentenceCaseAction,
    text.UseTitleCaseAction,
    text.UseUpperCaseAction,
    tools.AdjustDurationsAction,
    tools.AppendFileAction,
    tools.CheckSpellingAction,
    tools.ConfigureSpellCheckAction,
    tools.ConvertFramerateAction,
    tools.CorrectTextsAction,
    tools.PreviewAction,
    tools.SelectVideoFileAction,
    tools.ShiftPositionsAction,
    tools.SplitProjectAction,
    tools.TransformPositionsAction,
    video.LoadVideoAction,
    video.PlayPauseAction,
    video.PlaySelectionAction,
    video.SeekBackwardAction,
    video.SeekForwardAction,
    video.SeekNextAction,
    video.SeekPreviousAction,
    video.SeekSelectionEndAction,
    video.SeekSelectionStartAction,
    view.SetEditModeAction,
    view.SetFramerateAction,
    view.SetLayoutAction,
    view.ToggleDurationColumnAction,
    view.ToggleEndColumnAction,
    view.ToggleMainTextColumnAction,
    view.ToggleNumberColumnAction,
    view.TogglePlayerAction,
    view.ToggleStartColumnAction,
    view.ToggleTranslationTextColumnAction,
)
