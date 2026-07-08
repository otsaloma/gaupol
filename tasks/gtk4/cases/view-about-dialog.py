"""
View about dialog: activating should create and present the about dialog.
Under GTK 4 it derives from GtkWindow and is presented (not run through
run_dialog), so it is not intercepted by the harness dialog script.
"""

def setup(application):
    pass

def verify(application):
    assert application._about_dialog is not None
