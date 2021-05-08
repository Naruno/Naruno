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
    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def config_class():
    temp_json = {}
    temp_json["main_folder"] = os.path.join(os.path.dirname(__file__), "..")

    return temp_json




def get_config():

    if not os.path.exists(CONFIG_PATH):
        temp_config_class = config_class()
        save_config(temp_config_class)
        return temp_config_class
    else:
        with open(CONFIG_PATH, 'rb') as config_file:
            return json.load(config_file)
