#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


class Test_Settings(unittest.TestCase):

    def test_creating_settings(self):
        temp_settings = the_settings()
        self.assertIsNotNone(temp_settings["test_mode"], "A problem on the test_mode.")
        self.assertIsNotNone(temp_settings["debug_mode"], "A problem on the debug_mode.")

    def test_saving_settings(self):
        backup_settings = the_settings()

        temp_settings = the_settings()


        temp_settings["test_mode"] = True
        temp_settings["debug_mode"] = True
        save_settings(temp_settings)



        temp_test_settings = the_settings()
        self.assertEqual(temp_test_settings["test_mode"], True, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings["debug_mode"], True, "A problem on the saving the settings.")


        temp_test_settings["test_mode"] = False
        temp_test_settings["debug_mode"] = False
        save_settings(temp_test_settings)



        temp_test_settings2 = the_settings()
        self.assertEqual(temp_test_settings2["test_mode"], False, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings2["debug_mode"], False, "A problem on the saving the settings.")

        temp_test_settings2["test_mode"] = backup_settings["test_mode"]
        temp_test_settings2["debug_mode"] = backup_settings["debug_mode"]
        save_settings(temp_test_settings2)




import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lib.settings_system import the_settings, save_settings
unittest.main(exit=False)
