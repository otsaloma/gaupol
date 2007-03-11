# Copyright (C) 2006-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Miscellaneous functions."""


import codecs
import cPickle
import functools
import gc
import inspect
import os
import subprocess
import sys
import urllib
import urlparse
import webbrowser

from gaupol import enclib, paths


__all__ = set(dir())

def memoize(function):
    """Decorator for functions that cache their return values."""

    cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        key = cPickle.dumps((args, kwargs))
        if not key in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]

    return wrapper

def browse_url(url, browser=None):
    """Open URL in browser."""

    url = shell_quote_path(url)
    desktop = get_desktop_environment()
    if desktop == "GNOME":
        return start_process("gnome-open %s" % url)
    if desktop == "KDE":
        return start_process("kfmclient exec %s" % url)
    if sys.platform == "darwin":
        return start_process("open %s" % url)
    if sys.platform == "win32":
        # pylint: disable-msg=E1101
        return os.startfile(url)

    return webbrowser.open(url)

@memoize
def chardet_available():
    """Return True if chardet is available."""

    try:
        # pylint: disable-msg=W0612
        import chardet
        return True
    except Exception:
        return False

def compare_versions(x, y):
    """Compare version strings x and y.

    Used version number formats are MAJOR.MINOR, MAJOR.MINOR.PATCH and
    MAJOR.MINOR.PATCH.DATE, where all parts are expected to be integers.
    Return 1 if x newer, 0 if equal or -1 if y newer.
    """
    x = list(int(d) for d in x.split("."))
    y = list(int(d) for d in y.split("."))
    return cmp(x, y)

def connect(observer, observable, signal, *args):
    """Connect observable's signal to observer's callback method.

    If observable is a string, it should be an attribute of observer. If
    observable is not a string it should be the same as observer.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = observable + "_" + method_name
    method_name = ("_on_" + method_name).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

@memoize
def enchant_available():
    """Return True if enchant is available."""

    try:
        # pylint: disable-msg=W0612
        import enchant
        return True
    except Exception:
        return False

def exceptional(exception, handler, *data):
    """Decorator for handling exceptions raised  by function.

    handler will receive sys.exc_info() as the first argument and data as
    optional arguments. data are indexes of arguments and keys of keyword
    arguments to the function that should be passed to the handler as well.
    """
    def get_params(data, function, args, kwargs):
        params = list(args[x] for x in data if isinstance(x, int))
        for key in (x for x in data if isinstance(x, str)):
            if  key in kwargs:
                params.append(kwargs[key])
                continue
            spec = inspect.getargspec(function)
            index = spec[0].index(key) - len(spec[0])
            params.append(spec[3][index])
        return params

    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                params = get_params(data, function, args, kwargs)
                handler(sys.exc_info(), *params)
        return inner_wrapper

    return outer_wrapper

def gc_collected(function):
    """Decorator for functions to be followed by a gc.collect call."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        gc.collect()
        return value

    return wrapper

def get_chardet_version():
    """Return chardet version number as string or None."""

    try:
        import chardet
        return chardet.__version__
    except Exception:
        return None

@memoize
def get_default_encoding():
    """Get locale encoding or UTF-8 (as fallback)."""

    encoding = enclib.get_locale_python_name()
    if encoding is None:
        return "utf_8"
    return encoding

def get_desktop_environment():
    """Return 'GNOME', 'KDE' or None if unknown."""

    if os.getenv("GNOME_DESKTOP_SESSION_ID") is not None:
        return "GNOME"
    if os.getenv("KDE_FULL_SESSION") is not None:
        return "KDE"
    return None

def get_enchant_version():
    """Return enchant version number as string or None."""

    try:
        import enchant
        return enchant.__version__
    except Exception:
        return None

