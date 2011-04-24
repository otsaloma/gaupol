# Copyright (C) 2011 Osmo Salomaa
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

"""Using custom, non-standard framerates."""

import aeidon
import gaupol
import gtk
import os
_ = aeidon.i18n._


class CustomFrameratesExtension(gaupol.Extension):

    """Using custom, non-standard framerates."""

    def __init__(self):
        """Initialize a :class:`CustomFrameratesExtension` object."""
        self._action_group = None
        self._conf = None
        self._framerates = []
        self._uim_ids = []
        self.application = None

    def _clear_attributes(self):
        """Clear values of attributes."""
        self._action_group = None
        self._conf = None
        self._framerates = []
        self._uim_ids = []
        self.application = None

    def _init_framerates(self):
        """Initialize framerates and corresponding UI manager actions."""
        self._action_group = gtk.ActionGroup("custom-framerates")
        self.application.uim.insert_action_group(self._action_group, -1)
        tooltip = _("Calculate nonnative units with a framerate of %.3f fps")
        directory = os.path.abspath(os.path.dirname(__file__))
        ui_file_path = os.path.join(directory, "custom-framerates.ui.xml")
        ui_xml_template = open(ui_file_path, "r").read()
        for value in sorted(self._conf.framerates):
            name = "FPS_%s" % (("%.3f" % value).replace(".", "_"))
            if hasattr(aeidon.framerates, name):
                print "Framerate %.3f already exists!" % value
                continue
            setattr(aeidon.framerates, name, aeidon.EnumerationItem())
            framerate = getattr(aeidon.framerates, name)
            framerate.label = "%.3f fps" % value
            framerate.mpsub = "%.2f" % value
            framerate.value = float(value)
            self._framerates.append(framerate)
            action = gtk.RadioAction(name=name.replace("FPS", "show_framerate"),
                                     label=framerate.label,
                                     tooltip=(tooltip % value),
                                     stock_id=None,
                                     value=int(framerate))

            group = "show_framerate_23_976"
            action.set_group(self.application.get_action(group))
            action.framerate = framerate
            self._action_group.add_action(action)
            ui_xml = ui_xml_template % (name.replace("FPS_", ""),
                                        action.get_name())

            uim_id = self.application.uim.add_ui_from_string(ui_xml)
            self._uim_ids.append(uim_id)
            gaupol.framerate_actions[framerate] = action.get_name()
            self.application.framerate_combo.append_text(action.get_label())
        self.application.uim.ensure_update()
        self.application.set_menu_notify_events("custom-framerates")

    def setup(self, application):
        """Setup extension for use with `application`."""
        gaupol.conf.register_extension("custom_framerates",
                                       {"framerates": [48.0]})

        self._conf = gaupol.conf.extensions.custom_framerates
        self.application = application
        self._init_framerates()

    def teardown(self, application):
        """End use of extension with `application`."""
        store = application.framerate_combo.get_model()
        for framerate in reversed(self._framerates):
            store.remove(store.get_iter(framerate))
            del gaupol.framerate_actions[framerate]
            name = "FPS_%s" % (("%.3f" % framerate.value).replace(".", "_"))
            delattr(aeidon.framerates, name)
        for uim_id in self._uim_ids:
            application.uim.remove_ui(uim_id)
        application.uim.remove_action_group(self._action_group)
        application.uim.ensure_update()
        self._clear_attributes()
