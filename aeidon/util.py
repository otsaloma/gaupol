# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Miscellaneous functions."""

import aeidon
import collections
import contextlib
import locale
import mimetypes
import os
import random
import re
import shutil
import stat
import subprocess
import sys
import urllib.parse

from pathlib import Path

VIDEO_FILE_EXTENSIONS = [
    ".avi",
    ".flv",
    ".m2ts",
    ".mkv",
    ".mov",
    ".mp4",
    ".ogg",
    ".ogv",
    ".vob",
    ".webm",
]

def affirm(value):
    """Raise :exc:`aeidon.AffirmationError` if value evaluates to ``False``."""
    if not value:
        raise aeidon.AffirmationError(f"Not True: {value!r}")

@contextlib.contextmanager
def atomic_open(path, mode="w", *args, **kwargs):
    """
    A context manager for atomically writing a file.

    The file is written to a temporary file on the same filesystem, flushed and
    fsynced and then renamed to replace the existing file. This should
    (probably) be atomic on any Unix system. On Windows, it should (probably)
    be atomic if using Python 3.3 or greater.
    """
    path = Path(path).resolve()
    chars = list("abcdefghijklmnopqrstuvwxyz0123456789")
    while True:
        # Let's use a hidden temporary file to avoid a file
        # flickering in a possibly open file browser window.
        suffix = "".join(random.sample(chars, 8))
        temp_path = path.parent / f".{path.name}.tmp{suffix}"
        if not temp_path.is_file(): break
    try:
        if path.is_file():
            # If the file exists, use the same permissions.
            # Note that all other file metadata, including
            # owner and group, is not preserved.
            temp_path.touch()
            st = path.stat()
            temp_path.chmod(stat.S_IMODE(st.st_mode))
        with open(temp_path, mode, *args, **kwargs) as f:
            yield f
            f.flush()
            os.fsync(f.fileno())
        try:
            # This should be atomic on Windows too.
            # Path.replace will fail if path and temp_path
            # are not on the same device, for instance they
            # can be on two separate branches of a union
            # mount. Atomicity is not possible in this case.
            temp_path.replace(path)
        except OSError:
            # Fall back to a non-atomic operation using
            # shutil.move. On Windows this requires that
            # the destination file does not exist.
            if sys.platform == "win32":
                path.unlink(missing_ok=True)
            shutil.move(temp_path, path)
    finally:
        with contextlib.suppress(Exception):
            temp_path.unlink()

@aeidon.deco.once
def chardet_available():
    """Return ``True`` if :mod:`charset_normalizer` module is available."""
    try:
        import charset_normalizer # noqa
        return True
    except ImportError:
        return False

def compare_versions(x, y):
    """
    Compare version strings `x` and `y`.

    Used version number formats are ``MAJOR.MINOR``, ``MAJOR.MINOR.PATCH``
    and ``MAJOR.MINOR.PATCH.DATE/REVISION``, where all items are integers.
    Return 1 if `x` newer, 0 if equal or -1 if `y` newer.
    """
    compare = lambda a, b: (a > b) - (a < b)
    return compare(list(map(int, x.split("."))),
                   list(map(int, y.split("."))))

