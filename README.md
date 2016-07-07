Gaupol
======

[![Build Status](https://travis-ci.org/otsaloma/gaupol.svg)](https://travis-ci.org/otsaloma/gaupol)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/gaupol)

Gaupol is an editor for text-based subtitle files. It supports multiple
subtitle file formats and provides means of creating, editing and
translating subtitles and timing subtitles to match video.

The Gaupol source tree includes `aeidon`, a separately installable
general-purpose Python package for reading, writing and manipulating
text-based subtitle files. See the file `README.aeidon.md` for details.

Gaupol is free software released under the GNU General Public License
(GPL), see the file `COPYING` for details.

Dependencies
============

Gaupol requires [Python](https://www.python.org/) ≥ 3.2,
[PyGObject](https://wiki.gnome.org/Projects/PyGObject) ≥ 3.12 and
[GTK+](http://www.gtk.org/) ≥ 3.12. Optional, but strongly recommended
dependencies include:

| Dependency | Version | Required for |
| :--------- | :------ | :----------- |
| [GStreamer](https://gstreamer.freedesktop.org/) | ≥ 1.0 | integrated video player |
| [PyEnchant](http://pythonhosted.org/pyenchant/) | ≥ 1.4.0 | spell-check |
| [GtkSpell](http://gtkspell.sourceforge.net/) | ≥ 3.0.0 | inline spell-check |
| [iso-codes](http://pkg-isocodes.alioth.debian.org/) | any | translations |
| [chardet](https://pypi.python.org/pypi/chardet) | any | character encoding auto-detection |

From GStreamer you need at least the core, gst-plugins-base and
gst-plugins-good; and for good container and codec support preferrably
each of gst-plugins-bad, gst-plugins-ugly and gst-libav.

Additionally, Gaupol's external preview is preconfigured to work with
[mpv](https://mpv.io/), [MPlayer](http://www.mplayerhq.hu/) and
[VLC](http://www.videolan.org/vlc/). Any other video player that
supports a command line argument to set where playing begins from can be
used as well, but you need to configure the command yourself.

Running
=======

To try Gaupol from the source directory without installation, use
command `bin/gaupol`. For installing Gaupol, see the file `INSTALL.md`.
