#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest


class Test_Config(unittest.TestCase):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
    def tearDown(self):
        self.ctx.pop()

    def test_api(self):
        backup_settings = the_settings()
        print(backup_settings["debug_mode"])
        response = self.client.get("/settings/debug/on")
        if backup_settings["debug_mode"] == True:
            self.client.get("/settings/debug/on")
        else:
            self.client.get("/settings/debug/off")
        self.assertEqual(response.status_code, 200, "A problem on the API.")


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..","src"))
from api import app
from lib.settings_system import the_settings
unittest.main(exit=False)