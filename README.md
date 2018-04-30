Gaupol
======

[![Build Status](https://travis-ci.org/otsaloma/gaupol.svg)](https://travis-ci.org/otsaloma/gaupol)
[![Packages](https://repology.org/badge/tiny-repos/gaupol.svg)](https://repology.org/metapackage/gaupol)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/gaupol)
[![Donate](https://img.shields.io/badge/donate-paypal.me-blue.svg)](https://www.paypal.me/otsaloma)

Gaupol is an editor for text-based subtitle files. It supports multiple
subtitle file formats and provides means of creating, editing and
translating subtitles and timing subtitles to match video.

Gaupol also includes `aeidon`, a separately installable general-purpose
Python package for reading, writing and manipulating text-based subtitle
files. See [`README.aeidon.md`](README.aeidon.md) for details.

## Installing

### Linux

Gaupol is packaged for most of the popular [distros][packages], so
easiest is to install via your distro's package management. If you need
a newer version than packaged, read on.

Gaupol requires Python ≥ 3.2, PyGObject ≥ 3.12 and GTK+ ≥ 3.12.
Additionally, during installation you need gettext. Optional, but
strongly recommended dependencies include:

| Dependency | Version | Required for |
| :--------- | :------ | :----------- |
| [GStreamer](https://gstreamer.freedesktop.org/) | ≥ 1.6 | integrated video player |
| [PyEnchant](https://github.com/rfk/pyenchant) | ≥ 1.4.0 | spell-check |
| [GtkSpell](http://gtkspell.sourceforge.net/) | ≥ 3.0.0 | inline spell-check |
| [iso-codes](https://salsa.debian.org/iso-codes-team/iso-codes) | any | translations |
| [chardet](https://pypi.org/project/chardet/) | any | character encoding auto-detection |

From GStreamer you need at least the core, gst-plugins-base,
gst-plugins-good and gst-plugins-bad; and for good container and codec
support preferrably both of gst-plugins-ugly and gst-libav.

On Debian/Ubuntu you can install the dependencies with the following
command.

    sudo apt install python3 \
                     python3-gi \
                     python3-gi-cairo \
                     gir1.2-gtk-3.0 \
                     gir1.2-gstreamer-1.0 \
                     gir1.2-gst-plugins-base-1.0 \
                     gstreamer1.0-plugins-good \
                     gstreamer1.0-plugins-bad \
                     gstreamer1.0-plugins-ugly \
                     gstreamer1.0-libav \
                     python3-enchant \
                     gir1.2-gtkspell3-3.0 \
                     iso-codes \
                     python3-chardet \
                     gettext

Then, to install Gaupol, run command

    sudo python3 setup.py install --prefix=/usr/local

[packages]: https://repology.org/metapackage/gaupol

### Windows

See the [releases page][releases] for installers. Note that Windows
packaging will sometimes be a bit behind and might sometimes skip a
version, so you might need to look further than the latest release.

[releases]: https://github.com/otsaloma/gaupol/releases
