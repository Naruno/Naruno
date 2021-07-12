#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import json
import os
from lib.config_system import get_config

from config import *


def save_settings(new_settings):
    """
    Saves the settings.
    """

    os.chdir(get_config()["main_folder"])
    with open(SETTING_PATH, "w") as settings_file:
        json.dump(new_settings, settings_file, indent=4)


def create_and_save_the_settings(test_mode_settings=False, debug_mode_settings=False):
    """
    Creates and saves settings.
    """

    temp_json = {}
    temp_json["test_mode"] = test_mode_settings

    temp_json["debug_mode"] = debug_mode_settings

    temp_json["wallet"] = 0

    save_settings(temp_json)
    return temp_json


def test_mode(new_value):
    """
    Changes the test_mode setting.

    Inputs:
      * new_value: New value for the test_mode
    """

    settings = the_settings()
    settings["test_mode"] = new_value
    save_settings(settings)


def debug_mode(new_value):
    """
    Changes the debug_mode setting.

    Inputs:
      * new_value: New value for the debug_mode
    """

    settings = the_settings()
    settings["debug_mode"] = new_value
    save_settings(settings)


def change_wallet(new_value):
    """
    Changes the debug_mode setting.

    Inputs:
      * new_value: New value for the debug_mode
    """

    settings = the_settings()
    settings["wallet"] = new_value
    save_settings(settings)


def the_settings():
    """
    Returns the settings. If it doesn't exist, it creates,
    saves and returns.
    """

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(SETTING_PATH):
        return create_and_save_the_settings()
    else:
        with open(SETTING_PATH, "rb") as settings_file:
            return json.load(settings_file)