def connect(observer, observable, signal, *args):
    """
    Connect `observable`'s `signal` to `observer`'s callback method.

    If `observable` is a string, it should be an attribute of `observer`.
    If `observable` is not a string it should be the same as `observer`.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "_".join((observable, method_name))
    method_name = f"_on_{method_name}".replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def detect_format(path, encoding):
    """
    Detect and return format of subtitle file at `path`.

    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    Raise :exc:`aeidon.FormatError` if unable to detect format.
    Return an :attr:`aeidon.formats` enumeration item.
    """
    re_ids = [(x, re.compile(x.identifier)) for x in aeidon.formats]
    with open(path, "r", encoding=encoding) as f:
        for line in f:
            for format, re_id in re_ids:
                if re_id.search(line) is not None:
                    return format
    raise aeidon.FormatError(f"Failed to detect format of file {path!r}")

def detect_newlines(path):
    """Detect and return the newline type of file at `path` or ``None``."""
    try:
        with open(path, "r", newline="") as f:
            f.read()
            chars = f.newlines
    except Exception:
        return None
    if chars is None:
        return None
    if isinstance(chars, str):
        return aeidon.newlines.find_item("value", chars)
    if isinstance(chars, tuple):
        if len(chars) == 1:
            return aeidon.newlines.find_item("value", chars[0])
        # This is not actually correct. If both CR and LF are detected,
        # it could mean a mixture of Mac and Unix newlines on separate
        # lines or one Windows newline in a mostly something else file.
        # We could count the frequencies, but it's probably not worth
        # the effort.
        return aeidon.newlines.WINDOWS
    return None

@aeidon.deco.listify
def flatten(lst):
    """
    Return a shallow version of `lst`.

    >>> aeidon.util.flatten([1, 2, 3, [4, 5, [6]]])
    [1, 2, 3, 4, 5, 6]
    """
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else: # Non-list item.
            yield item

def get_chardet_version():
    """Return :mod:`charset_normalizer` version number as string or ``None``."""
    try:
        import charset_normalizer
        return charset_normalizer.__version__
    except ImportError:
        return None

@aeidon.deco.once
def get_default_encoding(fallback="utf_8"):
    """Return the locale encoding or `fallback`."""
    encoding = locale.getpreferredencoding()
    encoding = encoding or fallback
    re_illegal = re.compile(r"[^a-z0-9_]")
    encoding = re_illegal.sub("_", encoding.lower())
    encoding = get_encoding_alias(encoding)
    return encoding

@aeidon.deco.once
def get_default_newline():
    """Return system default newline as :attr:`aeidon.newlines` item."""
    return aeidon.newlines.find_item("value", os.linesep)

def get_encoding_alias(encoding):
    """Return proper Python alias for `encoding`."""
    from encodings.aliases import aliases
    with contextlib.suppress(LookupError):
        return aliases[encoding]
    return encoding

def get_ranges(lst):
    """
    Return a list of ranges in list of integers.

    >>> aeidon.util.get_ranges([1, 2, 3, 5, 6, 7, 9, 11, 12])
    [[1, 2, 3], [5, 6, 7], [9], [11, 12]]
    """
    if not lst: return []
    lst = sorted(get_unique(lst))
    ranges = [[lst.pop(0)]]
    for item in lst:
        if item == ranges[-1][-1] + 1:
            ranges[-1].append(item)
        else:
            ranges.append([item])
    return ranges

def get_template_header(format):
    """
    Read and return the template header for `format`.

    Raise :exc:`IOError` if reading global header file fails.
    Raise :exc:`UnicodeError` if decoding global header file fails.
    """
    path = aeidon.DATA_HOME_DIR / "headers" / format.name.lower()
    with contextlib.suppress(Exception):
        header = read(path, encoding=None, quiet=True).rstrip()
        return normalize_newlines(header)
    path = aeidon.DATA_DIR / "headers" / format.name.lower()
    header = read(path, "ascii").rstrip()
    return normalize_newlines(header)

def get_unique(lst, keep_last=False):
    """Return `lst` with duplicates removed."""
    if keep_last:
        return list(reversed(get_unique(list(reversed(lst)))))
    # https://stackoverflow.com/a/7961425
    return list(collections.OrderedDict.fromkeys(lst))

def is_video_file(path):
    """Return ``True`` if `path` is a video file."""
    path = Path(path)
    if not path.is_file():
        return False
    # The mimetypes module doesn't work well on Windows,
    # fall back on a custom list of video file extensions.
    type, encoding = mimetypes.guess_type(path)
    return ((type and type.startswith("video/")) or
            path.suffix.lower() in VIDEO_FILE_EXTENSIONS)

def last(iterator):
    """Return the last value from `iterator` or ``None``."""
    value = None
    for value in iterator: pass
    return value

def makedirs(directory):
    """
    Recursively make `directory` if it does not exist.

    Raise :exc:`OSError` if unsuccessful.
    """
    directory = Path(directory).resolve()
    if directory.is_dir():
        return directory
    try:
        directory.mkdir(parents=True)
    except OSError as error:
        print(f"Failed to create directory {directory!r}: {error!s}",
              file=sys.stderr)
        raise # OSError
    return directory

def normalize_newlines(text):
    """Convert all newlines in `text` to "\\n"."""
    re_newline_char = re.compile(r"\r\n?")
    return re_newline_char.sub("\n", text)

def path_to_uri(path):
    """Convert local filepath to URI."""
    path = str(path)
    if sys.platform == "win32":
        path = "/" + path.replace("\\", "/")
    path = urllib.parse.quote(path)
    return f"file://{path}"

def print_read_io(exc_info, path):
    """Print :exc:`IOError` message to standard error."""
    message = exc_info[1].args[1]
    print(f"Failed to read file '{path}': {message}",
          file=sys.stderr)

def print_read_unicode(exc_info, path, encoding):
    """Print :exc:`UnicodeError` message to standard error."""
    encoding = encoding or get_default_encoding()
    print(f"Failed to decode file '{path}' with codec '{encoding}'",
          file=sys.stderr)

def print_write_io(exc_info, path):
    """Print :exc:`IOError` message to standard error."""
    message = exc_info[1].args[1]
    print(f"Failed to write file '{path}': {message}",
          file=sys.stderr)

def print_write_unicode(exc_info, path, encoding):
    """Print :exc:`UnicodeError` message to standard error."""
    encoding = encoding or get_default_encoding()
    print(f"Failed to encode file '{path}' with codec '{encoding}'",
          file=sys.stderr)

def read(path, encoding=None, fallback="utf_8", quiet=False):
    """
    Read file at `path` and return text.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    """
    encoding = encoding or get_default_encoding()
    try:
        return Path(path).read_text(encoding=encoding).strip()
    except IOError:
        if not quiet:
            print_read_io(sys.exc_info(), path)
        raise # IOError
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return read(path, fallback, None, quiet)
        if not quiet:
            print_read_unicode(sys.exc_info(), path, encoding)
        raise # UnicodeError

def readlines(path, encoding=None, fallback="utf_8", quiet=False):
    """
    Read file at `path` and return lines.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    """
    text = read(path, encoding, fallback, quiet)
    text = normalize_newlines(text)
    return text.split("\n")

def replace_extension(path, format):
    """Replace possible extension in `path` with that of `format`."""
    path = Path(path)
    extensions = [x.extension for x in aeidon.formats]
    if path.suffix in extensions:
        path = path.with_suffix("")
    return path.with_name(path.name + format.extension)

def shell_quote(path):
    """Quote and escape `path` for shell use."""
    path = str(path)
    if sys.platform != "win32":
        # Windows filenames can contain backslashes only as
        # directory separators and cannot contain double quotes.
        path = path.replace("\\", "\\\\")
        path = path.replace('"', '\\"')
    return f'"{path}"'

def start_process(command, **kwargs):
    """
    Start `command` as a new background subprocess.

    `command` and `kwargs` are passed to :class:`subprocess.Popen`.
    Raise :exc:`aeidon.ProcessError` if something goes wrong.
    Return :class:`subprocess.Popen` instance.
    """
    # Use no environment on Windows due to a subprocess bug.
    # https://bugzilla.gnome.org/show_bug.cgi?id=605805
    env = os.environ.copy() if sys.platform != "win32" else None
    try:
        return subprocess.Popen(command,
                                shell=(sys.platform != "win32"),
                                cwd=os.getcwd(),
                                env=env,
                                universal_newlines=True,
                                **kwargs)

    except OSError as error:
        raise aeidon.ProcessError(str(error.args))

def title_to_lower_case(title_name):
    """Convert title case name to lower case with underscores."""
    lower_name = ""
    for char in title_name:
        if char.isupper() and lower_name:
            lower_name += "_"
        lower_name += char.lower()
    return lower_name

def uri_to_path(uri):
    """Convert `uri` to local filepath."""
    uri = urllib.parse.unquote(uri)
    if sys.platform == "win32":
        path = urllib.parse.urlsplit(uri)[2]
        return Path(path.lstrip("/").replace("/", "\\"))
    return Path(urllib.parse.urlsplit(uri)[2])

def write(path, text, encoding=None, fallback="utf_8", quiet=False):
    """
    Write `text` to file at `path`.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if writing fails.
    Raise :exc:`UnicodeError` if encoding fails.
    """
    makedirs(Path(path).parent)
    encoding = encoding or get_default_encoding()
    try:
        return Path(path).write_text(text, encoding=encoding)
    except IOError:
        if not quiet:
            print_write_io(sys.exc_info(), path)
        raise # IOError
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return write(path, text, fallback, None, quiet)
        if not quiet:
            print_write_unicode(sys.exc_info(), path, encoding)
        raise # UnicodeError

def writelines(path, lines, encoding=None, fallback="utf_8", quiet=False):
    """
    Write `lines` of text to file at `path`.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if writing fails.
    Raise :exc:`UnicodeError` if encoding fails.
    """
    text = "\n".join(lines) + "\n"
    return write(path, text, encoding, fallback, quiet)
