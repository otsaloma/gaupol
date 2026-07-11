"""
Toggle duration column: activating should flip the visibility of the
duration column and update the visible-fields config accordingly.

The visible-fields config is global, so the original value is restored
afterwards to keep later cases unaffected.
"""

import gaupol

def setup(application):
    page = application.get_current_page()
    column = page.view.get_column(page.view.columns.DURATION)
    global _visible_before, _fields_before
    _visible_before = column.get_visible()
    _fields_before = list(gaupol.conf.editor.visible_fields)

def verify(application):
    page = application.get_current_page()
    column = page.view.get_column(page.view.columns.DURATION)
    try:
        assert column.get_visible() != _visible_before
        present = gaupol.fields.DURATION in gaupol.conf.editor.visible_fields
        assert present != (gaupol.fields.DURATION in _fields_before)
    finally:
        gaupol.conf.editor.visible_fields = list(_fields_before)
