Gaupol
======

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/gaupol)

Gaupol is an editor for text-based subtitle files. It supports multiple
subtitle file formats and provides means of creating, editing and
translating subtitles and timing subtitles to match video.

Gaupol also contains Aeidon, a separately installable general-purpose
Python package for reading, writing and manipulating text-based subtitle
files. See the file `README.aeidon.md` for details.

Gaupol is free software released under the GNU General Public License
(GPL), see the file `COPYING` for details.

Dependencies
============

Gaupol requires [Python](https://www.python.org/) 3.2 or greater,
[PyGObject](https://wiki.gnome.org/Projects/PyGObject) 3.6.0 or greater
and [GTK+](http://www.gtk.org/) 3.12 or greater. Optional, but strongly
recommended dependencies include:

 * [GStreamer](https://gstreamer.freedesktop.org/) 1.0 or greater (at
   least the core, gst-plugins-base and gst-plugins-good; and for good
   container and codec support preferrably each of gst-plugins-bad,
   gst-plugins-ugly and gst-libav) – required for the integrated video
   player

 * [PyEnchant](http://pythonhosted.org/pyenchant/) 1.4.0 or greater –
   required for spell-checking

 * [GtkSpell](http://gtkspell.sourceforge.net/) 3.0.0 or greater –
   required for inline spell-checking

 * [iso-codes](http://pkg-isocodes.alioth.debian.org/) – required to
   translate language and country names

 * [Universal Encoding Detector](https://pypi.python.org/pypi/chardet)
   (a.k.a. chardet) – required for character encoding auto-detection

 * [mpv](https://mpv.io/), [MPlayer](http://www.mplayerhq.hu/) or
   [VLC](http://www.videolan.org/vlc/) – recommended for preview

Running
=======

To try Gaupol from the source directory without installation, use
command `bin/gaupol`. For installing Gaupol, see the file `INSTALL.md`.
