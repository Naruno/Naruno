#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import CONFIG_PATH
from naruno.lib.kot import KOT

config_db = KOT("config",
                folder=os.path.join(os.path.dirname(__file__), "..") + "/db")


def save_config(config):
    """
    Saves the settings.
    """

    config_db.set("config", config)


def create_and_save_the_configs():
    """
    Creates and saves configs.
    """

    temp_json = {"main_folder": os.path.join(os.path.dirname(__file__), "..")}
    save_config(temp_json)
    return temp_json


def get_config():
    """
    Returns the configs. If it doesn't exist, it creates,
    saves and returns.
    """

    record = config_db.get("config")
    if record is None:
        return create_and_save_the_configs()
    return record
