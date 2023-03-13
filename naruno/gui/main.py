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
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp

import naruno.gui.the_naruno_gui_app
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.lib.safety import safety_check
from naruno.lib.settings_system import the_settings

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "450")
Config.set("graphics", "minimum_width", "700")
Config.set("graphics", "minimum_height", "450")
Config.set("input", "mouse", "mouse,disable_multitouch")

os.environ["NARUNO_ROOT"] = get_config()["main_folder"]

KV_DIR = f"{os.environ['NARUNO_ROOT']}/gui_lib/libs/kv/"

for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

KV = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import NarunoWelcomeScreen naruno.gui_lib.libs.baseclass.welcome_screen.NarunoWelcomeScreen
#:import NarunoRootScreen naruno.gui_lib.libs.baseclass.root_screen.NarunoRootScreen

ScreenManager:
    transition: FadeTransition()

    NarunoWelcomeScreen:
        name: "naruno register screen"

    NarunoRootScreen:
        name: "naruno root screen"

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
        self.title = "Naruno"
        self.icon = f"{os.environ['NARUNO_ROOT']}/gui_lib/images/logo.ico"

    def build(self):
        """
        Some configurations.
        """
        Window.borderless = True
        value = the_settings()["dark_mode"]


        for i in self.theme_cls.colors["Yellow"]:
            self.theme_cls.colors["Yellow"][i] = "#5C6BC0"
        for i in self.theme_cls.colors["Dark"]:
            self.theme_cls.colors["Dark"][i] = "#303030"

        self.theme_cls.theme_style = "Dark" if value else "Light"
        self.theme_cls.primary_palette = "Yellow"  # "Purple", "Red"

        self.FONT_PATH = os.path.join(os.environ["NARUNO_ROOT"], "gui_lib",
                                      "fonts")

        self.theme_cls.font_styles.update({
            "H1":
            [os.path.join(self.FONT_PATH, "Poppins-Light"), 96, False, -1.5],
            "H2":
            [os.path.join(self.FONT_PATH, "Poppins-Light"), 60, False, -0.5],
            "H3":
            [os.path.join(self.FONT_PATH, "Poppins-Regular"), 48, False, 0],
            "H4": [
                os.path.join(self.FONT_PATH, "Poppins-Regular"),
                34,
                False,
                0.25,
            ],
            "H5":
            [os.path.join(self.FONT_PATH, "Poppins-Regular"), 24, False, 0],
            "H6":
            [os.path.join(self.FONT_PATH, "Poppins-Bold"), 20, False, 0.15],
            "Subtitle1": [
                os.path.join(self.FONT_PATH, "Poppins-Regular"),
                16,
                False,
                0.15,
            ],
            "Subtitle2": [
                os.path.join(self.FONT_PATH, "Poppins-Medium"),
                14,
                False,
                0.1,
            ],
            "Body1": [
                os.path.join(self.FONT_PATH, "Poppins-Regular"),
                16,
                False,
                0.5,
            ],
            "Body2": [
                os.path.join(self.FONT_PATH, "Poppins-Light"),
                14,
                False,
                0.25,
            ],
            "Button": [
                os.path.join(self.FONT_PATH, "Poppins-Bold"),
                14,
                True,
                1.25,
            ],
            "Caption": [
                os.path.join(self.FONT_PATH, "Poppins-Regular"),
                12,
                False,
                0.4,
            ],
            "Overline": [
                os.path.join(self.FONT_PATH, "Poppins-Regular"),
                10,
                True,
                1.5,
            ],
        })

        return Builder.load_string(KV)

    def restart(self):
        self.root.clear_widgets()
        self.stop()
        naruno.gui.the_naruno_gui_app.the_naruno_gui = (
            GUI())
        return (naruno.gui.the_naruno_gui_app.
                the_naruno_gui.run())


def arguments():
    """
    This function parses the arguments and makes the directions.
    """

    parser = argparse.ArgumentParser(
        description=
        "Naruno is a lightning-fast, secure, and scalable blockchain that is able to create transaction proofs and verification via raw data and timestamp. We remove the archive nodes and lazy web3 integrations. With Naruno everyone can get the proof (5-10MB) of their transactions via their nodes and after everyone can use in another node for verification the raw data and timestamp. Also you can integrate your web3 applications with 4 code lines (just python for now) via our remote app system. Use the menu (-m) or GUI to gain full control and use the node, operation, etc."
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

    naruno.gui.the_naruno_gui_app.the_naruno_gui = GUI(
    )

    naruno.gui.the_naruno_gui_app.the_naruno_gui.run(
    )


def start():
    """
    Start the GUI mode.
    """

    logger.info("Starting GUI mode")
    arguments()


if __name__ == "__main__":
    start()
