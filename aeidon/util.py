# Copyright (C) 2006-2009,2011 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous functions."""

import aeidon
import inspect
import locale
import os
import re
import subprocess
import sys
import urllib.parse


def affirm(value):
    """Raise :exc:`aeidon.AffirmationError` if value evaluates to ``False``."""
    if not value:
        raise aeidon.AffirmationError

@aeidon.deco.once
def chardet_available():
    """Return ``True`` if :mod:`chardet` module is available."""
    try:
        import chardet
        return True
    except Exception:
        return False

def compare_versions_require(x, y):
    re_version = re.compile(r"^(\d+\.)+\d+$")
    assert re_version.match(x) is not None
    assert re_version.match(y) is not None

@aeidon.deco.contractual
def compare_versions(x, y):
    """
    Compare version strings `x` and `y`.

    Used version number formats are ``MAJOR.MINOR``, ``MAJOR.MINOR.PATCH`` and
    ``MAJOR.MINOR.PATCH.DATE/REVISION``, where all items are integers.
    Return 1 if `x` newer, 0 if equal or -1 if `y` newer.
    """
    compare = lambda a, b: (a > b) - (a < b)
    return compare(list(map(int, x.split("."))),
                   list(map(int, y.split("."))))

def connect_require(observer, observable, signal, *args):
    if observer is not observable:
        assert hasattr(observer, observable)

