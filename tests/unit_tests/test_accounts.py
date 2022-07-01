#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from accounts.account import Account
import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class Test_Accounts(unittest.TestCase):
    def test_dumb_account(self):

        new_account = Account("test_account", 1, 1)

        dumped_account = new_account.dump_json()

        the_json = {
            "address": "test_account",
            "balance": 1,
            "sequence_number": 1,
        }

        self.assertEqual(dumped_account, the_json)

    def test_load_accounts(self):

        the_json = {
            "address": "test_account",
            "balance": 1,
            "sequence_number": 1,
        }

        loaded_account = Account.load_json(the_json)

        loaded_account_json = loaded_account.dump_json()

        self.assertEqual(loaded_account_json, the_json)

    def test_get_hash(self):

        the_account = Account("test_account", 1, 1)

        the_hash = "7fe8746bb0feae44e73aa4e6182e3ca577c4a5d5e219cd468adafd2ec4086550"

        the_account_hash = the_account.get_hash()

        self.assertEqual(the_hash, the_account_hash)

    def test_string_account(self):

        the_account = Account("test_account", 1, 1)

        account_string = "test_account"

        the_account_string = str(the_account)

        self.assertEqual(account_string, the_account_string)


unittest.main(exit=False)
