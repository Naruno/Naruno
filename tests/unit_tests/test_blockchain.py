#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from node.unl import Unl
from node.node_connection import Node_Connection
from blockchain.block.block_main import Block
import unittest
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


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


unittest.main(exit=False)
