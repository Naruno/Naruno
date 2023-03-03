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


class Node_Scene(Naruno_Scene):

    def construct(self):
        self.set_title("Node")
        self.settings()
        self.intro_logo()
        self.intro_text()

        self.creating_nodes()
        self.create_node_connections()
        self.create_security_circles()
        self.creates_network()
        self.data_running_through_the_intersections_and_circles()

        self.clear_scren()
        self.intro_logo()


if __name__ == "__main__":
    Node_Scene().render()
