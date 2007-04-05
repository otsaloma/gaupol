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


"""Miscellaneous functions and decorators."""


import cPickle
import codecs
import functools
import gc
import locale
import os
import re
import subprocess
import sys
import urllib
import urlparse
import webbrowser


# All defined variables and functions (Scroll to bottom).
__all__ = set(locals())

CHECK_CONTRACTS = True


def contractual(function):
    """Design by contract decorator for functions.

    function call will be wrapped around 'FUNCTION_NAME_require' and
    'FUNCTION_NAME_ensure' calls if such functions exist. The require function
    receives the same arguments as function, the ensure function will in
    addition receive function's return value as its first argument.

    Works only for module level functions, methods and classmethods;
    fails silently for nested functions and staticmethods!
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not CHECK_CONTRACTS:
            return function(*args, **kwargs)
        name = "%s_require" % function.__name__
        if (args and hasattr(args[0], function.__name__)):
            if function.__name__.startswith("__"):
                name = "_%s%s" % (args[0].__class__.__name__, name)
            if hasattr(args[0], name):
                getattr(args[0], name)(*args[1:], **kwargs)
        elif name in function.func_globals:
            function.func_globals[name](*args, **kwargs)
        value = function(*args, **kwargs)
        name = "%s_ensure" % function.__name__
        if (args and hasattr(args[0], function.__name__)):
            if function.__name__.startswith("__"):
                name = "_%s%s" % (args[0].__class__.__name__, name)
            if hasattr(args[0], name):
                getattr(args[0], name)(value, *args[1:], **kwargs)
        elif name in function.func_globals:
            function.func_globals[name](value, *args, **kwargs)
        return value

    return wrapper

def memoize(function):
    """Decorator for functions that cache their return values."""

    cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        params = (args, kwargs)
        if args and hasattr(args[0], function.__name__):
            params = (args[1:], kwargs)
        key = cPickle.dumps(params)
        if not key in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]

    return wrapper

def browse_url(url, browser=None):
    """Open URL in browser."""

    qurl = shell_quote(url)
    desktop = get_desktop_environment()
    if desktop == "GNOME":
        return start_process("gnome-open %s" % qurl)
    if desktop == "KDE":
        return start_process("kfmclient exec %s" % qurl)
    if sys.platform == "darwin":
        return start_process("open %s" % qurl)
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

def compare_versions_require(x, y):
    re_version = re.compile(r"^(\d+\.)+\d+$")
    assert re_version.match(x) is not None
    assert re_version.match(y) is not None

@contractual
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

@contractual
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

@memoize
def enchant_available():
    """Return True if enchant is available."""

    try:
        # pylint: disable-msg=W0612
        import enchant
        return True
    except Exception:
        return False

def gc_collected(function):
    """Decorator for functions to be followed by a gc.collect call."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        gc.collect()
        return value

    return wrapper

def get_chardet_version_ensure(value):
    assert isinstance(value, basestring)

@contractual
def get_chardet_version():
    """Return chardet version number as string or None."""

    try:
        import chardet
        return chardet.__version__
    except Exception:
        return None

def get_default_encoding_ensure(value):
    codecs.lookup(value)

@memoize
@contractual
def get_default_encoding():
    """Get the locale encoding or UTF-8 (as fallback)."""

    encoding = locale.getpreferredencoding()
    if encoding is None:
        return "utf_8"
    re_illegal = re.compile(r"[^a-z0-9_]")
    encoding = re_illegal.sub("_", encoding.lower())
    from encodings.aliases import aliases
    if encoding in aliases:
        encoding = aliases[encoding]
    return encoding

@memoize
def get_desktop_environment():
    """Return 'GNOME', 'KDE' or None if unknown."""

    if "GNOME_DESKTOP_SESSION_ID" in os.environ:
        return "GNOME"
    if "KDE_FULL_SESSION" in os.environ:
        return "KDE"
    return None

def get_enchant_version_ensure(value):
    assert isinstance(value, basestring)

@memoize
@contractual
def get_enchant_version():
    """Return enchant version number as string or None."""

    try:
        import enchant
        return enchant.__version__
    except Exception:
        return None

def get_ranges_require(lst):
    for item in lst:
        assert isinstance(item, int)

def get_ranges_ensure(value, lst):
    for item in value:
        assert item == range(item[0], item[-1] + 1)

@contractual
def get_ranges(lst):
    """Get a list of ranges in list of integers."""

    if not lst:
        return []
    lst = get_sorted_unique(lst)
    ranges = [[lst.pop(0)]]
    for item in lst:
        if item == ranges[-1][-1] + 1:
            ranges[-1].append(item)
        else:
            ranges.append([item])
    return ranges

def get_sorted_unique_ensure(value, lst):
    for item in value:
        assert value.count(item) == 1

@contractual
def get_sorted_unique(lst):
    """Get sorted list with duplicates removed."""

    lst = sorted(lst)
    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)
    return lst

def get_unique_ensure(value, lst):
    for item in value:
        assert value.count(item) == 1

@contractual
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

    print "Failed to read file '%s': %s." % (path, exc_info[1].args[1])

def handle_read_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    if encoding is None:
        encoding = get_default_encoding()
    print "Failed to decode file '%s' with codec '%s'." % (path, encoding)

def handle_write_io(exc_info, path):
    """Print IO error message to standard output."""

    print "Failed to write file '%s': %s." % (path, exc_info[1].args[1])

def handle_write_unicode(exc_info, path, encoding):
    """Print Unicode error message to standard output."""

    if encoding is None:
        encoding = get_default_encoding()
    print "Failed to encode file '%s' with codec '%s'." % (path, encoding)

def makedirs_ensure(value, directory):
    assert os.path.isdir(directory)

@contractual
def makedirs(directory):
    """Make directory if it does not exist.

    Raise OSError if unsuccessful.
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)

def notify_frozen(function):
    """Decorator for methods to be run in notify frozen state."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        frozen = args[0].freeze_notify()
        value = function(*args, **kwargs)
        args[0].thaw_notify(frozen)
        return value

    return wrapper

def path_to_uri(path):
    """Convert local filepath to URI."""

    return "file://%s" % urllib.quote(path)

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

def shell_quote(path):
    """Quote and escape path for shell use."""

    if sys.platform != "win32":
        path = path.replace("\\", "\\\\")
        path = path.replace('"', '\\"')
    return '"%s"' % path

def silent(*exceptions):
    """Decorator for ignoring exceptions raised  by function.

    If no exceptions specified, ignore Exception.
    Return None if an exception encountered.
    """
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

def write_ensure(value, path, text, encoding=None):
    assert os.path.isfile(path)

@contractual
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
