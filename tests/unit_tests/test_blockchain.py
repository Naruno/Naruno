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
import time
import unittest

from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import (GetBlockshash,
                                                           GetBlockshash_part,
                                                           SaveBlockshash,
                                                           SaveBlockshash_part)
from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from decentra_network.blockchain.block.hash.accounts_hash import AccountsHash
from decentra_network.blockchain.block.hash.blocks_hash import BlocksHash
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.blockchain.block.hash.tx_hash import TransactionsHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.block.save_block_to_blockchain_db import \
    SaveBlockstoBlockchainDB
from decentra_network.blockchain.block.shares import shares
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.node.client.client import client
from decentra_network.node.unl import Unl
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


class Test_Blockchain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    def test_block_reset_start_time(self):
        block = Block("onur")
        block.block_time = 1
        first_time = block.start_time
        time.sleep(2)
        block.reset_the_block()
        second_time = block.start_time
        self.assertNotEqual(first_time, second_time)

    def test_block_reset_start_time_none(self):
        block = Block("onur")
        block.block_time = 3
        first_time = block.start_time
        time.sleep(2)
        block.reset_the_block()
        second_time = block.start_time
        self.assertEqual(first_time, second_time)

    def test_block_reset_round_1(self):
        block = Block("onur")
        block.reset_the_block()
        self.assertEqual(block.round_1, False)

    def test_block_reset_round_2(self):
        block = Block("onur")
        block.reset_the_block()
        self.assertEqual(block.round_2_starting_time, None)
        self.assertEqual(block.round_2, False)

    def test_block_reset_validated(self):
        block = Block("onur")
        block.reset_the_block()
        self.assertEqual(block.validated_time, None)
        self.assertEqual(block.validated, False)

    def test_block_not_reset_enough_transaction(self):
        block = Block("onur")
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertEqual(result, False)

    def test_block_reset_enough_transaction_result(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertNotEqual(result, False)

    def test_block_reset_enough_transaction_hash_configuration(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertEqual(result[0].hash, result[1].previous_hash)

    def test_block_reset_enough_transaction_sequance_number(self):
        block = Block("onur")
        block.sequance_number = 0
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        result = block.reset_the_block(custom_nodes=nodes_2)
        true_sequence = result[0].sequance_number + 1
        self.assertEqual(result[1].sequance_number, true_sequence)

    def test_block_reset_enough_transaction_validating_list(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertEqual(result[1].validating_list, [])

    def test_block_reset_enough_transaction_hash(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertEqual(result[1].hash, None)

    def test_block_TXHash_none(self):
        block = Block("onur")

        block.validating_list = []

        result = TransactionsHash(block)
        self.assertEqual(result, "0")

    def test_block_TransactionsHash(self):
        block = Block("onur")

        the_transaction = Transaction(1, 1, 1, 1, 1, 1, 1, 1)

        block.validating_list = [the_transaction, the_transaction]

        result = TransactionsHash(block)
        self.assertEqual(
            result,
            "4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8")

    def test_block_BlocksHash(self):
        block = Block("onur", previous_hash="ulusoy")

        block.part_amount = 3

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(part_of_blocks_hash, ["onur"])
        self.assertEqual(the_blocks_hash, ["atakan", "ulusoy", "sivas"])
        self.assertEqual(
            result,
            "15476a4f0d177ff1a01f24746507ada567583ac037dfabf6f1be1e174d069ced")

    def test_block_BlocksHash_enough_for_parting(self):
        block = Block("onur", previous_hash="ulusoy")

        block.part_amount = 2

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]

        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(
            part_of_blocks_hash,
            [
                "onur",
            ],
        )
        self.assertEqual(the_blocks_hash, ["atakan", "ulusoy", "sivas"])
        self.assertEqual(
            result,
            "15476a4f0d177ff1a01f24746507ada567583ac037dfabf6f1be1e174d069ced")

    def test_block_AccountsHash(self):
        block = Block("onur")

        block.part_amount = 3

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(
            result,
            "fc70a682d1518ec2174127912b63edc59dd0353e5932e1008eefe3b85ffb4a96")

    def test_block_AccountsHash_enough_for_parting(self):
        block = Block("onur")

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(
            result,
            "fc70a682d1518ec2174127912b63edc59dd0353e5932e1008eefe3b85ffb4a96")

    def test_block_CalculateHash(self):
        block = Block("onur", previous_hash="ulusoy")

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = CalculateHash(block, part_of_blocks_hash, the_blocks_hash,
                               the_accounts)
        block.hash = result
        self.assertEqual(
            part_of_blocks_hash,
            [
                "onur",
            ],
        )
        self.assertEqual(the_blocks_hash, ["atakan", "ulusoy", "sivas"])
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        true_hash = "d901915ac088767c2695ae3be647ce6ab3f60acef26e1f705163b25f7d40f0d4"
        self.assertEqual(block.hash, true_hash)
        self.assertEqual(result, true_hash)

    def test_SaveBlock_GetBlock_first_time(self):
        block = Block("onur")

        custom_TEMP_BLOCK_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCK_PATH.json")
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_ACCOUNTS_PATH.json")
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        the_accounts_c = GetAccounts(
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH)
        the_accounts_c.execute("SELECT * FROM account_list")
        the_accounts = the_accounts_c.fetchall()
        the_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)

        self.assertEqual(len(the_accounts), 1)
        self.assertEqual(the_accounts[0][0], "onur")
        self.assertEqual(the_accounts[0][2], block.coin_amount)
        self.assertEqual(the_accounts[0][1], 0)

        self.assertEqual(len(the_blocks_hash), 1)
        self.assertEqual(the_blocks_hash[0], block.previous_hash)

        self.assertEqual(block.first_time, False)

    def test_SaveBlock_GetBlock(self):
        block = Block("onur")

        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        block_2 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(block.__dict__, block_2.__dict__)


    def test_SaveBlock_GetBlock_olds_specific_situation_1(self):
        self.maxDiff = None
        block = Block("onur")
        block.round_1 = True
        block_2 = Block("onur")
        block_2.round_1 = True
        block_2.validating_list = [Transaction(1, 1, 1, 1, 1, 1, 1, 1)]


        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_1_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_1_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_1_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        block_3 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(block_2.dump_json(), block_3.dump_json())

    def test_SaveBlock_GetBlock_olds_specific_situation_2(self):
        self.maxDiff = None
        block = Block("onur")
        block.round_1 = False
        block_2 = Block("onur")
        block_2.round_1 = False
        block_2.validating_list = [Transaction(1, 1, 1, 1, 1, 1, 1, 1)]


        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_2_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_2_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_2_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_2_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        block_3 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(block_2.dump_json(), block_3.dump_json())


    def test_SaveBlock_GetBlock_olds_specific_situation_3(self):
        self.maxDiff = None
        block = Block("onur")
        block.round_1 = False
        block.round_2 = False
        block_2 = Block("onur")
        block_2.round_1 = False
        block_2.round_2 = False
        block_2.validating_list = [Transaction(1, 1, 1, 1, 1, 1, 1, 1)]


        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_3_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_3_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_3_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_3_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        block_3 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(block_2.dump_json(), block_3.dump_json())

    def test_SaveBlock_GetBlock_olds_specific_situation_4(self):
        self.maxDiff = None
        block = Block("onur")
        block.round_1 = True
        block.round_2 = True
        block_2 = Block("onur")
        block_2.round_1 = False
        block_2.round_2 = False
        block_2.validating_list = [Transaction(1, 1, 1, 1, 1, 1, 1, 1)]


        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_4_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_specific_situation_4_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_4_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_specific_situation_4_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        block_3 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(block.dump_json(), block_3.dump_json())


    def test_SaveBlock_GetBlock_olds_secondly(self):
        self.maxDiff = None
        block = Block("onur")
        block.round_1 = False
        block.round_2 = False
        block_2 = Block("onur")
        block_2.round_1 = True
        block_3 = Block("onur")
        block_3.round_1 = True
        block_3.round_2 = True

        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_secondly_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_secondly_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_olds_secondly_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_secondly_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )




        block_result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)


        self.assertFalse(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(0)))
        self.assertTrue(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(1)))
        self.assertEqual(block_2.__dict__, block_result.__dict__)


        self.assertFalse(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(0)))
        self.assertTrue(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(1)))
        block_result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        self.assertEqual(block_2.__dict__, block_result.__dict__)


        SaveBlock(
            block_3,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertFalse(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(0)))
        self.assertFalse(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(1)))        
        self.assertTrue(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|" + str(2)))  
        block_result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        self.assertEqual(block_3.__dict__, block_result.__dict__)

        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        block_result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        self.assertEqual(block_3.__dict__, block_result.__dict__)


        SaveBlock(
            block_3,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        block_result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        self.assertEqual(block_3.__dict__, block_result.__dict__)

    def test_SaveBlock_GetBlock_olds(self):
        block = Block("onur")
        block.sequance_number = 0
        block.validating_list = []
        block_2 = Block("onur")
        block_2.sequance_number = 1
        block_2.validating_list = [Transaction(1, 1, 1, 1, 1, 1, 1, 1)]

        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_olds_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_olds_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_SaveBlock_GetBlock_oldsk_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_olds_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        SaveBlock(
            block_2,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )        
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        self.assertEqual(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|0"), True)
    
        self.assertEqual(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block_2.sequance_number) + "|" + str(len(block_2.validating_list)) + "|0"), True)
        print("started block_3 saving")
        block_3 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        print(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|0")
        self.assertEqual(os.path.exists(custom_TEMP_BLOCK_PATH + "|" + str(block.sequance_number) + "|" + str(len(block.validating_list)) + "|0"), False)

        self.maxDiff = None

        self.assertEqual(block_2.dump_json(), block_3.dump_json())

    def test_SaveBlockshash(self):

        custom_TEMP_BLOCKSHASH_PATH = "db/test_SaveBlockshash_TEMP_BLOCKSHASH_PATH.json"
        the_list = "onur"
        SaveBlockshash(the_list,
                       custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_list_2 = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        self.assertEqual([the_list], the_list_2)

    def test_SaveBlockshash_part(self):

        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlockshash_part_TEMP_BLOCKSHASH_PART_PATH.json")
        the_list = ["onur"]
        SaveBlockshash_part(
            the_list,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        the_list_2 = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        self.assertEqual(the_list, the_list_2)

    def test_GetBlockshash_non(self):
        custom_TEMP_BLOCKSHASH_PATH = (
            f"db/test_GetBlockshash_non_TEMP_BLOCKSHASH_PATH.json")
        the_list = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        self.assertEqual(the_list, [])

    def test_GetBlockshash_part_non(self):
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            f"db/test_GetBlockshash_part_non_TEMP_BLOCKSHASH_PART_PATH.json")
        the_list = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        self.assertEqual(the_list, [])

    def test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_not_our_transaction(
            self):
        block = Block("onur")
        custom_BLOCKS_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_not_our_transaction/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_BLOCKSHASH_PART_PATH.json"
        SaveBlockstoBlockchainDB(
            block,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        result = GetBlockstoBlockchainDB(
            block.sequance_number,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        self.assertEqual(result, False)

    def test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_fromUser(self):
        block = Block("onur")
        block.first_time = False

        the_json = {
            "sequance_number": 1,
            "signature": "",
            "fromUser": wallet_import(-1, 0),
            "toUser": "",
            "data": "",
            "amount": 1,
            "transaction_fee": 1,
            "transaction_time": 1,
        }

        loaded_transaction = Transaction.load_json(the_json)

        block.validating_list.append(loaded_transaction)

        custom_BLOCKS_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_ACCOUNTS_PATH.db"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB_TEMP_BLOCKSHASH_PART_PATH.json"
        the_account = Account("dbd811a12104827240153c8fd2f25a294a851ec8", 10,
                              1)
        SaveAccounts(the_account, custom_TEMP_ACCOUNTS_PATH)
        SaveBlockshash(block.previous_hash, custom_TEMP_BLOCKSHASH_PATH)
        SaveBlockshash_part(block.previous_hash,
                            custom_TEMP_BLOCKSHASH_PART_PATH)
        SaveBlockstoBlockchainDB(
            block,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        result = GetBlockstoBlockchainDB(
            block.sequance_number,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        block_2 = copy.copy(result[0])
        block_2_normal = copy.copy(block)

        block_2.validating_list = []
        block_2_normal.validating_list = []

        self.assertEqual(len(result), 4)
        self.assertEqual(block_2.__dict__, block_2_normal.__dict__)
        self.assertEqual(result[0].validating_list[0].__dict__,
                         block.validating_list[0].__dict__)
        result[1].execute("SELECT * FROM account_list")
        the_account_list = result[1].fetchall()
        self.assertEqual(the_account_list[0][0], the_account.Address)
        self.assertEqual(the_account_list[0][2], the_account.balance)
        self.assertEqual(the_account_list[0][1], the_account.sequance_number)
        self.assertEqual(result[2], [block.previous_hash])
        self.assertEqual(result[3], [block.previous_hash])

    def test_CreateBlock_from_zero(self):
        custom_TEMP_BLOCK_PATH = "db/test_CreateBlock_from_zero_TEMP_BLOCK_PATH.json"
        custom_TEMP_BLOCK_PATH_2 = (
            "db/test_2_CreateBlock_from_zero_TEMP_BLOCK_PATH.json")
        custom_TEMP_BLOCK_PATH_3 = (
            "db/test_3_CreateBlock_from_zero_TEMP_BLOCK_PATH.json")
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_CreateBlock_from_zero_TEMP_ACCOUNTS_PATH.json")
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_CreateBlock_from_zero_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        block = CreateBlock(custom_TEMP_BLOCK_PATH)
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_2,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_2)
        self.assertEqual(result.__dict__, block.__dict__)

        block.hash = "onur"
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_3,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

    def test_CreateBlock_migration(self):
        custom_TEMP_BLOCK_PATH_3 = (
            "db/test_3_CreateBlock_from_zero_TEMP_BLOCK_PATH.json")
        block = CreateBlock(custom_TEMP_BLOCK_PATH_3)
        result = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_3)
        self.assertEqual(block.previous_hash, result.hash)

    def test_CreateBlock_migratation_from_uncomplated_block(self):
        custom_TEMP_BLOCK_PATH = "db/test_CreateBlock_migratation_from_uncomplated_block_TEMP_BLOCK_PATH.json"
        custom_TEMP_BLOCK_PATH_2 = "db/test_CreateBlock_migratation_from_uncomplated_block_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_CreateBlock_migratation_from_uncomplated_block_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_CreateBlock_migratation_from_uncomplated_block_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        block = CreateBlock(custom_TEMP_BLOCK_PATH)
        block.hash = None
        block.previous_hash = "Onuratakan"
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_2,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )

        result = CreateBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH_2)
        self.assertEqual(result.previous_hash, block.previous_hash)

    def test_dump_json_load_json_Block(self):
        block = Block("onur")

        the_transaction = Transaction(1, "", "", "", 1, 1, 1, 1)

        block.validating_list.append(the_transaction)

        result = Block.load_json(block.dump_json())

        self.assertEqual(block.dump_json(), result.dump_json())

    def test_shares_start(self):
        block = Block("onur")

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 0)

    def test_shares_low(self):
        block = Block("onur")
        block.sequance_number = 5

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 0)

    def test_shares_big(self):
        block = Block("onur")
        block.sequance_number = 15

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 0)

    def test_shares_more_times_one(self):
        block = Block("onur")
        block.validating_list = [
            Transaction(1, "", "", "", 1, 1, 1000, 1),
            Transaction(1, "", "", "", 1, 1, 250, 1),
        ]
        block.sequance_number = 20

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 3)
        self.assertEqual(the_txs[0].toUser, "atakan")
        self.assertEqual(the_txs[0].amount, 10)
        self.assertEqual(the_txs[1].toUser, "ulusoy")
        self.assertEqual(the_txs[1].amount, 15)

        self.assertEqual(the_txs[2].toUser, "onuratakanulusoy")
        self.assertEqual(the_txs[2].amount, 1250)

    def test_shares_more_times_twice(self):
        block = Block("onur")
        block.validating_list = [Transaction(1, "", "", "", 1, 1, 1000, 1)]
        block.sequance_number = 30

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 3)
        self.assertEqual(the_txs[0].toUser, "atakan")
        self.assertEqual(the_txs[0].amount, 10)
        self.assertEqual(the_txs[1].toUser, "ulusoy")
        self.assertEqual(the_txs[1].amount, 15)

        self.assertEqual(the_txs[2].toUser, "onuratakanulusoy")
        self.assertEqual(the_txs[2].amount, 1000)

    def test_shares_more_times_last(self):
        block = Block("onur")
        block.validating_list = [Transaction(1, "", "", "", 1, 1, 1000, 1)]
        block.sequance_number = 40

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 3)
        self.assertEqual(the_txs[0].toUser, "atakan")
        self.assertEqual(the_txs[0].amount, 10)
        self.assertEqual(the_txs[1].toUser, "ulusoy")
        self.assertEqual(the_txs[1].amount, 15)

        self.assertEqual(the_txs[2].toUser, "onuratakanulusoy")
        self.assertEqual(the_txs[2].amount, 1000)

    def test_shares_more_times_more_last(self):
        block = Block("onur")
        block.validating_list = [Transaction(1, "", "", "", 1, 1, 1000, 1)]
        block.sequance_number = 50

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 1)
        self.assertEqual(the_txs[0].toUser, "onuratakanulusoy")
        self.assertEqual(the_txs[0].amount, 1000)

    def test_shares(self):
        block = Block("onur")
        block.validating_list = [Transaction(1, "", "", "", 1, 1, 1000, 1)]
        block.sequance_number = 10

        custom_shares = [["atakan", 10, 10, 40], ["ulusoy", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"
        the_txs = shares(block,
                         custom_shares=custom_shares,
                         custom_fee_address=custom_fee_address)

        self.assertEqual(len(the_txs), 3)
        self.assertEqual(the_txs[0].toUser, "atakan")
        self.assertEqual(the_txs[0].amount, 10)
        self.assertEqual(the_txs[1].toUser, "ulusoy")
        self.assertEqual(the_txs[1].amount, 15)

        self.assertEqual(the_txs[2].toUser, "onuratakanulusoy")
        self.assertEqual(the_txs[2].amount, 1000)


unittest.main(exit=False)
