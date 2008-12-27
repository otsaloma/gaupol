# Copyright (C) 2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Finding activating, storing and deactivating extensions."""

import gaupol
import inspect
import os
import re
import sys
import traceback

__all__ = ("ExtensionManager", "ExtensionMetadata",)


class ExtensionManager(object):

    """Finding activating, storing and deactivating extensions.

    Instance attribute '_active' is a dictionary mapping module names to
    Extension instances for active extensions. '_metadata' is a dictionary
    mapping module names to Metadata instances, which are available regarless
    of whether the extensions is active or not.

    '_dependants' is a dictionary mapping modules to a list of other modules
    depending on them. '_inferior' is a list of modules activated just to
    satisfy a dependency of another module. Dependency handling is done
    automatically with 'setup_extension[s]' and 'teardown_extension[s]'.
    """

    __metaclass__ = gaupol.Contractual
    _global_dir = os.path.join(gaupol.LIB_DIR, "extensions")
    _local_dir = os.path.join(gaupol.PROFILE_DIR, "extensions")
    _re_comment = re.compile(r"#.*$")

    def __init__(self, application):

        self.application = application
        self._active = {}
        self._dependants = {}
        self._inferior = []
        self._metadata = {}

    def _find_extensions_in_directory(self, directory):
        """Find all extensions in directory and parse their metadata files."""

        is_metadata_file = lambda x: x.endswith(".gaupol-extension")
        for (root, dirs, files) in os.walk(directory):
            for name in filter(is_metadata_file, files):
                path = os.path.abspath(os.path.join(root, name))
                self._parse_metadata(path)

    def _parse_metadata(self, path):
        """Parse extension metadata file."""

        try: lines = gaupol.util.readlines(path, "utf_8", None)
        except UnicodeError: # Metadata file must be UTF-8.
            args = (sys.exc_info(), path, "utf_8")
            return gaupol.gtk.util.print_read_unicode(*args)
        lines = [self._re_comment.sub("", x) for x in lines]
        lines = [x.strip() for x in lines]
        metadata = ExtensionMetadata()
        metadata.path = path
        for line in (x for x in lines if x):
            if line.startswith("["): continue
            name, value = unicode(line).split("=", 1)
            name = (name[1:] if name.startswith("_") else name)
            metadata.set_field(name, value)
        self._store_metadata(path, metadata)

    def _store_metadata(self, path, metadata):
        """Store metadata to instance variables after validation."""

        def discard_extension(name):
            message = "Field '%s' missing in file '%s', dicarding extension."
            print message % (name, path)
        if not metadata.has_field("GaupolVersion"):
            return discard_extension("GaupolVersion")
        if not metadata.has_field("Module"):
            return discard_extension("Module")
        if not metadata.has_field("Name"):
            return discard_extension("Name")
        if not metadata.has_field("Description"):
            return discard_extension("Description")
        module = metadata.get_field("Module")
        self._metadata[module] = metadata

    def find_extensions(self):
        """Find all extensions and parse their metadata files."""

        self._find_extensions_in_directory(self._global_dir)
        self._find_extensions_in_directory(self._local_dir)

    def get_metadata(self, module):
        """Return the metadata instance for module."""

        return self._metadata[module]

    def get_modules(self):
        """Return a list of all extension module names."""

        return self._metadata.keys()

    def has_help_require(self, module):
        assert module in self._active
        assert module in self._metadata

    def has_help(self, module):
        """Return True if extension can display documentation."""

        extension = self._active[module]
        child = extension.show_help.im_func
        parent = gaupol.gtk.Extension.show_help.im_func
        return child is not parent

    def has_preferences_dialog_require(self, module):
        assert module in self._active
        assert module in self._metadata

    def has_preferences_dialog(self, module):
        """Return True if extension can display a preferences dialog."""

        extension = self._active[module]
        child = extension.show_preferences_dialog.im_func
        parent = gaupol.gtk.Extension.show_preferences_dialog.im_func
        return child is not parent

    def is_active(self, module):
        """Return True if extension is active, False if not."""

        return (module in self._active)

    def setup_extension_require(self, module, inferior=False):
        assert module in self._metadata

    def setup_extension(self, module, inferior=False):
        """Import and setup extension by module name.

        inferior should be True if called just to satisfy a dependency.
        Setup all modules required by module.
        Return silently if module is already set up.
        """
        if module in self._active: return
        metadata = self._metadata[module]
        for m in metadata.get_field_list("Requires", ()):
            if not m in self._active:
                self.setup_extension(m, True)
            self._dependants[m].append(module)
        directory = os.path.dirname(metadata.path)
        sys.path.insert(0, directory)
        try: mobj = __import__(module, {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        for attribute in dir(mobj):
            if attribute.startswith("_"): continue
            value = getattr(mobj, attribute)
            if not inspect.isclass(value): continue
            if issubclass(value, gaupol.gtk.Extension):
                extension = value()
                extension.setup(self.application)
                self._active[module] = extension
                self._dependants[module] = []
        if inferior:
            self._inferior.append(module)
        elif module in self._inferior:
            self._inferior.remove(module)

    def setup_extensions(self):
        """Import and setup all extensions configured as active."""

        for module in gaupol.gtk.conf.extensions.active:
            if not module in self._metadata:
                gaupol.gtk.conf.extensions.active.remove(module)
            else: self.setup_extension(module)

    def show_help_require(self, module):
        assert module in self._active
        assert module in self._metadata

    def show_help(self, module):
        """Show documentation on using extension."""

        extension = self._active[module]
        extension.show_help()

    def show_preferences_dialog_require(self, module, parent):
        assert module in self._active
        assert module in self._metadata

    def show_preferences_dialog(self, module, parent):
        """Show a preferences dialog for configuring extension."""

        extension = self._active[module]
        extension.show_preferences_dialog(parent)

    def teardown_extension_require(self, module, force=True):
        assert module in self._metadata

    def teardown_extension(self, module, force=True):
        """Teardown extension by module name.

        If not using force (which should only be used with care),
        raise DependencyError if module is required by other modules.
        Teardown no longer used dependencies of module.
        Return silently if module is already torn down.
        """
        if not module in self._active: return
        if self._dependants[module]:
            if not force: raise gaupol.gtk.DependencyError
            for user in self._dependants[module]:
                self.teardown_extension(user)
        extension = self._active[module]
        extension.teardown(self.application)
        del self._active[module]
        del self._dependants[module]
        for dependency in self._dependants.keys():
            # Teardown no longer used dependencies.
            if module in self._dependants[dependency]:
                self._dependants[dependency].remove(module)
            if self._dependants[dependency]: continue
            if not dependency in self._inferior: continue
            self.teardown_extension(dependency)
        if module in self._inferior:
            self._inferior.remove(module)

    def teardown_extensions(self):
        """Teardown all active extensions."""

        for module in self._active.keys():
            self.teardown_extension(module, True)

    def update_extensions(self, page):

        for name, extension in self._active.iteritems():
            extension.update(self.application, page)


class ExtensionMetadata(gaupol.MetadataItem):

    """Extension metadata specified in a separate desktop-style file."""

    def __init__(self, fields=None):

        gaupol.MetadataItem.__init__(self, fields)
        self.path = None
