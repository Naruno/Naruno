#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


class Test_Settings(unittest.TestCase):

    def test_creating_settings(self):
        temp_settings = the_settings()
        self.assertIsNotNone(temp_settings["test_mode"], "A problem on the test_mode.")
        self.assertIsNotNone(temp_settings["debug_mode"], "A problem on the debug_mode.")

    def test_saving_settings(self):
        temp_settings = the_settings()
        temp_test_mode = temp_settings["test_mode"]
        temp_debug_mode = temp_settings["debug_mode"]

        test_mode(True)
        debug_mode(True)


        temp_test_settings = the_settings()
        self.assertEqual(temp_test_settings["test_mode"], True, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings["debug_mode"], True, "A problem on the saving the settings.")

        test_mode(False)
        debug_mode(False)


        temp_test_settings = the_settings()
        self.assertEqual(temp_test_settings["test_mode"], False, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings["debug_mode"], False, "A problem on the saving the settings.")

        test_mode(temp_test_mode)
        debug_mode(temp_debug_mode)



import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lib.settings_system import the_settings, test_mode, debug_mode
unittest.main(exit=False)
