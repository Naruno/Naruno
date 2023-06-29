#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import SETTING_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT

settings_db = KOT("settings", folder=get_config()["main_folder"] + "/db")

temp_json = {
    "test_mode": False,
    "funtionaltest_mode": False,
    "debug_mode": False,
    "wallet": 0,
    "save_blockshash": True,
    "mute_notifications": False,
    "dark_mode": True,
    "status_cache_time": 0,
    "status_cache": {},
    "status_working": False,
    "publisher_mode": False,
    "baklava": False,
    "disable_log_clearing": False,
    "baklava_users": False,
    "dont_save_blocks": False,
}


def save_settings(new_settings):
    """
    Saves the settings.
    """
    settings_db.set("settings", new_settings)


def create_and_save_the_settings(test_mode_settings=False,
                                 debug_mode_settings=True):
    """
    Creates and saves settings.
    """
    global temp_json

    save_settings(temp_json)

    t_mode_settings(test_mode_settings)
    d_mode_settings(debug_mode_settings)

    return temp_json


def t_mode_settings(new_value):
    """
    Changes the test_mode setting.

    Inputs:
      * new_value: New value for the test_mode
    """

    settings = the_settings()
    settings["test_mode"] = new_value
    save_settings(settings)


def d_mode_settings(new_value):
    """
    Changes the debug_mode setting.

    Inputs:
      * new_value: New value for the debug_mode
    """

    settings = the_settings()
    settings["debug_mode"] = new_value
    save_settings(settings)


def ft_mode_settings(new_value):
    """
    Changes the funtionaltest_mode setting.

    Inputs:
      * new_value: New value for the funtionaltest_mode
    """

    settings = the_settings()
    settings["funtionaltest_mode"] = new_value
    save_settings(settings)


def mt_settings(new_value):
    """
    Changes the mute_notifications setting.

    Inputs:
      * new_value: New value for the mute_notifications
    """

    settings = the_settings()
    settings["mute_notifications"] = new_value
    save_settings(settings)


def dark_mode_settings(new_value):
    """
    Changes the dark_mode setting.

    Inputs:
      * new_value: New value for the dark_mode
    """

    settings = the_settings()
    settings["dark_mode"] = new_value
    save_settings(settings)


def publisher_mode_settings(new_value):
    """
    Changes the publisher_mode setting.

    Inputs:
      * new_value: New value for the publisher_mode
    """

    settings = the_settings()
    settings["publisher_mode"] = new_value
    save_settings(settings)


def baklava_settings(new_value):
    """
    Changes the baklava setting.

    Inputs:
      * new_value: New value for the baklava
    """

    settings = the_settings()
    settings["baklava"] = new_value
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
    return settings["wallet"]


def the_settings():
    """
    Returns the settings. If it doesn't exist, it creates,
    saves and returns.
    """

    the_setting = settings_db.get("settings")
    if the_setting is None:
        create_and_save_the_settings()
        the_setting = settings_db.get("settings")

    missing = False
    for element in temp_json:
        if element not in the_setting:
            missing = True
            the_setting[element] = temp_json[element]
    if missing:
        save_settings(the_setting)

    return the_setting
