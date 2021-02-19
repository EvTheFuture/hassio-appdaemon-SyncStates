"""
    SyncStates tries to syncronize states of entities when no read back
    function exists. A good exampe is when using multiple switches to
    control a single light with Telldus Tellstick 433MHz devices.

    Copyright (C) 2021    Magnus Sandin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Arguments in config file:

entity:                     M: entity id to update the state of
switches:                   M: list of entity id's to trigger on
debug:                      O: yes | no (activate debug logging)

"""
import appdaemon.plugins.hass.hassapi as hass

import copy
import json

VERSION = "0.1"


class SyncStates(hass.Hass):
    def initialize(self):
        if "debug" in self.args and self.args["debug"]:
            self.log("Setting log level to DEBUG")
            self.set_log_level("DEBUG")

        self.initialize_entities()

    def debug(self, text):
        self.get_main_log().debug(text)

    def warning(self, text):
        self.get_main_log().warning(text)

    def initialize_entities(self):
        self.debug("Setting up entities")

        for a in ["entity", "switches"]:
            if a not in self.args:
                self.error(f"Missing attribute '{a}', ABORTING...")
                return

        self.state_entity = self.args["entity"]
        if not self.entity_exists(self.state_entity):
            self.error(
                f"Entity '{self.entity_exists}' doesn't exist, ABORTING..."
            )

        switches = []

        # Handle both single switch and multiple switches
        if isinstance(self.args["switches"], list):
            for l in self.args["switches"]:
                if isinstance(l, dict):
                    switches += list(l.keys())
                elif isinstance(l, str):
                    switches += [l]
                else:
                    self.warning(f"Unknown switch config: {l}, IGNORING...")
        else:
            switches = [self.args["switches"]]

        self.switches = []
        for s in switches:
            if self.entity_exists(s):
                self.listen_state(callback=self.update_state, entity=s)
                self.switches += [s]
            else:
                self.warning(f"{s} does not exists, IGNORING...")


        self.debug(f"Switches configured: {self.switches}")

    def update_state(self, entity, attribute, old, new, kwargs):
        self.debug(f"State changed on '{entity}' to {new}, updating states...")

        self.set_state(self.state_entity, state=new)
        for s in self.switches:
            if s != entity:
                self.set_state(s, state=new)

