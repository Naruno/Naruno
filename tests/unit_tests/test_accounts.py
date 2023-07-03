#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest

from naruno.accounts.account import Account
from naruno.accounts.commanders.delete_commander import DeleteCommander
from naruno.accounts.commanders.get_comnder import GetCommander
from naruno.accounts.commanders.save_commander import SaveCommander
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.get_balance import GetBalance
from naruno.accounts.get_sequence_number import GetSequanceNumber
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.save_block import SaveBlock
from naruno.lib.clean_up import CleanUp_tests


class Test_Accounts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

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

    def test_GetBalance_not_list_account(self):
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15,
                                1)
        the_account_3 = Account("7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1", 20,
                                1)

        temp_path = "db/test_GetBalance_not_list_account.db"

        SaveAccounts(the_account, temp_path)
        SaveAccounts(the_account_2, temp_path)
        SaveAccounts(the_account_3, temp_path)

        account_list = GetAccounts(temp_path)

        block = Block("alieren")
        block.minumum_transfer_amount = 5

        result = GetBalance("the_account_4",
                            account_list=account_list,
                            block=block)

        self.assertEqual(result, -5)

    def test_GetBalance(self):
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15,
                                1)
        the_account_3 = Account("7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1", 20,
                                1)

        temp_path = "db/test_GetBalance_not_list_account.db"

        SaveAccounts(the_account, temp_path)
        SaveAccounts(the_account_2, temp_path)
        SaveAccounts(the_account_3, temp_path)

        account_list = GetAccounts(temp_path)

        block = Block("alieren")
        block.minumum_transfer_amount = 5

        result = GetBalance("test_account",
                            account_list=account_list,
                            block=block)
        self.assertEqual(result, 5)
        result_2 = GetBalance("test_account_2",
                              account_list=account_list,
                              block=block)
        self.assertEqual(result_2, 10)
        result_3 = GetBalance("test_account_3",
                              account_list=account_list,
                              block=block)
        self.assertEqual(result_3, 15)

    def test_GetBalance_non_block(self):
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15,
                                1)
        the_account_3 = Account("7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1", 20,
                                1)

        temp_path = "db/test_GetBalance_non_block_account.db"

        SaveAccounts(the_account, temp_path)
        SaveAccounts(the_account_2, temp_path)
        SaveAccounts(the_account_3, temp_path)

        account_list = GetAccounts(temp_path)
        print(account_list)

        block = Block("alieren")
        block.minumum_transfer_amount = 5
        custom_TEMP_BLOCK_PATH = "db/test_GetBalance_non_block.db"
        SaveBlock(block, custom_TEMP_BLOCK_PATH)

        result = GetBalance(
            "test_account",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result, 5)
        result_2 = GetBalance(
            "test_account_2",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result_2, 10)
        result_3 = GetBalance(
            "test_account_3",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result_3, 15)

    def test_GetBalance_non_block_non_record(self):
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15,
                                1)
        the_account_3 = Account("7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1", 20,
                                1)

        temp_path = "db/test_GetBalance_not_list_account.db"

        SaveAccounts(the_account, temp_path)
        SaveAccounts(the_account_2, temp_path)
        SaveAccounts(the_account_3, temp_path)

        account_list = GetAccounts(temp_path)

        block = Block("alieren")
        block.minumum_transfer_amount = 5
        custom_TEMP_BLOCK_PATH = "db/test_GetBalance_non_block_no_record.db"

        result = GetBalance(
            "test_account",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result, None)
        result_2 = GetBalance(
            "test_account_2",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result_2, None)
        result_3 = GetBalance(
            "test_account_3",
            account_list=account_list,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        )
        self.assertEqual(result_3, None)

    def test_SaveAccounts_GetAccounts(self):
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15,
                                2)
        the_account_3 = Account("7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1", 20,
                                3)

        temp_path = "db/test_SaveAccounts_GetAccounts.db"

        SaveAccounts(the_account, temp_path)
        SaveAccounts(the_account_2, temp_path)
        SaveAccounts(the_account_3, temp_path)

        result = GetAccounts(temp_path)
        result_list = result
        account_list = {
            "dbd811a12104827240153c8fd2f25a294a851ec8": [1, 10],
            "15562b06dc6b1acd6e8c86031e564e0c451c7a73": [2, 15],
            "7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1": [3, 20],
        }
        self.assertEqual(len(result_list), len(account_list))

        self.assertEqual(result_list["15562b06dc6b1acd6e8c86031e564e0c451c7a73"]
                         [0], account_list["15562b06dc6b1acd6e8c86031e564e0c451c7a73"][0])
        self.assertEqual(result_list["7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1"]
                         [1], account_list["7340ac0cdf3f7b59cba4ec6348ee8e41d0c24ef1"][1])

    def test_commanders(self):
        backup_commanders = copy.copy(GetCommander())

        SaveCommander("merhaba")

        self.assertEqual(GetCommander(), ["merhaba"])

        SaveCommander("merhabaa")

        self.assertEqual(GetCommander(), ["merhaba", "merhabaa"])

        # Find difference with backup and new commanders list
        new_commanders = GetCommander()
        difference = list(set(new_commanders) - set(backup_commanders))
        for commander in difference:
            DeleteCommander(commander)

        self.assertEqual(GetCommander(), backup_commanders)


backup = sys.argv
sys.argv = [sys.argv[0]]
unittest.main(exit=False)
sys.argv = backup
