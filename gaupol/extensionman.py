# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Finding activating, storing and deactivating extensions."""

import aeidon
import gaupol
import importlib.machinery
import inspect
import os
import re

__all__ = ("ExtensionManager", "ExtensionMetadata",)


class ExtensionManager:

    """
    Finding activating, storing and deactivating extensions.

    :ivar _active: Dictionary mapping module names to extensions
    :ivar _dependants: Dictionary mapping module names to a list of others
    :ivar _metadata: Dictionary mapping module names to metadata items
    :ivar _slaves: List of modules activated to satisfy a dependency
    """
    _global_dir = os.path.join(aeidon.DATA_DIR, "extensions")
    _local_dir  = os.path.join(aeidon.DATA_HOME_DIR, "extensions")
    _re_comment = re.compile(r"#.*$")

    def __init__(self, application):
        """Initialize an :class:`ExtensionManager` instance."""
        self._active = {}
        self.application = application
        self._dependants = {}
        self._metadata = {}
        self._slaves = []

    def find_extensions(self):
        """Find all extensions and parse their metadata files."""
        self._find_extensions_in_directory(self._global_dir)
        self._find_extensions_in_directory(self._local_dir)

    def _find_extensions_in_directory(self, directory):
        """Find all extensions in `directory` and parse their metadata."""
        def is_metadata_file(path):
            return (path.endswith(".extension") or
                    path.endswith(".extension.in"))
        for root, dirs, files in os.walk(directory):
            files = list(filter(is_metadata_file, files))
            for name in [x for x in files if x.endswith(".in")]:
                # If both untranslated and translated metadata files are found,
                # load extension only from the translated one.
                if name[:-3] in files:
                    files.remove(name)
            for name in files:
                path = os.path.abspath(os.path.join(root, name))
                self._parse_metadata(path)

    def get_metadata(self, module):
        """Return an :class:`ExtensionMetadata` instance for `module`."""
        return self._metadata[module]

    def get_modules(self):
        """Return a list of all extension module names."""
        return list(self._metadata.keys())

    def has_help(self, module):
        """Return ``True`` if extension can display documentation."""
        extension = self._active[module]
        return (extension.__class__.show_help is not
                gaupol.Extension.show_help)

    def has_preferences_dialog(self, module):
        """Return True if extension can display a preferences dialog."""
        extension = self._active[module]
        return (extension.__class__.show_preferences_dialog is not
                gaupol.Extension.show_preferences_dialog)

    def is_active(self, module):
        """Return ``True`` if extension is active, ``False`` if not."""
        return (module in self._active)

    def _parse_metadata(self, path):
        """Parse extension metadata file at `path`."""
        lines = aeidon.util.readlines(path, "utf_8", fallback=None)
        lines = [self._re_comment.sub("", x) for x in lines]
        lines = [x.strip() for x in lines]
        metadata = ExtensionMetadata()
        metadata.path = path
        for line in (x for x in lines if x):
            if line.startswith("["): continue
            name, value = line.split("=", 1)
            name = name[1:] if name.startswith("_") else name
            metadata.set_field(name, value)
        module = metadata.get_field("Module")
        self._metadata[module] = metadata

    @aeidon.deco.silent(ImportError, tb=True)
    def setup_extension(self, module, slave=False):
        """Import and setup extension by module name."""
        if module in self._active: return
        metadata = self._metadata[module]
        for dependency in metadata.get_field_list("Requires", ()):
            if not dependency in self._active:
                self.setup_extension(dependency, slave=True)
                self._slaves.append(dependency)
            self._dependants[dependency].append(module)
        directory = os.path.dirname(metadata.path)
        name = "gaupol.extension.{:s}".format(module)
        path = os.path.join(directory, "{}.py".format(module))
        loader = importlib.machinery.SourceFileLoader(name, path)
        module_object = loader.load_module(name)
        for attribute in dir(module_object):
            if attribute.startswith("_"): continue
            value = getattr(module_object, attribute)
            if not inspect.isclass(value): continue
            if issubclass(value, gaupol.Extension):
                extension = value()
                extension.setup(self.application)
                self._active[module] = extension
                self._dependants[module] = []
        self.application.update_gui()

    def setup_extensions(self):
        """Import and setup all extensions configured as active."""
        active = gaupol.conf.extensions.active[:]
        gaupol.conf.extensions.active.clear()
        for module in sorted(set(active) & self._metadata.keys()):
            self.setup_extension(module)
            gaupol.conf.extensions.active.append(module)

    def show_help(self, module):
        """Show documentation on using extension."""
        extension = self._active[module]
        extension.show_help()

    def show_preferences_dialog(self, module, parent):
        """Show a preferences dialog for configuring extension."""
        extension = self._active[module]
        extension.show_preferences_dialog(parent)

    def teardown_extension(self, module):
        """Teardown extension by module name."""
        if not module in self._active: return
        for user in self._dependants[module]:
            # Teardown all extensions depending on this one.
            self.teardown_extension(user)
        if not module in self._active: return
        extension = self._active[module]
        extension.teardown(self.application)
        del self._active[module]
        del self._dependants[module]
        for dependency in list(self._dependants.keys()):
            # Teardown no longer used dependencies.
            if module in self._dependants[dependency]:
                self._dependants[dependency].remove(module)
            if self._dependants[dependency]: continue
            if not dependency in self._slaves: continue
            self.teardown_extension(dependency)
        if module in self._slaves:
            self._slaves.remove(module)
        gaupol.conf.write_to_file()

    def teardown_extensions(self):
        """Teardown all active extensions."""
        for module in list(self._active.keys()):
            self.teardown_extension(module)

    def update_extensions(self, page):
        """Call ``update`` on all active extensions."""
        for name, extension in self._active.items():
            extension.update(self.application, page)


class ExtensionMetadata(aeidon.MetadataItem):

    """Extension metadata specified in a separate desktop-style file."""

    def __init__(self, fields=None):
        """Initialize an :class:`ExtensionMetadata` instance."""
        aeidon.MetadataItem.__init__(self, fields)
        self.path = None
