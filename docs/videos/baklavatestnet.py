#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
from unicodedata import name

from manim import *

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from naruno.lib.config_system import get_config
from docs.videos.main import Naruno_Scene


class BaklavaTestNet_Scene(Naruno_Scene):

    def construct(self):
        self.set_title("Baklava TestNet")
        self.settings()
        self.intro_logo()
        self.intro_text()

        self.creating_nodes()
        self.create_node_connections()
        self.turn_to_security_circle(circe_1="Baklava TestNet")
        self.turn_to_network()


        self.clear_scren()
        self.intro_logo()


if __name__ == "__main__":
    Baklava_TestNet_Scene().render()
