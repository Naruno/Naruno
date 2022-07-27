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

from decentra_network.api.main import app
from decentra_network.lib.clean_up import CleanUp_tests


class Test_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

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
