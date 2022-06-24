#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import unittest


class Test_Decentra_Network_Local(unittest.TestCase):

    def test_1_multiple_transaction_with_time_difference(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        wallet_2_json = json.loads(urllib.request.urlopen("http://localhost:8101/wallet/create/123").read().decode())
        wallet_2_address = wallet_2_json[0].replace("0) ", "").replace(" - CURRENTLY USED\n", "")

        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
        time.sleep(25)
        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8101/wallet/balance").read().decode())
        self.assertEqual(balance_wallet_1,4000.0,"A problem in same network one transaction -1.")


        time.sleep(45)


        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
        time.sleep(25)
        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8101/wallet/balance").read().decode())
        self.assertEqual(balance_wallet_1,9000.0,"A problem in same network one transaction -3.")

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..","..",".."))
import urllib.request, json
import time
from auto_builders.local import Decentra_Network_Local

temp_environment = Decentra_Network_Local(7, 2)
temp_environment.delete()
temp_environment.install()
temp_environment.run()
temp_environment.start()

unittest.main(exit=False)