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
import unittest
import urllib.request

from auto_builders.local import Decentra_Network_Local

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


class Test_Decentra_Network_Local(unittest.TestCase):

    def test_1_different_network_one_transacton(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        success = False
        for i in range(1):
            temp_environment = Decentra_Network_Local()
            temp_environment.delete()
            temp_environment.install()
            temp_environment.run()
            temp_environment.start()

            wallet_2_json = json.loads(
                urllib.request.urlopen(
                    "http://localhost:8101/wallet/print").read().decode())
            wallet_2_address = (wallet_2_json[0].replace("0) ", "").replace(
                " - CURRENTLY USED\n", ""))

            for i in range(2):
                urllib.request.urlopen(
                    f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123"
                )

                time.sleep(25)

            balance_wallet_1 = json.loads(
                urllib.request.urlopen(
                    "http://localhost:8101/wallet/balance").read().decode())

            if balance_wallet_1 == 9000.0:
                success = True

        self.assertEqual(success, True,
                         "A problem in different network one transaction.")


unittest.main(exit=False)