@aeidon.deco.contractual
def connect(observer, observable, signal, *args):
    """
    Connect `observable`'s signal to `observer`'s callback method.

    If `observable` is a string, it should be an attribute of `observer`.
    If `observable` is not a string it should be the same as `observer`.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "_".join((observable, method_name))
    method_name = ("_on_{}".format(method_name)).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def copy_dict_ensure(src, value):
    assert src == value
    assert src is not value

@aeidon.deco.contractual
def copy_dict(src):
    """Copy `src` dictionary recursively and return copy."""
    dst = src.copy()
    for key, value in src.items():
        if isinstance(value, dict):
            dst[key] = copy_dict(value)
        if isinstance(value, list):
            dst[key] = copy_list(value)
        if isinstance(value, set):
            dst[key] = set(value)
    return dst

def copy_list_ensure(src, value):
    assert src == value
    assert src is not value

@aeidon.deco.contractual
def copy_list(src):
    """Copy `src` list recursively and return copy."""
    dst = list(src)
    for i, value in enumerate(src):
        if isinstance(value, dict):
            dst[i] = copy_dict(value)
        if isinstance(value, list):
            dst[i] = copy_list(value)
        if isinstance(value, set):
            dst[i] = set(value)
    return dst

def detect_format_require(path, encoding):
    assert aeidon.encodings.is_valid_code(encoding)

@aeidon.deco.contractual
def detect_format(path, encoding):
    """
    Detect and return format of subtitle file at `path`.

    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    Raise :exc:`aeidon.FormatError` if unable to detect format.
    Return an :attr:`aeidon.formats` enumeration item.
    """
    re_ids = [(x, re.compile(x.identifier)) for x in aeidon.formats]
    with open(path, "r", encoding=encoding) as fobj:
        for line in fobj:
            for format, re_id in re_ids:
                if re_id.search(line) is not None:
                    return format
    raise aeidon.FormatError("Failed to detect format of file {}"
                             .format(repr(path)))

def detect_newlines(path):
    """Detect and return the newline type of file at `path` or ``None``."""
    try:
        fobj = open(path, "r")
        fobj.read()
        chars = fobj.newlines
    except Exception:
        return None
    if chars is None: return None
    if isinstance(chars, tuple):
        chars = chars[0]
    return aeidon.newlines.find_item("value", chars)

@aeidon.deco.once
def enchant_available():
    """Return ``True`` if :mod:`enchant` module is available."""
    try:
        import enchant
        return True
    except Exception:
        return False

def flatten(lst):
    """
    Return a shallow version of `lst`.

    >>> aeidon.util.flatten([1, 2, 3, [4, 5, [6]]])
    [1, 2, 3, 4, 5, 6]
    """
    flat_lst = []
    for item in lst:
        if isinstance(item, list):
            flat_lst.extend(flatten(item))
        else: # Non-list item.
            flat_lst.append(item)
    return flat_lst

def get_chardet_version_ensure(value):
    if value is not None:
        assert isinstance(value, str)

@aeidon.deco.contractual
def get_chardet_version():
    """Return :mod:`chardet` version number as string or ``None``."""
    try:
        import chardet
        return chardet.__version__
    except Exception:
        return None

def get_default_encoding_ensure(value):
    assert aeidon.encodings.is_valid_code(value)

@aeidon.deco.once
@aeidon.deco.contractual
def get_default_encoding():
    """Return the locale encoding or UTF-8 (as fallback)."""
    encoding = locale.getpreferredencoding()
    encoding = encoding or "utf_8"
    re_illegal = re.compile(r"[^a-z0-9_]")
    encoding = re_illegal.sub("_", encoding.lower())
    encoding = get_encoding_alias(encoding)
    return encoding

@aeidon.deco.once
def get_default_newline():
    """Return system default newline as :attr:`aeidon.newlines` item."""
    return aeidon.newlines.find_item("value", os.linesep)

def get_enchant_version_ensure(value):
    if value is not None:
        assert isinstance(value, str)

@aeidon.deco.contractual
def get_enchant_version():
    """Return :mod:`enchant` version number as string or ``None``."""
    try:
        import enchant
        return enchant.__version__
    except Exception:
        return None

def get_encoding_alias(encoding):
    """Return proper Python alias for `encoding`."""
    from encodings.aliases import aliases
    if encoding in aliases:
        return aliases[encoding]
    return encoding

def get_ranges_require(lst):
    for item in lst:
        assert isinstance(item, int)

def get_ranges_ensure(value, lst):
    for item in value:
        assert item == list(range(item[0], item[-1] + 1))

@aeidon.deco.contractual
def get_ranges(lst):
    """
    Return a list of ranges in list of integers.

    >>> aeidon.util.get_ranges([1, 2, 3, 5, 6, 7, 9, 11, 12])
    [[1, 2, 3], [5, 6, 7], [9], [11, 12]]
    """
    if not lst: return []
    lst = get_sorted_unique(lst)
    ranges = [[lst.pop(0)]]
    for item in lst:
        if item == ranges[-1][-1] + 1:
            ranges[-1].append(item)
        else: ranges.append([item])
    return ranges

def get_sorted_unique_ensure(value, lst):
    for item in value:
        assert value.count(item) == 1
    assert sorted(value) == value

@aeidon.deco.contractual
def get_sorted_unique(lst):
    """
    Return sorted `lst` with duplicates removed.

    >>> aeidon.util.get_sorted_unique([3, 2, 1, 2, 4, 4])
    [1, 2, 3, 4]
    """
    lst = sorted(lst)
    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)
    return lst

@aeidon.deco.memoize(100)
def get_template_header(format):
    """
    Read and return the template header for `format`.

    Raise :exc:`IOError` if reading global header file fails.
    Raise :exc:`UnicodeError` if decoding global header file fails.
    """
    header = None
    directory = os.path.join(aeidon.DATA_HOME_DIR, "headers")
    path = os.path.join(directory, format.name.lower())
    if os.path.isfile(path):
        try: header = read(path, None).rstrip()
        except IOError:
            print_read_io(sys.exc_info(), path)
        except UnicodeError:
            print_read_unicode(sys.exc_info(),
                               path,
                               get_default_encoding())

    if header is None:
        directory = os.path.join(aeidon.DATA_DIR, "headers")
        path = os.path.join(directory, format.name.lower())
        header = read(path, "ascii").rstrip()
    return normalize_newlines(header)

def get_unique_ensure(value, lst, keep_last=False):
    for item in value:
        assert value.count(item) == 1

@aeidon.deco.contractual
def get_unique(lst, keep_last=False):
    """
    Return `lst` with duplicates removed.

    Keep the last duplicate if `keep_last` is ``True``, else keep first.

    >>> aeidon.util.get_unique([3, 2, 1, 2, 4, 4])
    [3, 2, 1, 4]
    >>> aeidon.util.get_unique([3, 2, 1, 2, 4, 4], keep_last=True)
    [3, 1, 2, 4]
    """
    lst = lst[:]
    if keep_last:
        lst.reverse()
    for i in reversed(range(len(lst))):
        for j in range(0, i):
            if lst[j] == lst[i]:
                lst.pop(i)
                break
    if keep_last:
        lst.reverse()
    return lst

def install_module(name, obj):
    """
    Install `obj`'s module into the :mod:`aeidon` namespace.

    Typical call is of form::

        aeidon.util.install_module("foo", lambda: None)
    """
    aeidon.__dict__[name] = inspect.getmodule(obj)

def is_command(command):
    """Return ``True`` if `command` exists as a file in ``$PATH``."""
    dirs = os.environ.get("PATH", "").split(os.pathsep)
    paths = [os.path.join(x, command) for x in dirs]
    return any(map(os.path.isfile, paths))

def last(iterator):
    """Return the last value from `iterator` or ``None``."""
    value = None
    for value in iterator: pass
    return value

def makedirs_ensure(value, directory):
    assert os.path.isdir(directory)

@aeidon.deco.contractual
def makedirs(directory):
    """
    Recursively make `directory` if it does not exist.

    Raise :exc:`OSError` if unsuccessful.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)

