#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sys
import time
from decentra_network.wallet.print_wallets import print_wallets
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest

import urllib

from decentra_network.api.main import start
from decentra_network.lib.clean_up import CleanUp_tests

import threading

class Test_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()
        backup = sys.argv
        sys.argv = [sys.argv[0]]
        cls.result = start(port=7777, test=True)
        cls.proc = threading.Thread(target=cls.result.run)
        cls.proc.start()
        sys.argv = backup
        time.sleep(2)
    
    @classmethod
    def tearDownClass(cls):
        cls.result.close()

    def test_api_debug_by_response_status_code(self):
        response = urllib.request.urlopen("http://localhost:7777/wallet/print")
        result = str(json.loads(response.read())).replace("'", """\"""")
        data = str(json.dumps(print_wallets()))
        self.assertEqual(result, data)



unittest.main(exit=False)