def get_ranges(lst):
    """Get a list of ranges in list."""

    if not lst:
        return []
    lst = get_sorted_unique(lst)
    ranges = [[lst.pop(0)]]
    i = 0
    for item in lst:
        if item == ranges[i][-1] + 1:
            ranges[i].append(item)
        else:
            ranges.append([item])
            i += 1
    return ranges

def get_sorted_unique(lst):
    """Get sorted list with duplicates removed."""

    lst = sorted(lst)
    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)
    return lst

def get_unique(lst):
    """Get list with duplicates removed."""

    lst = lst[:]
    for i in reversed(range(len(lst))):
        for j in range(0, i):
            if lst[j] == lst[i]:
                lst.pop(i)
                break
    return lst

def handle_read_io(exc_info, path):
    """Print IO error message to standard output."""

    print_read_io(path, exc_info[1].args[1])

def handle_read_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    if encoding is None:
        encoding = get_default_encoding()
    print_read_unicode(path, encoding)

def handle_write_io(exc_info, path):
    """Print IO error message to standard output."""

    print_write_io(path, exc_info[1].args[1])

def handle_write_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    if encoding is None:
        encoding = get_default_encoding()
    print_write_unicode(path, encoding)

def ignore_exceptions(*exceptions):
    """Decorator for ignoring exceptions raised  by function."""

    if not exceptions:
        exceptions = (Exception,)

    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exceptions:
                return None
        return inner_wrapper

    return outer_wrapper

def make_profile_dir():
    """Make profile directory paths.PROFILE_DIR.

    Raise OSError if unsuccessful.
    """
    makedirs(paths.PROFILE_DIR)

def makedirs(directory):
    """Make directory if it does not exist.

    Raise OSError if unsuccessful.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)

def path_to_uri(path):
    """Convert local filepath to URI."""

    return "file://%s" % urllib.quote(path)

def print_read_io(path, message):
    """Print IO error message to standard output."""

    print "Failed to read file '%s': %s." % (path, message)

def print_read_unicode(path, encoding):
    """Print Unicode error message to standard output."""

    print "Failed to decode file '%s' with codec '%s'." % (path, encoding)

def print_write_io(path, message):
    """Print IO error message to standard output."""

    print "Failed to write file '%s': %s." % (path, message)

def print_write_unicode(path, encoding):
    """Print Unicode error message to standard output."""

    print "Failed to encode file '%s' with codec '%s'." % (path, encoding)

def read(path, encoding=None):
    """Read file and return text.

    Raise IOError if reading fails.
    Raise UnicodeError if decoding fails.
    """
    if encoding is None:
        encoding = get_default_encoding()
    fobj = codecs.open(path, "r", encoding)
    try:
        return fobj.read().strip()
    finally:
        fobj.close()

def readlines(path, encoding=None):
    """Read file and return lines.

    Raise IOError if reading fails.
    Raise UnicodeError if decoding fails.
    """
    text = read(path, encoding)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n")

def shell_quote_path(path):
    """Quote and escape path for shell use."""

    if sys.platform != "win32":
        path = path.replace("\\", "\\\\")
        path = path.replace('"', '\\"')
    return '"%s"' % path

def start_process(command, **kwargs):
    """Start command as a new background subprocess.

    command and kwargs are passed to subprocess.Popen.__init__.
    Return subprocess.Popen instance.
    """
    return subprocess.Popen(
        command,
        shell=True,
        cwd=os.getcwd(),
        env=os.environ.copy(),
        universal_newlines=True,
        **kwargs)

def uri_to_path(uri):
    """Convert URI to local filepath."""

    return urlparse.urlsplit(urllib.unquote(uri))[2]

def write(path, text, encoding=None):
    """Write text to file.

    Raise IOError if writing fails.
    Raise UnicodeError if encoding fails.
    """
    if encoding is None:
        encoding = get_default_encoding()
    fobj = codecs.open(path, "w", encoding)
    try:
        return fobj.write(text)
    finally:
        fobj.close()

__all__ = sorted(list(set(dir()) - __all__))