def normalize_newlines(text):
    """
    Convert all newlines in `text` to Unix newlines.

    >>> aeidon.util.normalize_newlines("one\\r\\ntwo")
    'one\\ntwo'
    """
    re_newline_char = re.compile(r"\r\n?")
    return re_newline_char.sub("\n", text)

def path_to_uri(path):
    """Convert local filepath to URI."""
    if sys.platform == "win32":
        path = "/{}".format(path.replace("\\", "/"))
    return "file://{}".format(urllib.parse.quote(path))

def print_read_io(exc_info, path):
    """Print :exc:`IOError` message to standard error."""
    print("Failed to read file '{}': {}"
          .format(path, exc_info[1].args[1]),
          file=sys.stderr)

def print_read_unicode(exc_info, path, encoding):
    """Print :exc:`UnicodeError` message to standard error."""
    encoding = encoding or get_default_encoding()
    print("Failed to decode file '{}' with codec '{}'"
          .format(path, encoding),
          file=sys.stderr)

def print_remove_os(exc_info, path):
    """Print :exc:`OSError` message to standard error."""
    print("Failed to remove file '{}': {}"
          .format(path, exc_info[1].args[1]),
          file=sys.stderr)

def print_write_io(exc_info, path):
    """Print :exc:`IOError` message to standard error."""
    print("Failed to write file '{}': {}"
          .format(path, exc_info[1].args[1]),
          file=sys.stderr)

def print_write_unicode(exc_info, path, encoding):
    """Print :exc:`UnicodeError` message to standard error."""
    encoding = encoding or get_default_encoding()
    print("Failed to encode file '{}' with codec '{}'"
          .format(path, encoding),
          file=sys.stderr)

def read_require(path, encoding=None, fallback="utf_8"):
    if encoding is not None:
        assert aeidon.encodings.is_valid_code(encoding)
    if fallback is not None:
        assert aeidon.encodings.is_valid_code(fallback)

@aeidon.deco.contractual
def read(path, encoding=None, fallback="utf_8"):
    """
    Read file at `path` and return text.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    """
    encoding = encoding or get_default_encoding()
    try:
        with open(path, "r", encoding=encoding) as fobj:
            return fobj.read().strip()
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return read(path, fallback, None)
        raise # UnicodeError

