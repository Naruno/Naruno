#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os


from config import *



def save_config(config):
    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config, config_file)

def config_class():
    temp_json = {}
    temp_json["main_folder"] = os.getcwd()

    return temp_json




def get_config():
    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")

    if not os.path.exists(CONFIG_PATH):
        temp_config_class = config_class()
        with open(CONFIG_PATH, 'w') as config_file:
            json.dump(temp_config_class, config_file)
        return temp_config_class

    
    with open(CONFIG_PATH, 'rb') as config_file:
        return json.load(config_file)
