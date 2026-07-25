# Python Package aeidon for Subtitles

[![PyPI](https://img.shields.io/pypi/v/aeidon.svg)](https://pypi.org/project/aeidon/)
[![Downloads](https://pepy.tech/badge/aeidon/month)](https://pepy.tech/project/aeidon)

aeidon is a Python package that provides classes and functions for
dealing with text-based subtitle files of many different formats.
Functions exist for reading and writing subtitle files as well as
manipulating subtitle data, i.e. positions (times or frames) and texts.

## Examples

Converting a file from the SubRip format to the MicroDVD format:

```python
project = aeidon.Project()
project.open_main("/path/to/file.srt", "utf_8")
project.set_framerate(aeidon.framerates.FPS_23_976)
project.save_main(aeidon.files.new(aeidon.formats.MICRODVD,
                                   "/path/to/file.sub",
                                   "utf_8"))
```

Making all subtitles in a file appear two seconds earlier:

```python
project = aeidon.Project()
project.open_main("/path/to/file.srt", "utf_8")
project.shift_positions(None, aeidon.as_seconds(-2))
project.save_main()
```

## Installation

```bash
pip install -U aeidon
```

## Documentation

https://otsaloma.io/gaupol/doc/api/aeidon.html

The API documentation is for an older version, but it applies 99% to the
latest version as well. There's currently no build mechanism for
up-to-date API documentation. Restoring that is a known low-priority
issue.

## History

aeidon is part of the [Gaupol](https://github.com/otsaloma/gaupol)
subtitle editor, where the other package, gaupol, provides the GTK user
interface.
