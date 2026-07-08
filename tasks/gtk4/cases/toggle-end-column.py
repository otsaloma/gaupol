"""
Toggle end column: activating should flip the visibility of the end column
and update the visible-fields config accordingly.

The visible-fields config is global, so the original value is restored
afterwards to keep later cases unaffected.
"""

import gaupol

def setup(application):
    page = application.get_current_page()
    column = page.view.get_column(page.view.columns.END)
    global _visible_before, _fields_before
    _visible_before = column.get_visible()
    _fields_before = list(gaupol.conf.editor.visible_fields)

def verify(application):
    page = application.get_current_page()
    column = page.view.get_column(page.view.columns.END)
    try:
        assert column.get_visible() != _visible_before
        present = gaupol.fields.END in gaupol.conf.editor.visible_fields
        assert present != (gaupol.fields.END in _fields_before)
    finally:
        gaupol.conf.editor.visible_fields = list(_fields_before)
