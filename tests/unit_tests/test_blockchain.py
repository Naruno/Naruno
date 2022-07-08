#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
import time
import unittest

from accounts.account import Account
from accounts.get_accounts import GetAccounts
from blockchain.block.blocks_hash import GetBlockshash
from blockchain.block.block_main import Block
from blockchain.block.get_block import GetBlock
from blockchain.block.save_block import SaveBlock
from blockchain.block.hash.accounts_hash import AccountsHash
from blockchain.block.hash.blocks_hash import BlocksHash
from blockchain.block.hash.calculate_hash import CalculateHash
from blockchain.block.hash.tx_hash import TransactionsHash
from node.node_connection import Node_Connection
from node.unl import Unl
from transactions.transaction import Transaction



class Test_Blockchain(unittest.TestCase):

    def test_block_reset_start_time(self):
        block = Block("onur")
        first_time = block.start_time
        time.sleep(2)
        current_blockshash_list = []
        block.reset_the_block(current_blockshash_list)
        second_time = block.start_time
        self.assertNotEqual(first_time, second_time)

    def test_block_reset_raund_1(self):
        block = Block("onur")
        current_blockshash_list = []
        block.reset_the_block(current_blockshash_list)
        self.assertEqual(block.raund_1_starting_time, None)
        self.assertEqual(block.raund_1, False)

    def test_block_reset_raund_2(self):
        block = Block("onur")
        current_blockshash_list = []
        block.reset_the_block(current_blockshash_list)
        self.assertEqual(block.raund_2_starting_time, None)
        self.assertEqual(block.raund_2, False)

    def test_block_reset_validated(self):
        block = Block("onur")
        current_blockshash_list = []
        block.reset_the_block(current_blockshash_list)
        self.assertEqual(block.validated_time, None)
        self.assertEqual(block.validated, False)

    def test_block_reset_nodes(self):
        block = Block("onur")
        node_1 = Node_Connection("main_node", "sock", "id", "host", "port")
        node_1.candidate_block = True
        node_1.candidate_block_hash = True
        nodes_2 = [node_1]
        current_blockshash_list = []
        block.reset_the_block(current_blockshash_list, custom_nodes=nodes_2)
        for node in nodes_2:
            self.assertEqual(node.candidate_block, None)
            self.assertEqual(node.candidate_block_hash, None)

    def test_block_not_reset_enough_transaction(self):
        block = Block("onur")
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        self.assertEqual(result, False)

    def test_block_reset_enough_transaction_result(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        self.assertNotEqual(result, False)

    def test_block_reset_enough_transaction_hash_configuration(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        self.assertEqual(result[0].hash, result[1].previous_hash)

    def test_block_reset_enough_transaction_blockshash_list(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        self.assertEqual(current_blockshash_list, [result[1].previous_hash])

    def test_block_reset_enough_transaction_sequance_number(self):
        block = Block("onur")
        block.sequance_number = 0
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        true_sequence = result[0].sequance_number + 1
        self.assertEqual(result[1].sequance_number, true_sequence)

    def test_block_reset_enough_transaction_validating_list(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
        self.assertEqual(result[1].validating_list, [])

    def test_block_reset_enough_transaction_hash(self):
        block = Block("onur")
        block.hash = "onur"
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1, 2]
        current_blockshash_list = []
        result = block.reset_the_block(current_blockshash_list,
                                       custom_nodes=nodes_2)
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
        block = Block("onur")

        block.part_amount = 3

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(part_of_blocks_hash, ["onur"])
        self.assertEqual(the_blocks_hash, ["atakan", "ulusoy", "sivas"])
        self.assertEqual(
            result,
            "f99f80322fa66623d9b332fb91eee976333b024f19905c490c20acdfecaa7a86")

    def test_block_BlocksHash_enough_for_parting(self):
        block = Block("onur")

        block.part_amount = 2

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]

        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(
            part_of_blocks_hash,
            [
                "onur",
                "1d6f7d1be1273cab52939c01e6de8d9f725c1689f45b4ae0af64337599a10d6b",
            ],
        )
        self.assertEqual(the_blocks_hash, [])
        self.assertEqual(
            result,
            "97fce529fae4a3fea934aca54ed8b3be5d8be9dd09b5761d353ae5d440edbdf9")

    def test_block_AccountsHash(self):
        block = Block("onur")

        block.part_amount = 3

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        self.assertEqual(
            result,
            "4cbc6f4516470078ef91f1eb33a0f7e99cc5f95808a3343a3e256cfee657d6f8")

    def test_block_AccountsHash_enough_for_parting(self):
        block = Block("onur")

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        self.assertEqual(
            result,
            "4cbc6f4516470078ef91f1eb33a0f7e99cc5f95808a3343a3e256cfee657d6f8")

    def test_block_CalculateHash(self):
        block = Block("onur")

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = CalculateHash(block, part_of_blocks_hash, the_blocks_hash,
                               the_accounts)
        self.assertEqual(
            part_of_blocks_hash,
            [
                "onur",
                "1d6f7d1be1273cab52939c01e6de8d9f725c1689f45b4ae0af64337599a10d6b",
            ],
        )
        self.assertEqual(the_blocks_hash, [])
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        true_hash = "873a38de099d3d779b66c45537bc1d1865a506a59573a669d2fdbfca67d3634b"
        self.assertEqual(block.hash, true_hash)
        self.assertEqual(result, true_hash)

    def test_SaveBlock_GetBlock_first_time(self):
        block = Block("onur")

        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCK_PATH"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_first_time_TEMP_ACCOUNTS_PATH"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_SaveBlock_GetBlock_first_time_TEMP_BLOCKSHASH_PATH"
        SaveBlock(block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )

        block_2 = GetBlock(
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH          
        )

        the_accounts = GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH)
        the_blocks_hash = GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)


        self.assertEqual(len(the_accounts), 1)
        self.assertEqual(the_accounts[0].Address, "onur")
        self.assertEqual(the_accounts[0].balance, block.coin_amount)
        self.assertEqual(the_accounts[0].sequance_number, 0)

        self.assertEqual(len(the_blocks_hash), 1)
        self.assertEqual(the_blocks_hash[0], block.previous_hash)

        self.assertEqual(block.first_time, False)



    def test_SaveBlock_GetBlock(self):
        block = Block("onur")

        custom_TEMP_BLOCK_PATH = "db/test_SaveBlock_GetBlock_TEMP_BLOCK_PATH"
        custom_TEMP_ACCOUNTS_PATH = "db/test_SaveBlock_GetBlock_TEMP_ACCOUNTS_PATH"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_SaveBlock_GetBlock_TEMP_BLOCKSHASH_PATH"
        SaveBlock(block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )

        block_2 = GetBlock(
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH          
        )


        self.assertEqual(block.__dict__, block_2.__dict__)


unittest.main(exit=False)
