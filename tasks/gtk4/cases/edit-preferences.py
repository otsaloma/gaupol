"""
Edit preferences: activating should create and show the (non-modal)
preferences dialog. It is shown rather than run through run_dialog, so it is
not intercepted by the harness dialog script.
"""

def setup(application):
    pass

def verify(application):
    assert application._pref_dialog is not None
