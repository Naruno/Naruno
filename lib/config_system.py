#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pickle
import os


from config import *

class config_class:
    def __init__(self):
        self.main_folder = None

def save_folder(config):
    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")
    config.main_folder = os.getcwd()
    with open(CONFIG_PATH, 'wb') as config_file:
        pickle.dump(config, config_file)
        return config


def get_config():

    if not os.path.exists(CONFIG_PATH):
        return save_folder(config_class()) 

    temp_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(temp_folder)
    os.chdir("..")
    with open(CONFIG_PATH, 'rb') as config_file:
        return pickle.load(config_file)





if __name__ == '__main__':
    try:
        get_config()
    except:
        save_folder(config_class())