def readlines_require(path, encoding=None, fallback="utf_8"):
    if encoding is not None:
        assert aeidon.encodings.is_valid_code(encoding)
    if fallback is not None:
        assert aeidon.encodings.is_valid_code(fallback)

@aeidon.deco.contractual
def readlines(path, encoding=None, fallback="utf_8"):
    """
    Read file at `path` and return lines.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if reading fails.
    Raise :exc:`UnicodeError` if decoding fails.
    """
    text = read(path, encoding, fallback)
    text = normalize_newlines(text)
    return text.split("\n")

def replace_extension(path, format):
    """Replace possible extension in `path` with that of `format`."""
    extensions = [x.extension for x in aeidon.formats]
    if path.endswith(tuple(extensions)):
        path = path[:path.rfind(".")]
    return "".join((path, format.extension))

def shell_quote(path):
    """Quote and escape `path` for shell use."""
    if sys.platform != "win32":
        # Windows filenames can contain backslashes only as
        # directory separators and cannot contain double quotes.
        path = path.replace("\\", "\\\\")
        path = path.replace('"', '\\"')
    return '"{}"'.format(path)

def start_process(command, **kwargs):
    """
    Start `command` as a new background subprocess.

    `command` and `kwargs` are passed to :class:`subprocess.Popen`.
    Raise :exc:`aeidon.ProcessError` if something goes wrong.
    Return :class:`subprocess.Popen` instance.
    """
    # Use no environment on Windows due to a subprocess bug.
    # https://bugzilla.gnome.org/show_bug.cgi?id=605805
    try:
        return subprocess.Popen(command,
                                shell=(sys.platform != "win32"),
                                cwd=os.getcwd(),
                                env=(os.environ.copy()
                                     if sys.platform != "win32"
                                     else None),

                                universal_newlines=True,
                                **kwargs)

    except OSError as error:
        raise aeidon.ProcessError(error.args[1])

def title_to_lower_case_ensure(value, title_name):
    assert value.islower()

@aeidon.deco.memoize(100)
@aeidon.deco.contractual
def title_to_lower_case(title_name):
    """
    Convert title case name to lower case with underscores.

    >>> aeidon.util.title_to_lower_case('TitleCase')
    'title_case'
    """
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
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urllib.parse.urlsplit(uri)[2]

def write_require(path, text, encoding=None, fallback="utf_8"):
    if encoding is not None:
        assert aeidon.encodings.is_valid_code(encoding)
    if fallback is not None:
        assert aeidon.encodings.is_valid_code(fallback)

def write_ensure(value, path, text, encoding=None, fallback="utf_8"):
    assert os.path.isfile(path)

@aeidon.deco.contractual
def write(path, text, encoding=None, fallback="utf_8"):
    """
    Write `text` to file at `path`.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if writing fails.
    Raise :exc:`UnicodeError` if encoding fails.
    """
    encoding = encoding or get_default_encoding()
    try:
        with open(path, "w", encoding=encoding) as fobj:
            return fobj.write(text)
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return write(path, text, fallback, None)
        raise # UnicodeError

def writelines_require(path, lines, encoding=None, fallback="utf_8"):
    if encoding is not None:
        assert aeidon.encodings.is_valid_code(encoding)
    if fallback is not None:
        assert aeidon.encodings.is_valid_code(fallback)

def writelines_ensure(value, path, lines, encoding=None, fallback="utf_8"):
    assert os.path.isfile(path)

@aeidon.deco.contractual
def writelines(path, lines, encoding=None, fallback="utf_8"):
    """
    Write `lines` of text to file at `path`.

    `fallback` should be ``None`` to try only `encoding`.
    Raise :exc:`IOError` if writing fails.
    Raise :exc:`UnicodeError` if encoding fails.
    """
    text = os.linesep.join(lines) + os.linesep
    return write(path, text, encoding, fallback)
