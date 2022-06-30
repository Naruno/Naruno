#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import unittest

from lib.settings_system import save_settings, the_settings

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class Test_Settings(unittest.TestCase):
    def test_1_settings_by_creating_settings(self):
        temp_settings = the_settings()
        self.assertIsNotNone(temp_settings["test_mode"], "A problem on the test_mode.")
        self.assertIsNotNone(
            temp_settings["debug_mode"], "A problem on the debug_mode."
        )

    def test_2_settings_by_saving_and_getting_new_settings(self):
        backup_settings = the_settings()

        temp_settings = the_settings()

        temp_settings["test_mode"] = True
        temp_settings["debug_mode"] = True
        save_settings(temp_settings)

        temp_test_settings = the_settings()
        self.assertEqual(
            temp_test_settings["test_mode"],
            True,
            "A problem on the saving the settings.",
        )
        self.assertEqual(
            temp_test_settings["debug_mode"],
            True,
            "A problem on the saving the settings.",
        )

        temp_test_settings["test_mode"] = False
        temp_test_settings["debug_mode"] = False
        save_settings(temp_test_settings)

        temp_test_settings2 = the_settings()
        self.assertEqual(
            temp_test_settings2["test_mode"],
            False,
            "A problem on the saving the settings.",
        )
        self.assertEqual(
            temp_test_settings2["debug_mode"],
            False,
            "A problem on the saving the settings.",
        )

        temp_test_settings2["test_mode"] = backup_settings["test_mode"]
        temp_test_settings2["debug_mode"] = backup_settings["debug_mode"]
        save_settings(temp_test_settings2)


unittest.main(exit=False)
