#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest

from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.config_system import get_config


class Test_Config(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    def test_config_by_getting_and_saving_main_folder_config(self):
        finded_true_folder = False

        temp_config = get_config()

        os.chdir(temp_config["main_folder"])

        obj = os.scandir()
        for entry in obj:
            if entry.name == "db":
                finded_true_folder = True

        self.assertEqual(finded_true_folder, True, "A problem on the config.")


backup = sys.argv
sys.argv = [sys.argv[0]]
unittest.main(exit=False)
sys.argv = backup
