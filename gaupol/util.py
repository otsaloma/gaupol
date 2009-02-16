# Copyright (C) 2006-2008 Osmo Salomaa
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

"""Miscellaneous functions and decorators."""

from __future__ import absolute_import
from __future__ import with_statement

import codecs
import contextlib
import gaupol
import inspect
import locale
import os
import re
import subprocess
import sys
import urllib
import urlparse
import webbrowser


def affirm(value):
    """Raise AffirmationError if value evaluates to False."""

    if not value:
        raise gaupol.AffirmationError

def browse_url(url, browser=None):
    """Open URL in web browser."""

    if browser and isinstance(browser, basestring):
        return subprocess.Popen((browser, url))
    if "GNOME_DESKTOP_SESSION_ID" in os.environ:
        return subprocess.Popen(("gnome-open", url))
    if "KDE_FULL_SESSION" in os.environ:
        return subprocess.Popen(("kfmclient", "exec", url))
    if sys.platform == "darwin":
        return subprocess.Popen(("open", url))
    if is_command("xdg-open"):
        return subprocess.Popen(("xdg-open", url))
    if is_command("exo-open"):
        return subprocess.Popen(("exo-open", url))
    return webbrowser.open(url)

@gaupol.deco.once
def chardet_available():
    """Return True if chardet module is available."""

    try:
        import chardet
        return True
    except Exception:
        return False

def compare_versions_require(x, y):
    re_version = re.compile(r"^(\d+\.)+\d+$")
    assert re_version.match(x) is not None
    assert re_version.match(y) is not None

@gaupol.deco.contractual
def compare_versions(x, y):
    """Compare version strings x and y.

    Used version number formats are MAJOR.MINOR, MAJOR.MINOR.PATCH and
    MAJOR.MINOR.PATCH.{DATE/REVISION/...}, where all items are integers.
    Return 1 if x newer, 0 if equal or -1 if y newer.
    """
    x = [int(d) for d in x.split(".")]
    y = [int(d) for d in y.split(".")]
    return cmp(x, y)

def connect_require(observer, observable, signal, *args):
    if observer is not observable:
        assert hasattr(observer, observable)

