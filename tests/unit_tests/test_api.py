#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from api import app
import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class Test_API(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_api_debug_by_response_status_code(self):
        response = self.client.get("/wallet/print")
        self.assertEqual(response.status_code, 200, "A problem on the API.")


unittest.main(exit=False)
