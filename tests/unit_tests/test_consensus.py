#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import time
import unittest

from decentra_network.blockchain.block.block_main import Block
from decentra_network.consensus.time.true_time.true_time_main import true_time
from decentra_network.lib.clean_up import CleanUp_tests


class Test_Consensus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    @classmethod
    def tearDownClass(cls):
        CleanUp_tests()

    def test_true_time_false(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 100
        self.assertFalse(true_time(block=block))

    def test_true_time(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        time.sleep(1)
        self.assertTrue(true_time(block=block))


unittest.main(exit=False)
