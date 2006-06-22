# Copyright (C) 2006 Osmo Salomaa
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


"""Functions for reading and writing files."""


import codecs
import os

from gaupol.base.paths import PROFILE_DIR


def make_profile_directory():
    """
    Make profile directory.

    Raise OSError if unsuccessful.
    """
    if os.path.isdir(PROFILE_DIR):
        return
    try:
        os.makedirs(PROFILE_DIR)
    except OSError, message:
        print 'Failed to create profile directory "%s": %s.' % (
            PROFILE_DIR, message)
        raise

def read(path, encoding, verbose=True):
    """
    Read file and return text.

    Raise IOError if reading fails.
    Raise UnicodeError if decoding fails.
    """
    try:
        fobj = codecs.open(path, 'r', encoding)
        try:
            return fobj.read().strip()
        finally:
            fobj.close()
    except IOError, (no, message):
        if verbose:
            print 'Failed to read file "%s": %s.' % (path, message)
        raise
    except UnicodeError, message:
        if verbose:
            print 'Failed to decode file "%s" with encoding "%s": %s.' % (
                path, encoding, message)
        raise

def write(path, encoding, text, verbose=True):
    """
    Write text to file.

    Raise IOError if writing fails.
    Raise UnicodeError if encoding fails.
    """
    try:
        fobj = codecs.open(path, 'w', encoding)
        try:
            fobj.write(text)
            return
        finally:
            fobj.close()
    except IOError, (no, message):
        if verbose:
            print 'Failed to write file "%s": %s.' % (path, message)
        raise
    except UnicodeError, message:
        if verbose:
            print 'Failed to encode file "%s" with encoding "%s": %s.' % (
                path, encoding, message)
        raise
