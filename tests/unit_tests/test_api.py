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

from decentra_network.wallet.ellipticcurve.get_saved_wallet import \
    get_saved_wallet
from decentra_network.wallet.ellipticcurve.save_wallet_list import \
    save_wallet_list
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create
from decentra_network.wallet.print_wallets import print_wallets

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import threading
import unittest
import urllib

from decentra_network.api.main import start
from decentra_network.lib.clean_up import CleanUp_tests


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

    def test_print_wallets_page(self):
        response = urllib.request.urlopen("http://localhost:7777/wallet/print")
        result = str(json.loads(response.read())).replace("'", """\"""")

        data = str(json.dumps(print_wallets()))

        self.assertEqual(result, data)

    def test_change_wallet_page(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        temp_private_key_2 = wallet_create(password)

        response = urllib.request.urlopen("http://localhost:7777/wallet/change/1")
        result = response.read()

        self.assertEqual(result, b"1\n")

        control = False
        if "CURRENTLY USED" in print_wallets()[1]:
            control = True

        self.assertTrue(control)
        save_wallet_list(original_saved_wallets)


unittest.main(exit=False)
