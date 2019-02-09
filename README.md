Gaupol
======

[![Build Status](https://travis-ci.org/otsaloma/gaupol.svg)](https://travis-ci.org/otsaloma/gaupol)
[![Packages](https://repology.org/badge/tiny-repos/gaupol.svg)](https://repology.org/metapackage/gaupol)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/gaupol)

Gaupol is an editor for text-based subtitle files. It supports multiple
subtitle file formats and provides means of creating, editing and
translating subtitles and timing subtitles to match video.

Gaupol also includes `aeidon`, a separately installable general-purpose
Python package for reading, writing and manipulating text-based subtitle
files. See [`README.aeidon.md`](README.aeidon.md) for details.

## Installing

### Linux

#### Packages

Gaupol is packaged for most of the popular [distros][], so easiest is to
install via your distro's package management. If not packaged for your
distro or you need a newer version than packaged, read below on how to
install from Flatpak or the source code.

[distros]: https://repology.org/metapackage/gaupol

#### Flatpak

Stable releases are available via [Flathub][].

The development version can be installed by running command `make
install` under the `flatpak` directory. You need make, flatpak-builder
and gettext to build the Flatpak.

[Flathub]: https://flathub.org/apps/details/io.otsaloma.gaupol

#### Source

Gaupol requires Python ≥ 3.2, PyGObject ≥ 3.12 and GTK+ ≥ 3.12.
Additionally, during installation you need gettext. Optional, but
strongly recommended dependencies include:

| Dependency | Version | Required for |
| :--------- | :------ | :----------- |
| [GStreamer](https://gstreamer.freedesktop.org/) | ≥ 1.6 | integrated video player |
| [PyEnchant](https://github.com/rfk/pyenchant) | ≥ 1.4.0 | spell-check |
| [GtkSpell](http://gtkspell.sourceforge.net/) | ≥ 3.0.0 | inline spell-check |
| [iso-codes](https://salsa.debian.org/iso-codes-team/iso-codes) | ≥ 3.67 | translations |
| [chardet](https://github.com/chardet/chardet) | any | character encoding auto-detection |

From GStreamer you need at least the core, gst-plugins-base,
gst-plugins-good and gst-plugins-bad; and for good container and codec
support preferrably both of gst-plugins-ugly and gst-libav.

On Debian/Ubuntu you can install the dependencies with the following
command.

    sudo apt install gettext \
                     gir1.2-gst-plugins-base-1.0 \
                     gir1.2-gstreamer-1.0 \
                     gir1.2-gtk-3.0 \
                     gir1.2-gtkspell3-3.0 \
                     gstreamer1.0-gtk3 \
                     gstreamer1.0-libav \
                     gstreamer1.0-plugins-bad \
                     gstreamer1.0-plugins-good \
                     gstreamer1.0-plugins-ugly \
                     iso-codes \
                     python3 \
                     python3-chardet \
                     python3-dev \
                     python3-enchant \
                     python3-gi \
                     python3-gi-cairo

Then, to install Gaupol, run command

    sudo python3 setup.py install --prefix=/usr/local

### Windows

Windows installers are built irregularly, see [releases][].

[releases]: https://github.com/otsaloma/gaupol/releases
