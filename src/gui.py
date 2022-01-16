#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from kivy import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '450')
Config.set('graphics', 'minimum_width', '700')
Config.set('graphics', 'minimum_height', '450')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.lang import Builder

from kivymd.app import MDApp

from lib.config_system import get_config
os.environ["DECENTRA_ROOT"] = get_config()["main_folder"]


KV_DIR = f"{os.environ['DECENTRA_ROOT']}/gui_lib/libs/kv/"

for kv_file in os.listdir(KV_DIR):
    with open(os.path.join(KV_DIR, kv_file), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

KV = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import DecentraWelcomeScreen gui_lib.libs.baseclass.welcome_screen.DecentraWelcomeScreen
#:import DecentraRootScreen gui_lib.libs.baseclass.root_screen.DecentraRootScreen

ScreenManager:
    transition: FadeTransition()

    DecentraWelcomeScreen:
        name: "decentra register screen"

    DecentraRootScreen:
        name: "decentra root screen"

"""


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

        self.theme_cls.primary_palette = "Green"
        FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

        self.theme_cls.font_styles.update(
            {
                "H1": [FONT_PATH + "RobotoCondensed-Light", 96, False, -1.5],
                "H2": [FONT_PATH + "RobotoCondensed-Light", 60, False, -0.5],
                "H3": [FONT_PATH + "Eczar-Regular", 48, False, 0],
                "H4": [FONT_PATH + "RobotoCondensed-Regular", 34, False, 0.25],
                "H5": [FONT_PATH + "RobotoCondensed-Regular", 24, False, 0],
                "H6": [FONT_PATH + "RobotoCondensed-Bold", 20, False, 0.15],
                "Subtitle1": [
                    FONT_PATH + "RobotoCondensed-Regular",
                    16,
                    False,
                    0.15,
                ],
                "Subtitle2": [
                    FONT_PATH + "RobotoCondensed-Medium",
                    14,
                    False,
                    0.1,
                ],
                "Body1": [FONT_PATH + "Eczar-Regular", 16, False, 0.5],
                "Body2": [FONT_PATH + "RobotoCondensed-Light", 14, False, 0.25],
                "Button": [FONT_PATH + "RobotoCondensed-Bold", 14, True, 1.25],
                "Caption": [
                    FONT_PATH + "RobotoCondensed-Regular",
                    12,
                    False,
                    0.4,
                ],
                "Overline": [
                    FONT_PATH + "RobotoCondensed-Regular",
                    10,
                    True,
                    1.5,
                ],
            }
        )
        
        return Builder.load_string(KV)

def start():
    """
    Start the GUI mode.
    """
    
    GUI().run()

if __name__ == '__main__':
    start()
