#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import copy
import time
import unittest

from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.finished.finished_main import finished_main
from decentra_network.consensus.finished.transactions.transactions_main import \
    transactions_main
from decentra_network.consensus.rounds.round_1.checks.candidate_blocks.candidate_blocks_main import \
    candidate_blocks_check
from decentra_network.consensus.rounds.round_1.checks.time.time_difference.time_difference_main import \
    time_difference_check
from decentra_network.consensus.rounds.round_2.checks.candidate_blocks_hashes.candidate_blocks_hashes_main import \
    candidate_blocks_hashes_check
from decentra_network.consensus.time.true_time.true_time_main import true_time
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


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

    def test_transactions_main(self):
        backup = GetMyTransaction()
        block = Block("Onur")
        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        block.validating_list.append(the_transaction)

        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "ulusoy"
        the_transaction_2.fromUser = "onuratakan"
        the_transaction_2.toUser = wallet_import(-1, 3)

        block.validating_list.append(the_transaction_2)

        SavetoMyTransaction(the_transaction)

        transactions_main(block=block)

        result = GetMyTransaction()

        for each_result in result:
            result[result.index(each_result)][0] = result[result.index(
                each_result)][0].dump_json()
        SaveMyTransaction(backup)
        self.assertEqual(
            result,
            [
                [the_transaction.dump_json(), True],
                [the_transaction_2.dump_json(), True],
            ],
        )

    def test_finished_main_false_time(self):
        custom_BLOCKS_PATH = "db/test_finished_main_false_time/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_false_time_TEMP_ACCOUNTS_PATH.json")
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_false_time_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_false_time_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 100

        result = finished_main(
            block=block,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertFalse(result)

    def test_finished_main_no_reset(self):
        custom_TEMP_BLOCK_PATH = "db/test_finished_main_no_reset_TEMP_BLOCK_PATH.json"
        custom_BLOCKS_PATH = "db/test_finished_main_no_reset/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_no_reset_TEMP_ACCOUNTS_PATH.json")
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_no_reset_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_no_reset_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequance_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertFalse(result_2)

    def test_finished_main(self):
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        block.validating_list = [the_transaction, the_transaction]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequance_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertIsNot(result_2, False)

    def test_candidate_blocks_check_false(self):

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block([data_block for i in range(7)],
                                         [data_block_hash for i in range(7)])
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_check(self):

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block([data_block for i in range(8)],
                                         [data_block_hash for i in range(7)])
        CandidateBlock.candidate_blocks = [data_block for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [
            data_block_hash for i in range(7)
        ]
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, False)

    def test_candidate_blocks_hashes_check_false(self):

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block([data_block for i in range(7)],
                                         [data_block_hash for i in range(7)])
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_hashes_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_hashes_check(self):

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block([data_block for i in range(7)],
                                         [data_block_hash for i in range(8)])
        CandidateBlock.candidate_block_hashes = [
            data_block_hash for i in range(8)
        ]
        CandidateBlock.candidate_blocks_hash = [
            data_block_hash for i in range(7)
        ]
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_hashes_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, False)

    def test_time_difference_check_round_1_false_time(self):
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2

        self.assertFalse(time_difference_check(block))

    def test_time_difference_check_round_1(self):
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(2.5)

        self.assertTrue(time_difference_check(block))


unittest.main(exit=False)
