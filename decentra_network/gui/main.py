#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import argparse

os.environ["KIVY_NO_ARGS"] = "1"
from kivy import Config
from kivy.lang import Builder
from kivymd.app import MDApp

from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from decentra_network.lib.safety import safety_check
from decentra_network.lib.settings_system import the_settings

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "450")
Config.set("graphics", "minimum_width", "700")
Config.set("graphics", "minimum_height", "450")
Config.set("input", "mouse", "mouse,disable_multitouch")

os.environ["DECENTRA_ROOT"] = get_config()["main_folder"]

KV_DIR = f"{os.environ['DECENTRA_ROOT']}/gui_lib/libs/kv/"

for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

KV = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import DecentraWelcomeScreen decentra_network.gui_lib.libs.baseclass.welcome_screen.DecentraWelcomeScreen
#:import DecentraRootScreen decentra_network.gui_lib.libs.baseclass.root_screen.DecentraRootScreen

ScreenManager:
    transition: FadeTransition()

    DecentraWelcomeScreen:
        name: "decentra register screen"

    DecentraRootScreen:
        name: "decentra root screen"

"""

logger = get_logger("GUI")


class GUI(MDApp):
    """
    An MDApp based  GUI class.
    GUI class consists of 2 elements:
      * title: Title of the app.
      * icon: icon of the app.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Decentra Network"
        self.icon = f"{os.environ['DECENTRA_ROOT']}/gui_lib/images/logo.ico"

    def build(self):
        """
        Some configurations.
        """
        value = the_settings()["dark_mode"]
        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"

        FONT_PATH = os.path.join(os.environ["DECENTRA_ROOT"], "gui_lib",
                                 "fonts")

        self.theme_cls.font_styles.update({
            "H1": [os.path.join(FONT_PATH, "Poppins-Light"), 96, False, -1.5],
            "H2": [os.path.join(FONT_PATH, "Poppins-Light"), 60, False, -0.5],
            "H3": [os.path.join(FONT_PATH, "Poppins-Regular"), 48, False, 0],
            "H4":
            [os.path.join(FONT_PATH, "Poppins-Regular"), 34, False, 0.25],
            "H5": [os.path.join(FONT_PATH, "Poppins-Regular"), 24, False, 0],
            "H6": [os.path.join(FONT_PATH, "Poppins-Bold"), 20, False, 0.15],
            "Subtitle1": [
                os.path.join(FONT_PATH, "Poppins-Regular"),
                16,
                False,
                0.15,
            ],
            "Subtitle2": [
                os.path.join(FONT_PATH, "Poppins-Medium"),
                14,
                False,
                0.1,
            ],
            "Body1":
            [os.path.join(FONT_PATH, "Poppins-Regular"), 16, False, 0.5],
            "Body2":
            [os.path.join(FONT_PATH, "Poppins-Light"), 14, False, 0.25],
            "Button":
            [os.path.join(FONT_PATH, "Poppins-Bold"), 14, True, 1.25],
            "Caption":
            [os.path.join(FONT_PATH, "Poppins-Regular"), 12, False, 0.4],
            "Overline":
            [os.path.join(FONT_PATH, "Poppins-Regular"), 10, True, 1.5],
        })

        return Builder.load_string(KV)

    def restart(self):
        self.root.clear_widgets()
        self.stop()
        return GUI().run()


def arguments():
    """
    This function parses the arguments and makes the directions.
    """

    parser = argparse.ArgumentParser(
        description=
        "This is an open source decentralized application network. In this network, you can develop and publish decentralized applications. Use the menu (-m) or GUI to gain full control and use the node, operation, etc."
    )

    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        help="Interface",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="Timeout",
    )

    args = parser.parse_args()

    safety_check(args.interface, args.timeout)

    GUI().run()


def start():
    """
    Start the GUI mode.
    """

    logger.info("Starting GUI mode")
    arguments()


if __name__ == "__main__":
    start()
