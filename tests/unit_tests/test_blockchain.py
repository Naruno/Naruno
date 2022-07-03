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

from blockchain.block.block_main import Block
from blockchain.block.hash.tx_hash import TransactionsHash
from blockchain.block.hash.blocks_hash import BlocksHash
from blockchain.block.hash.accounts_hash import AccountsHash
from blockchain.block.hash.calculate_hash import CalculateHash
from transactions.transaction import Transaction
from accounts.account import Account
from node.node_connection import Node_Connection
from node.unl import Unl



class Test_Blockchain(unittest.TestCase):

    def test_block_reset_start_time(self):
        block = Block("onur", start_the_system=False)
        first_time = block.start_time
        time.sleep(2)
        block.reset_the_block()
        second_time = block.start_time
        self.assertNotEqual(first_time, second_time)

    def test_block_reset_raund_1(self):
        block = Block("onur", start_the_system=False)
        block.reset_the_block()
        self.assertEqual(block.raund_1_starting_time, None)
        self.assertEqual(block.raund_1, False)

    def test_block_reset_raund_2(self):
        block = Block("onur", start_the_system=False)
        block.reset_the_block()
        self.assertEqual(block.raund_2_starting_time, None)
        self.assertEqual(block.raund_2, False)

    def test_block_reset_validated(self):
        block = Block("onur", start_the_system=False)
        block.reset_the_block()
        self.assertEqual(block.validated_time, None)
        self.assertEqual(block.validated, False)

    def test_block_reset_nodes(self):
        block = Block("onur", start_the_system=False)
        node_1 = Node_Connection("main_node", "sock", "id", "host", "port")
        node_1.candidate_block = True
        node_1.candidate_block_hash = True
        nodes_2 = [node_1]
        block.reset_the_block(custom_nodes=nodes_2)
        for node in nodes_2:
            self.assertEqual(node.candidate_block, None)
            self.assertEqual(node.candidate_block_hash, None)

    def test_block_not_enough_transaction(self):
        block = Block("onur", start_the_system=False)
        nodes = Unl.get_as_node_type(Unl.get_unl_nodes())
        nodes_2 = nodes.copy()
        block.max_tx_number = 3
        block.validating_list = [1]
        result = block.reset_the_block(custom_nodes=nodes_2)
        self.assertEqual(result, False)


    def test_block_TXHash_none(self):
        block = Block("onur", start_the_system=False)

        block.validating_list = []

        result = TransactionsHash(block)
        self.assertEqual(result, "0")

    def test_block_TransactionsHash(self):
        block = Block("onur", start_the_system=False)

        the_transaction = Transaction(1,1,1,1,1,1,1,1)

        block.validating_list = [the_transaction, the_transaction]

        result = TransactionsHash(block)
        self.assertEqual(result, "4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8")


    def test_block_BlocksHash(self):
        block = Block("onur", start_the_system=False)

        block.part_amount = 3

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(part_of_blocks_hash, ['onur'])
        self.assertEqual(the_blocks_hash, ['atakan', 'ulusoy', 'sivas'])
        self.assertEqual(result, "f99f80322fa66623d9b332fb91eee976333b024f19905c490c20acdfecaa7a86")

    def test_block_BlocksHash_enough_for_parting(self):
        block = Block("onur", start_the_system=False)

        block.part_amount = 2

        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]

        result = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
        self.assertEqual(part_of_blocks_hash, ['onur', '1d6f7d1be1273cab52939c01e6de8d9f725c1689f45b4ae0af64337599a10d6b'])
        self.assertEqual(the_blocks_hash, [])
        self.assertEqual(result, "97fce529fae4a3fea934aca54ed8b3be5d8be9dd09b5761d353ae5d440edbdf9")

    def test_block_AccountsHash(self):
        block = Block("onur", start_the_system=False)

        block.part_amount = 3

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        self.assertEqual(result, "4cbc6f4516470078ef91f1eb33a0f7e99cc5f95808a3343a3e256cfee657d6f8")

    def test_block_AccountsHash_enough_for_parting(self):
        block = Block("onur", start_the_system=False)

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        result = AccountsHash(block, the_accounts)
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        self.assertEqual(result, "4cbc6f4516470078ef91f1eb33a0f7e99cc5f95808a3343a3e256cfee657d6f8")


    def test_block_CalculateHash(self):
        block = Block("onur", start_the_system=False)

        block.part_amount = 2

        the_account = Account("onur", "atakan", "ulusoy")
        the_accounts = [the_account, the_account, the_account]
        block.edited_accounts.append(the_account)
        part_of_blocks_hash = ["onur"]
        the_blocks_hash = ["atakan", "ulusoy", "sivas"]
        result = CalculateHash(block, part_of_blocks_hash, the_blocks_hash, the_accounts)
        self.assertEqual(part_of_blocks_hash, ['onur', '1d6f7d1be1273cab52939c01e6de8d9f725c1689f45b4ae0af64337599a10d6b'])
        self.assertEqual(the_blocks_hash, [])        
        self.assertEqual(the_accounts, [the_account, the_account, the_account])
        self.assertEqual(block.edited_accounts, [])
        true_hash = "873a38de099d3d779b66c45537bc1d1865a506a59573a669d2fdbfca67d3634b"
        self.assertEqual(block.hash, true_hash)
        self.assertEqual(result, true_hash)



unittest.main(exit=False)