@gaupol.deco.contractual
def connect(observer, observable, signal, *args):
    """Connect observable's signal to observer's callback method.

    If observable is a string, it should be an attribute of observer. If
    observable is not a string it should be the same as observer.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "%s_%s" % (observable, method_name)
    method_name = ("_on_%s" % method_name).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def copy_dict_ensure(source, value):
    assert source == value
    assert source is not value

@gaupol.deco.contractual
def copy_dict(source):
    """Copy source dictionary recursively and return copy."""

    destination = source.copy()
    for key, value in source.items():
        if isinstance(source[key], dict):
            destination[key] = copy_dict(source[key])
        elif isinstance(source[key], list):
            destination[key] = copy_list(source[key])
        elif isinstance(source[key], set):
            destination[key] = set(source[key])
    return destination

def copy_list_ensure(source, value):
    assert source == value
    assert source is not value

@gaupol.deco.contractual
def copy_list(source):
    """Copy source list recursively and return copy."""

    destination = list(source)
    for i, value in enumerate(source):
        if isinstance(value, dict):
            destination[i] = copy_dict(value)
        elif isinstance(value, list):
            destination[i] = copy_list(value)
        elif isinstance(value, set):
            destination[i] = set(value)
    return destination

@gaupol.deco.once
def enchant_available():
    """Return True if enchant module is available."""

    try:
        import enchant
        return True
    except Exception:
        return False

def get_all(names, pattern=None):
    """Return a tuple of names filtered by pattern to use as __all__."""

    import __future__
    for i in reversed(range(len(names))):
        if (names[i].startswith("_")) or \
           (names[i].endswith("_require")) or \
           (names[i].endswith("_ensure")) or \
           (names[i] in sys.modules) or \
           (names[i] in dir(__future__)):
            names.pop(i)
    if pattern is not None:
        regex = re.compile(pattern, re.UNICODE)
        names = [x for x in names if regex.search(x)]
    return tuple(names)

def get_chardet_version_ensure(value):
    if value is not None:
        assert isinstance(value, basestring)

@gaupol.deco.contractual
def get_chardet_version():
    """Return chardet version number as string or None."""

    try:
        import chardet
        return chardet.__version__
    except Exception:
        return None

def get_default_encoding_ensure(value):
    codecs.lookup(value)

@gaupol.deco.once
@gaupol.deco.contractual
def get_default_encoding():
    """Return the locale encoding or UTF-8 (as fallback)."""

    encoding = locale.getpreferredencoding()
    encoding = encoding or "utf_8"
    re_illegal = re.compile(r"[^a-z0-9_]")
    encoding = re_illegal.sub("_", encoding.lower())
    encoding = get_encoding_alias(encoding)
    return encoding

def get_enchant_version_ensure(value):
    if value is not None:
        assert isinstance(value, basestring)

@gaupol.deco.contractual
def get_enchant_version():
    """Return enchant version number as string or None."""

    try:
        import enchant
        return enchant.__version__
    except Exception:
        return None

def get_encoding_alias(encoding):
    """Return proper alias for encoding."""

    # pylint: disable-msg=E0611
    from encodings.aliases import aliases
    if encoding in aliases:
        return aliases[encoding]
    return encoding

def get_ranges_require(lst):
    for item in lst:
        assert isinstance(item, int)

def get_ranges_ensure(value, lst):
    for item in value:
        assert item == range(item[0], item[-1] + 1)

@gaupol.deco.contractual
def get_ranges(lst):
    """Return a list of ranges in list of integers."""

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

@gaupol.deco.contractual
def get_sorted_unique(lst):
    """Return sorted list with duplicates removed."""

    lst = sorted(lst)
    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)
    return lst

def get_unique_ensure(value, lst, keep_last=False):
    for item in value:
        assert value.count(item) == 1

@gaupol.deco.contractual
def get_unique(lst, keep_last=False):
    """Return list with duplicates removed.

    Keep the last duplicate if keep_last is True, else keep first.
    """
    lst = lst[:]
    if keep_last: lst.reverse()
    for i in reversed(range(len(lst))):
        for j in range(0, i):
            if lst[j] == lst[i]:
                lst.pop(i)
                break
    if keep_last: lst.reverse()
    return lst

def install_module(name, obj):
    """Install object's module into the gaupol's namespace.

    Typical call is of form install_module('foo', lambda: None).
    """
    gaupol.__dict__[name] = inspect.getmodule(obj)

def is_command(command):
    """Return True if command exists as a file in $PATH."""

    for directory in os.environ.get("PATH", "").split(os.pathsep):
        path = os.path.join(directory, command)
        if os.path.isfile(path): return True
    return False

def last(iterator):
    """Return the last value from iterator or None."""

    value = None
    while True:
        try: value = iterator.next()
        except StopIteration: break
    return value

def makedirs_ensure(value, directory):
    assert os.path.isdir(directory)

@gaupol.deco.contractual
def makedirs(directory):
    """Recursively make directory if it does not exist.

    Raise OSError if unsuccessful.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)

def path_to_uri(path):
    """Convert local filepath to URI."""

    if sys.platform == "win32":
        path = "/%s" % path.replace("\\", "/")
    return "file://%s" % urllib.quote(path)

def print_read_io(exc_info, path):
    """Print IO error message to standard output."""

    print "Failed to read file '%s': %s." % (path, exc_info[1].args[1])

def print_read_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    encoding = encoding or get_default_encoding()
    print "Failed to decode file '%s' with codec '%s'." % (path, encoding)

def print_remove_os(exc_info, path):
    """Print OS error message to standard output."""

    print "Failed to remove file '%s': %s." % (path, exc_info[1].args[1])

def print_write_io(exc_info, path):
    """Print IO error message to standard output."""

    print "Failed to write file '%s': %s." % (path, exc_info[1].args[1])

