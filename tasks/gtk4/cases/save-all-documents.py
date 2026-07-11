"""
Save all documents: with an unsaved change in the single open project,
saving all should write the main file in place and clear the changed flag. The
project has no translation, so no save-as dialog is triggered.

The main file is redirected to a throwaway path in setup so the in-place save
does not overwrite the repository sample.
"""

import aeidon
import os
import tempfile

def setup(application):
    page = application.get_current_page()
    global _path
    _path = os.path.join(tempfile.mkdtemp(prefix="gaupol-case-"), "saved.srt")
    page.project.main_file.path = _path
    page.project.set_text(0, aeidon.documents.MAIN, "CHANGED")

def verify(application):
    page = application.get_current_page()
    assert not page.project.main_changed
    assert os.path.isfile(_path)
    with open(_path, encoding="utf_8") as f:
        assert "CHANGED" in f.read()
