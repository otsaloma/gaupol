"""
Shared setup helper for video action cases (not a case itself).

Loads the SMPTE color-bars sample video into the current page, pauses playback
and seeks to a fixed baseline position, so video-dependent actions run against
a ready, stationary player. `application.load_video` creates the player on
first use and sets `player.ready` synchronously via a discoverer.
"""

import gaupol
import os

from gi.repository import GLib

VIDEO = os.path.abspath(os.path.join(
    os.path.dirname(gaupol.__file__), "..", "data", "samples", "video.mp4"))

BASELINE = 10.0

def load_video(application, position=BASELINE):
    """Load the sample video, pause, and seek to `position` seconds."""
    application.load_video(VIDEO)
    application.player_box.set_visible(True)
    player = application.player
    player.pause()
    player.seek(position)
    # Iterate the default main context so the pause and seek settle before
    # the case queries the player position.
    context = GLib.MainContext.default()
    for i in range(200):
        while context.pending():
            context.iteration(False)
    return player
