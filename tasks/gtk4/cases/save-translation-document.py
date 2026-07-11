"""
Save translation document: with a translation file open (a throwaway copy
of the sample) and an unsaved translation change, saving in place should write
the translation file and clear its changed flag. No dialog appears since the
translation file already has a path and encoding.

A copy of the sample is opened as the translation so its path differs from the
already-open main file (opening the same path would be refused) and the
in-place save targets a throwaway file.
"""

import aeidon
import os
import shutil
import tempfile

def setup(application):
    page = application.get_current_page()
    global _path
    _path = os.path.join(tempfile.mkdtemp(prefix="gaupol-case-"), "translation.srt")
    shutil.copy(page.project.main_file.path, _path)
    application.open_translation(_path)
    page = application.get_current_page()
    page.project.set_text(0, aeidon.documents.TRAN, "CHANGED")

def verify(application):
    page = application.get_current_page()
    assert not page.project.tran_changed
    assert os.path.isfile(_path)
    with open(_path, encoding="utf_8") as f:
        assert "CHANGED" in f.read()
