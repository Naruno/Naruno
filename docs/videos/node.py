import os
import sys
from unicodedata import name

from manim import *

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from decentra_network.lib.config_system import get_config
from docs.videos.main import Decentra_Network_Scene


class Node_Scene(Decentra_Network_Scene):
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
