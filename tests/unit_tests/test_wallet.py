#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
import unittest

from lib.encryption import decrypt
from wallet.ellipticcurve.privateKey import PrivateKey
from wallet.ellipticcurve.publicKey import PublicKey
from wallet.get_saved_wallet import get_saved_wallet
from wallet.wallet_create import wallet_create
from wallet.wallet_delete import wallet_delete
from wallet.wallet_import import wallet_import


class Test_Wallet(unittest.TestCase):
    def test_1_wallet_by_creating_saving_importing_and_deleting_a_wallet(self):

        password = "123"

        temp_private_key = wallet_create(password)

        saved_wallets = get_saved_wallet()

        result = False
        for each_wallet in saved_wallets:
            if temp_private_key == (saved_wallets[each_wallet]["privatekey"]):
                if temp_private_key == (wallet_import(each_wallet, 1, password)):

                    wallet_delete(each_wallet)
                    result = True if each_wallet not in get_saved_wallet() else False
                    break
                elif decrypt(temp_private_key, password) == (
                    wallet_import(each_wallet, 1, password)
                ):
                    wallet_delete(each_wallet)
                    result = True if each_wallet not in get_saved_wallet() else False
                    break

        self.assertEqual(
            result, True, "A problem on the saving and importing the wallet."
        )

    def test_2_wallet_by_private_pem_conversion(self):

        password = "123"

        temp_private_key_class = wallet_create(password, save=False)
        pem = temp_private_key_class.toPem()
        privateKey2 = PrivateKey.fromPem(pem)
        self.assertEqual(temp_private_key_class.secret, privateKey2.secret)
        self.assertEqual(temp_private_key_class.curve, privateKey2.curve)

    def test_3_wallet_by_public_conversion(self):

        password = "123"

        privateKey = wallet_create(password, save=False)
        publicKey1 = privateKey.publicKey()
        pem = publicKey1.toPem()
        publicKey2 = PublicKey.fromPem(pem)
        self.assertEqual(publicKey1.point.x, publicKey2.point.x)
        self.assertEqual(publicKey1.point.y, publicKey2.point.y)
        self.assertEqual(publicKey1.curve, publicKey2.curve)


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
unittest.main(exit=False)
