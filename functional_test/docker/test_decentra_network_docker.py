#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import unittest


class Test_Decentra_Network_Docker(unittest.TestCase):

    def test_1_different_network_one_transacton(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        Decentra_Network_Docker()
        wallet_2_json = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/create/123").read().decode())
        wallet_2_address = wallet_2_json[0].replace("0) ", "").replace(" - CURRENTLY USED\n", "")
        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")

        time.sleep(15)


        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())

        self.assertEqual(balance_wallet_1,4000.0,"A problem in different network one transaction.")

    def test_2_different_network_multi_transacton(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        Decentra_Network_Docker()
        wallet_2_json = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/print").read().decode())
        wallet_2_address = wallet_2_json[0].replace("0) ", "").replace(" - CURRENTLY USED\n", "")



        for i in range(4):
            urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
            time.sleep(15)

        time.sleep(35)


        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())

        self.assertEqual(balance_wallet_1,19000.0,"A problem in different network multi transaction.")



    def test_3_same_network__one_and_multi_transacton(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        Decentra_Network_Docker()
        wallet_2_json = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/create/123").read().decode())
        wallet_2_address = wallet_2_json[0].replace("0) ", "").replace(" - CURRENTLY USED\n", "")
        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")

        time.sleep(15)


        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())

        self.assertEqual(balance_wallet_1,4000.0,"A problem in same network one and multi transaction -one.")



        for i in range(4):
            urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
            time.sleep(15)

        time.sleep(30)


        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())

        self.assertEqual(balance_wallet_1,24000.0,"A problem in same network one and multi transaction -multi.")



    def test_4_same_network_long_term_multi_transacton(self):
        """
        Send coin to 2.wallet from 1.wallet
        """

        Decentra_Network_Docker()
        wallet_2_json = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/create/123").read().decode())
        wallet_2_address = wallet_2_json[0].replace("0) ", "").replace(" - CURRENTLY USED\n", "")



        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
        time.sleep(15)
        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())
        self.assertEqual(balance_wallet_1,4000.0,"A problem in same network one transaction -1.")

        time.sleep(30)

        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
        time.sleep(15)
        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())
        self.assertEqual(balance_wallet_1,9000.0,"A problem in same network one transaction -2.")


        time.sleep(60)

        urllib.request.urlopen(f"http://localhost:8000/send/coin/{wallet_2_address}/5000/123")
        time.sleep(15)
        balance_wallet_1 = json.loads(urllib.request.urlopen("http://localhost:8010/wallet/balance").read().decode())
        self.assertEqual(balance_wallet_1,14000.0,"A problem in same network one transaction -3.")

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..",".."))
import urllib.request, json
import time
from functional_test.docker.docker import Decentra_Network_Docker
unittest.main(exit=False)
