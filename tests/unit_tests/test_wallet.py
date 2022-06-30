#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..","..","src"))
import unittest

from lib.encryption import decrypt
from lib.settings_system import change_wallet
from lib.settings_system import save_settings
from lib.settings_system import the_settings
from wallet.delete_current_wallet import delete_current_wallet
from wallet.ellipticcurve.privateKey import PrivateKey
from wallet.ellipticcurve.publicKey import PublicKey
from wallet.get_saved_wallet import get_saved_wallet
from wallet.print_wallets import print_wallets
from wallet.save_wallet_list import save_wallet_list
from wallet.wallet_create import wallet_create
from wallet.wallet_delete import wallet_delete
from wallet.wallet_import import wallet_import
from wallet.wallet_selector import wallet_selector


class Test_Wallet(unittest.TestCase):

    def test_1_wallet_by_creating_saving_importing_and_deleting_a_wallet(self):

        password = "123"

        temp_private_key = wallet_create(password)

        saved_wallets = get_saved_wallet()

        result = False
        for each_wallet in saved_wallets:
            if temp_private_key == (saved_wallets[each_wallet]["privatekey"]):
                if temp_private_key == (wallet_import(each_wallet, 1,
                                                      password)):

                    wallet_delete(each_wallet)
                    result = True if each_wallet not in get_saved_wallet(
                    ) else False
                    break
                elif decrypt(temp_private_key, password) == (wallet_import(
                        each_wallet, 1, password)):
                    wallet_delete(each_wallet)
                    result = True if each_wallet not in get_saved_wallet(
                    ) else False
                    break

        self.assertEqual(result, True,
                         "A problem on the saving and importing the wallet.")

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

    def test_4_wallet_selector_empty(self):

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        results = wallet_selector(0)
        save_wallet_list(original_saved_wallets)
        self.assertEqual(results, None)

    def test_5_wallet_selector(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)

        saved_wallets = get_saved_wallet()
        results = wallet_selector(0) + 1

        save_wallet_list(original_saved_wallets)
        self.assertEqual(results, True)

    def test_6_wallet_selector_false_wallet_number(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)

        saved_wallets = get_saved_wallet()
        results = wallet_selector(len(saved_wallets))
        save_wallet_list(original_saved_wallets)
        self.assertEqual(results, None)

    def test_7_wallet_selector_non_number(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)

        saved_wallets = get_saved_wallet()
        results = wallet_selector("Decentra Network") + 1

        save_wallet_list(original_saved_wallets)
        self.assertEqual(results, True)

    def test_8_delete_current_wallet_first_wallet(self):
        backup_settings = the_settings()

        temp_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        delete_current_wallet()

        saved_wallets = get_saved_wallet()

        save_wallet_list(original_saved_wallets)
        save_settings(backup_settings)
        self.assertEqual(len(saved_wallets), 1)

    def test_9_delete_current_wallet(self):
        backup_settings = the_settings()

        temp_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        temp_private_key_2 = wallet_create(password)

        change_wallet(1)
        delete_current_wallet()

        saved_wallets = get_saved_wallet()

        save_wallet_list(original_saved_wallets)
        save_settings(backup_settings)
        self.assertEqual(len(saved_wallets), 1)

    def test_10_print_wallets_one_wallet(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)

        result = print_wallets()
        true_version = [f"0) {wallet_import(-1,3)} - CURRENTLY USED\n"]

        save_wallet_list(original_saved_wallets)

        self.assertEqual(result, true_version)

    def test_11_print_wallets_multiple_wallet(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        temp_private_key_2 = wallet_create(password)

        result = print_wallets()
        print(result)
        true_version = [
            f"0) {wallet_import(-1,3)} - CURRENTLY USED\n",
            f"1) {wallet_import(1,3)}\n",
        ]

        save_wallet_list(original_saved_wallets)

        self.assertEqual(result, true_version)

    def test_12_print_wallets_multiple_wallet_different_current_wallet(self):
        original_saved_wallets = get_saved_wallet()
        backup_settings = the_settings()

        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        temp_private_key_2 = wallet_create(password)

        change_wallet(1)

        result = print_wallets()
        true_version = [
            f"0) {wallet_import(0,3)}\n",
            f"1) {wallet_import(-1,3)} - CURRENTLY USED\n",
        ]

        save_wallet_list(original_saved_wallets)
        save_settings(backup_settings)

        self.assertEqual(result, true_version)


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
unittest.main(exit=False)
