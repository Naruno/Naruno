#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


class Test_Config(unittest.TestCase):


    def test_getting_and_saving_config(self):
        finded_true_folder = False

        temp_config = get_config()

        os.chdir(temp_config["main_folder"])

        obj = os.scandir()
        for entry in obj :
            if entry.name == "wallet":
                finded_true_folder = True

        self.assertEqual(finded_true_folder,True,"A problem on the config.")


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lib.config_system import get_config    
unittest.main(exit=False)
