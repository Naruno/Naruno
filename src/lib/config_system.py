#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import json
import os

from config import *


def save_config(config):
    """
    Saves the settings.
    """

    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config, config_file, indent=4)


def create_and_save_the_configs():
    """
    Creates and saves configs.
    """

    temp_json = {}
    temp_json["main_folder"] = os.path.join(os.path.dirname(__file__), "..")

    save_config(temp_json)
    return temp_json


def get_config():
    """
    Returns the configs. If it doesn't exist, it creates,
    saves and returns.
    """

    if not os.path.exists(CONFIG_PATH):
        return create_and_save_the_configs()
    else:
        with open(CONFIG_PATH, "rb") as config_file:
            return json.load(config_file)
