"""
Close project: closing the single (unmodified) project should leave no
pages open. An unmodified document needs no save confirmation, so no dialog
appears.
"""

def setup(application):
    pass

def verify(application):
    assert len(application.pages) == 0
