#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import os
from lib.config_system import get_config

from config import *

def save_settings(new_settings):
    os.chdir(get_config()["main_folder"])
    with open(SETTING_PATH, 'w') as settings_file:
        json.dump(new_settings, settings_file, indent=4)

def settings_class(test_mode_settings= False, debug_mode_settings= False):
    temp_json = {}
    temp_json["test_mode"] = test_mode_settings

    temp_json["debug_mode"] = debug_mode_settings


    save_settings(temp_json)
    return(temp_json)



def test_mode(value):
    settings = the_settings()
    settings["test_mode"] = value
    save_settings(settings)


def debug_mode(value):
    settings = the_settings()
    settings["debug_mode"] = value
    save_settings(settings)






def the_settings():
    os.chdir(get_config()["main_folder"])

    if not os.path.exists(SETTING_PATH):
        return settings_class()
    else:
        with open(SETTING_PATH, 'rb') as settings_file:
            return json.load(settings_file)