def print_write_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    encoding = encoding or get_default_encoding()
    print "Failed to encode file '%s' with codec '%s'." % (path, encoding)


def read_require(path, encoding=None, fallback="utf_8"):
    if encoding is not None:
        codecs.lookup(encoding)
    if fallback is not None:
        codecs.lookup(fallback)

@gaupol.deco.contractual
def read(path, encoding=None, fallback="utf_8"):
    """Read file and return text.

    fallback should be None to not fall back to UTF-8.
    Raise IOError if reading fails.
    Raise UnicodeError if decoding fails.
    """
    try:
        encoding = encoding or get_default_encoding()
        args = (path, "r", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            return fobj.read().strip()
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return read(path, "utf_8", None)
        raise

def readlines_require(path, encoding=None, fallback="utf_8"):
    if encoding is not None:
        codecs.lookup(encoding)
    if fallback is not None:
        codecs.lookup(fallback)

@gaupol.deco.contractual
def readlines(path, encoding=None, fallback="utf_8"):
    """Read file and return lines.

    fallback should be None to not fall back to UTF-8.
    Raise IOError if reading fails.
    Raise UnicodeError if decoding fails.
    """
    text = read(path, encoding, fallback)
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    return text.split("\n")

def shell_quote(path):
    """Quote and escape path for shell use."""

    if sys.platform != "win32":
        path = path.replace("\\", "\\\\")
        path = path.replace('"', '\\"')
    return '"%s"' % path

def start_process(command, **kwargs):
    """Start command as a new background subprocess.

    command and kwargs are passed to subprocess.Popen.__init__.
    raise ProcessError if something goes wrong.
    Return subprocess.Popen instance.
    """
    try:
        return subprocess.Popen(
            command,
            shell=(sys.platform != "win32"),
            cwd=os.getcwd(),
            env=os.environ.copy(),
            universal_newlines=True,
            **kwargs)
    except OSError, (no, message):
        raise gaupol.ProcessError(message)

def title_to_lower_case_ensure(value, title_name):
    assert value.islower()

@gaupol.deco.memoize
@gaupol.deco.contractual
def title_to_lower_case(title_name):
    """Convert title case name to lower case with underscores."""

    lower_name = ""
    for char in title_name:
        if char.isupper() and lower_name:
            lower_name += "_"
        lower_name += char.lower()
    return lower_name

def uri_to_path(uri):
    """Convert URI to local filepath."""

    uri = urllib.unquote(uri)
    if sys.platform == "win32":
        path = urlparse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urlparse.urlsplit(uri)[2]

def write_require(path, text, encoding=None, fallback="utf_8"):
    if encoding is not None:
        codecs.lookup(encoding)
    if fallback is not None:
        codecs.lookup(fallback)

def write_ensure(value, path, text, encoding=None, fallback="utf_8"):
    assert os.path.isfile(path)

@gaupol.deco.contractual
def write(path, text, encoding=None, fallback="utf_8"):
    """Write text to file.

    fallback should be None to not fall back to UTF-8.
    Raise IOError if writing fails.
    Raise UnicodeError if encoding fails.
    """
    try:
        encoding = encoding or get_default_encoding()
        args = (path, "w", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            return fobj.write(text)
    except UnicodeError:
        if not fallback in (encoding, None, ""):
            return write(path, text, "utf_8", None)
        raise

def writelines_require(path, lines, encoding=None, fallback="utf_8"):
    if encoding is not None:
        codecs.lookup(encoding)
    if fallback is not None:
        codecs.lookup(fallback)

def writelines_ensure(value, path, lines, encoding=None, fallback="utf_8"):
    assert os.path.isfile(path)

@gaupol.deco.contractual
def writelines(path, lines, encoding=None, fallback="utf_8"):
    """Write lines of text to file.

    fallback should be None to not fall back to UTF-8.
    Raise IOError if writing fails.
    Raise UnicodeError if encoding fails.
    """
    text = os.linesep.join(lines) + os.linesep
    return write(path, text, encoding, fallback)
