#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

from naruno.consensus.sync.sync import sync

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import copy
import time
import unittest

from speed_calculator import calculate

from naruno.accounts.account import Account
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import GetBlockshash, GetBlockshash_part
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.get_block_from_blockchain_db import GetBlockstoBlockchainDB
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import candidate_block
from naruno.config import (
    CONNECTED_NODES_PATH,
    LOADING_ACCOUNTS_PATH,
    LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH,
    LOADING_BLOCKSHASH_PATH,
    PENDING_TRANSACTIONS_PATH,
    TEMP_ACCOUNTS_PATH,
    TEMP_BLOCK_PATH,
    TEMP_BLOCKSHASH_PART_PATH,
    TEMP_BLOCKSHASH_PATH,
    UNL_NODES_PATH,
)
from naruno.consensus.consensus_main import consensus_trigger
from naruno.consensus.finished.finished_main import finished_main
from naruno.consensus.finished.transactions.transactions_main import (
    transactions_main as transactions_main_finished,
)
from naruno.consensus.ongoing.ongoing_main import ongoing_main
from naruno.consensus.rounds.round_1.checks.candidate_blocks.candidate_blocks_main import (
    candidate_blocks_check,
)
from naruno.consensus.rounds.round_1.checks.checks_main import (
    round_check as round_check_round_1,
)
from naruno.consensus.rounds.round_1.checks.time.time_difference.time_difference_main import (
    time_difference_check as time_difference_check_round_1,
)
from naruno.consensus.rounds.round_1.process.process_main import (
    round_process as round_process_round_1,
)
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import (
    Remove_Duplicates,
)
from naruno.consensus.rounds.round_1.process.transactions.find_newly.find_newly_main import (
    find_newly,
)
from naruno.consensus.rounds.round_1.process.transactions.find_validated.find_validated_main import (
    find_validated,
)
from naruno.consensus.rounds.round_1.process.transactions.transactions_main import (
    transactions_main as transactions_main_round_1,
)
from naruno.consensus.rounds.round_1.round_1_main import consensus_round_1
from naruno.consensus.rounds.round_2.checks.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    candidate_blocks_hashes_check,
)
from naruno.consensus.rounds.round_2.checks.checks_main import (
    round_check as round_check_round_2,
)
from naruno.consensus.rounds.round_2.checks.time.time_difference.time_difference_main import (
    time_difference_check as time_difference_check_round_2,
)
from naruno.consensus.rounds.round_2.process.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    process_candidate_blocks_hashes,
)
from naruno.consensus.rounds.round_2.process.process_main import (
    round_process as round_process_round_2,
)
from naruno.consensus.rounds.round_2.process.rescue.rescue_main import rescue_main
from naruno.consensus.rounds.round_2.process.validate.validate_main import validate_main
from naruno.consensus.rounds.round_2.round_2_main import consensus_round_2
from naruno.consensus.finished.true_time.true_time_main import true_time
from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.mix.merkle_root import MerkleTree
from naruno.lib.settings_system import save_settings, the_settings
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.my_transactions.get_my_transaction import GetMyTransaction
from naruno.transactions.my_transactions.save_my_transaction import SaveMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import (
    SavetoMyTransaction,
)
from naruno.transactions.my_transactions.validate_transaction import ValidateTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.save_wallet_list import save_wallet_list
from naruno.wallet.wallet_create import wallet_create
from naruno.wallet.wallet_import import wallet_import


class Test_Consensus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CleanUp_tests()
        cls.custom_TEMP_BLOCK_PATH0 = TEMP_BLOCK_PATH.replace(
            ".json", "_0.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCK_PATH1 = TEMP_BLOCK_PATH.replace(
            ".json", "_1.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCK_PATH2 = TEMP_BLOCK_PATH.replace(
            ".json", "_2.json"
        ).replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCK_PATH0 = LOADING_BLOCK_PATH.replace(
            ".json", "_0.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCK_PATH1 = LOADING_BLOCK_PATH.replace(
            ".json", "_1.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCK_PATH2 = LOADING_BLOCK_PATH.replace(
            ".json", "_2.json"
        ).replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_ACCOUNTS_PATH0 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_0.db"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH1 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_1.db"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH2 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_2.db"
        ).replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH0 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_0.db"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH1 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_1.db"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH2 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_2.db"
        ).replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_BLOCKSHASH_PATH0 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_0.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH1 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_1.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH2 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_2.json"
        ).replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH0 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_0.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH1 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_1.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH2 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_2.json"
        ).replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_BLOCKSHASH_PART_PATH0 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_0.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PART_PATH1 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_1.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PART_PATH2 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_2.json"
        ).replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH0 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_0.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH1 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_1.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH2 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_2.json"
        ).replace("loading_", "test_loading_temp_")

        cls.custom_CONNECTED_NODES_PATH0 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_0"
        )
        cls.custom_CONNECTED_NODES_PATH1 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_1"
        )
        cls.custom_CONNECTED_NODES_PATH2 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_2"
        )

        cls.custom_PENDING_TRANSACTIONS_PATH0 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_0"
        )
        cls.custom_PENDING_TRANSACTIONS_PATH1 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_1"
        )
        cls.custom_PENDING_TRANSACTIONS_PATH2 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_2"
        )

        cls.node_0 = server(
            "127.0.0.1",
            10000,
            save_messages=True,
            custom_TEMP_BLOCK_PATH=cls.custom_TEMP_BLOCK_PATH0,
            custom_LOADING_BLOCK_PATH=cls.custom_LOADING_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=cls.custom_TEMP_ACCOUNTS_PATH0,
            custom_LOADING_ACCOUNTS_PATH=cls.custom_LOADING_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=cls.custom_TEMP_BLOCKSHASH_PATH0,
            custom_LOADING_BLOCKSHASH_PATH=cls.custom_LOADING_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.custom_TEMP_BLOCKSHASH_PART_PATH0,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.custom_LOADING_BLOCKSHASH_PART_PATH0,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH0,
            custom_PENDING_TRANSACTIONS_PATH=cls.custom_PENDING_TRANSACTIONS_PATH0,
            custom_variables=True,
        )

        cls.node_1 = server(
            "127.0.0.1",
            10001,
            save_messages=True,
            custom_TEMP_BLOCK_PATH=cls.custom_TEMP_BLOCK_PATH1,
            custom_LOADING_BLOCK_PATH=cls.custom_LOADING_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=cls.custom_TEMP_ACCOUNTS_PATH1,
            custom_LOADING_ACCOUNTS_PATH=cls.custom_LOADING_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=cls.custom_TEMP_BLOCKSHASH_PATH1,
            custom_LOADING_BLOCKSHASH_PATH=cls.custom_LOADING_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.custom_TEMP_BLOCKSHASH_PART_PATH1,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.custom_LOADING_BLOCKSHASH_PART_PATH1,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH1,
            custom_PENDING_TRANSACTIONS_PATH=cls.custom_PENDING_TRANSACTIONS_PATH1,
            custom_variables=True,
        )
        cls.node_2 = server(
            "127.0.0.1",
            10002,
            save_messages=True,
            custom_TEMP_BLOCK_PATH=cls.custom_TEMP_BLOCK_PATH2,
            custom_LOADING_BLOCK_PATH=cls.custom_LOADING_BLOCK_PATH2,
            custom_TEMP_ACCOUNTS_PATH=cls.custom_TEMP_ACCOUNTS_PATH2,
            custom_LOADING_ACCOUNTS_PATH=cls.custom_LOADING_ACCOUNTS_PATH2,
            custom_TEMP_BLOCKSHASH_PATH=cls.custom_TEMP_BLOCKSHASH_PATH2,
            custom_LOADING_BLOCKSHASH_PATH=cls.custom_LOADING_BLOCKSHASH_PATH2,
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.custom_TEMP_BLOCKSHASH_PART_PATH2,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.custom_LOADING_BLOCKSHASH_PART_PATH2,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH2,
            custom_PENDING_TRANSACTIONS_PATH=cls.custom_PENDING_TRANSACTIONS_PATH2,
            custom_variables=True,
        )
        Unl.save_new_unl_node(cls.node_0.id)
        Unl.save_new_unl_node(cls.node_1.id)
        Unl.save_new_unl_node(cls.node_2.id)
        time.sleep(2)
        cls.node_0.connect("127.0.0.1", 10001)
        cls.node_0.connect("127.0.0.1", 10002)
        time.sleep(2)
        cls.node_2.connect("127.0.0.1", 10001)

        print(cls.node_0.clients)
        print(cls.node_1.clients)
        print(cls.node_2.clients)
        print("started")

    @classmethod
    def tearDownClass(cls):
        cls.node_0.stop()
        cls.node_1.stop()
        cls.node_2.stop()

        time.sleep(2)

        cls.node_1.join()
        cls.node_2.join()
        cls.node_0.join()

        for a_client in cls.node_0.clients:
            the_dict = {}
            the_dict["id"] = a_client.id
            the_dict["host"] = a_client.host
            the_dict["port"] = a_client.port
            cls.node_0.connected_node_delete(the_dict)

        for a_client in cls.node_1.clients:
            the_dict = {}
            the_dict["id"] = a_client.id
            the_dict["host"] = a_client.host
            the_dict["port"] = a_client.port
            cls.node_1.connected_node_delete(the_dict)

        for a_client in cls.node_2.clients:
            the_dict = {}
            the_dict["id"] = a_client.id
            the_dict["host"] = a_client.host
            the_dict["port"] = a_client.port
            cls.node_2.connected_node_delete(the_dict)

    def test_true_time_false(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 100
        self.assertFalse(true_time(block=block))

    def test_true_time(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 2
        block.sequence_number = 1
        block.empty_block_number = 1
        time.sleep(7)
        self.assertTrue(true_time(block=block))

    def test_transactions_main_finished(self):
        self.maxDiff = None
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"
        wallet_create(password)
        wallet_create(password)

        backup = GetMyTransaction()
        block = Block("Onur")
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(0, 0)
        block.validating_list.append(the_transaction)

        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "ulusoy"
        the_transaction_2.fromUser = "onuratakan"
        the_transaction_2.toUser = wallet_import(1, 3)

        block.validating_list.append(the_transaction_2)

        the_transaction_3 = copy.copy(the_transaction)
        the_transaction_3.signature = "aaulusoy"
        the_transaction_3.fromUser = "onuratakan"
        the_transaction_3.toUser = wallet_import(0, 3)

        block.validating_list.append(the_transaction_3)

        SavetoMyTransaction(the_transaction)

        transactions_main_finished(block=block)

        result = GetMyTransaction()

        for each_result in result:
            result[result.index(each_result)][0] = result[result.index(each_result)][
                0
            ].dump_json()
        SaveMyTransaction(backup)
        save_wallet_list(original_saved_wallets)
        print("result ", result)
        self.assertEqual(
            result,
            [
                [the_transaction.dump_json(), True, True],
                [the_transaction_2.dump_json(), True, False],
                [the_transaction_3.dump_json(), True, False],
            ],
        )

    def test_finished_main_false_time(self):
        custom_BLOCKS_PATH = "db/test_finished_main_false_time/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_false_time_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_false_time_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_false_time_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 100

        result = finished_main(
            block=block,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertFalse(result)

    def test_finished_main_no_reset_other_0(self):
        custom_TEMP_BLOCK_PATH = "db/test_finished_main_no_reset_TEMP_BLOCK_PATH.json"
        custom_BLOCKS_PATH = "db/test_finished_main_no_reset/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_no_reset_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_no_reset_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_no_reset_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertFalse(result_2)

    def test_finished_main_no_save(self):
        backup = GetMyTransaction()

        custom_TEMP_BLOCK_PATH = "db/test_finished_main_no_save.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_no_save_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_no_save_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_no_save_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onursdadas")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 1
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        block.validating_list = [the_transaction, the_transaction]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(3)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=1,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertEqual(result_2, False)
        SaveMyTransaction(backup)

    def test_finished_main_no_save_0(self):
        backup = GetMyTransaction()

        custom_TEMP_BLOCK_PATH = "db/test_finished_main_no_save_0.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_finished_main_no_save_0_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_no_save_0_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_no_save_0_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onursdadas")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "a"
        block.validating_list = [the_transaction, the_transaction_2]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertNotEqual(result_2, False)
        SaveMyTransaction(backup)

    def test_finished_main_save_from(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = False
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onurdsadsaas")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            dont_clean=True,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

    def test_finished_main_save_to(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = False
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onursssdasda")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.toUser = wallet_import(-1, 3)
        block.validating_list = [the_transaction, the_transaction]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

    def test_finished_main_save_from_no_part(self):
        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_save_from_no_part_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_save_from_no_part_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 2
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            dont_clean=True,
        )
        time.sleep(3)
        gap_block = copy.copy(block.empty_block_number)
        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        new_gap_block = copy.copy(block.empty_block_number)
        # self.assertEqual(gap_block, new_gap_block)
        time.sleep(3)
        expected_new_time = true_time(block, return_result=True)
        self.assertEqual(expected_new_time, True)

        expected_round_1_true_time = time_difference_check_round_1(
            block, return_result=True
        )
        expected_true_time = (
            block.genesis_time
            + block.block_time
            + ((block.sequence_number + block.empty_block_number) * block.block_time)
        )
        self.assertEqual(
            expected_round_1_true_time, expected_true_time + block.round_2_time - 2
        )

        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        self.assertEqual(
            the_blockshash, [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        )
        self.assertEqual(
            the_blockshash_part, [Block("Onurdsadasdsaddsaas").previous_hash]
        )

    def test_finished_main_save_from_part_save_blockshash(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_save_from_part_save_blockshash_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_finished_main_save_from_part_save_blockshash_TEMP_BLOCKSHASH_PART_PATH.json"

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            dont_clean=True,
        )
        time.sleep(1)
        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        ).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(
                custom_BLOCKS_PATH
                + str(block.sequence_number)
                + ".blockshash_full.json"
            )
        )

        self.assertEqual(
            Saved_blocks_hash, [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        )

    def test_finished_main_save_from_part(self):
        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_finished_main_save_from_part_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_finished_main_save_from_part_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            dont_clean=True,
        )
        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        ).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

    def test_finished_main_save_from_part_save_blockshash_first_part(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = False
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_save_from_part_save_blockshash_first_parta_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_save_from_part_save_blockshash_first_parta_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_finished_main_save_from_part_save_blockshash_first_parta_TEMP_BLOCKSHASH_PART_PATH.json"

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 2
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        block.validating_list = [the_transaction, the_transaction]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(6)
        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=2,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        ).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(
                custom_BLOCKS_PATH
                + str(block.sequence_number)
                + ".blockshash_full.json"
            )
        )

        self.assertEqual(
            Saved_blocks_hash, [Block("Onurdsadasdsaddsaas").previous_hash, "new_hash"]
        )

    def test_finished_main_save_from_part_no_save_blockshash(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_TEMP_BLOCKSHASH_PART_PATH.json"

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 3
        block.round_1_time = 1
        block.round_2_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "a"
        block.validating_list = [the_transaction, the_transaction_2]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(
                custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
            ),
            GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(3)
        gap_block = copy.copy(block.empty_block_number)
        print("gap_block", gap_block)
        print(block.sequence_number)
        self.assertEqual(block.sync, False)
        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertEqual(block.sync, True)
        print(block.sequence_number)
        new_gap_block = copy.copy(block.empty_block_number)
        print("new_gap_block", new_gap_block)
        self.assertNotEqual(gap_block, new_gap_block)
        self.assertEqual((gap_block + block.gap_block_number), new_gap_block)
        expected_round_1_true_time = time_difference_check_round_1(
            block, return_result=True
        )
        expected_new_time = true_time(block, return_result=True)
        real_now_time = int(time.time())
        self.assertLessEqual(
            block.start_time - block.hard_block_number * block.block_time, real_now_time
        )
        print("time", int(time.time()))
        print("hard", block.hard_block_number)
        print("gap", block.gap_block_number)
        print("block_time", block.block_time)
        print("round_1_time", block.round_1_time)
        print("round_2_time", block.round_2_time)
        print("block_start_time", block.start_time)

        print("expected_round_1_true_time", expected_round_1_true_time)
        print("expected_new_time", expected_new_time)
        # self.assertEqual(
        #    expected_new_time,
        #    block.start_time +
        #    (block.block_time *
        #     (block.sequence_number + block.empty_block_number -
        #      block.hard_block_number)),
        # )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)
        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash, hash_1]
        ).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(
                custom_BLOCKS_PATH
                + str(block.sequence_number)
                + ".blockshash_full.json"
            )
        )

        self.assertEqual(
            Saved_blocks_hash, [Block("Onurdsadasdsaddsaas").previous_hash, hash_1]
        )

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0], hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

    def test_finished_main_save_from_part_no_save_blockshash_disable_saving(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_disable_saving.json"
        custom_BLOCKS_PATH = "db/test_finished_main_2/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_disable_saving_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_disable_saving_TEMP_BLOCKSHASH_PART_PATH.json"

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 1
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction_2 = Transaction.load_json(the_transaction_json)
        the_transaction_2.signature = "aa"
        block.validating_list = [the_transaction, the_transaction_2]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(
                custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
            ),
            GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(3)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=1,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertEqual(result_2, False)
        SaveMyTransaction(backup)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH
        )
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH
        )
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash, hash_1]
        ).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], False)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(
                custom_BLOCKS_PATH
                + str(block.sequence_number)
                + ".blockshash_full.json"
            )
        )

        self.assertEqual(
            Saved_blocks_hash, [Block("Onurdsadasdsaddsaas").previous_hash, hash_1]
        )

    def test_candidate_blocks_check_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_check(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "onur",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur",
            "sequence_number": 58,
            "signature": "onur",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, False)

    def test_candidate_blocks_hashes_check_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_hashes_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_hashes_check(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "onur",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur from tests",
            "sequence_number": 58,
            "signature": "onur",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_hashes_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, False)

    def test_time_difference_check_round_1_false_time(self):
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2

        self.assertFalse(time_difference_check_round_1(block))

    def test_time_difference_check_round_1(self):
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)

        self.assertTrue(time_difference_check_round_1(block))

    def test_round_check_round_1_false_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        self.assertFalse(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_round_check_round_1_true_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(7)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        self.assertFalse(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_round_check_round_1_false_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)
        self.assertFalse(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_round_check_round_1_true_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)
        self.assertTrue(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_find_newly(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "newMEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE="
        block = Block("Onur")
        block.validating_list = [the_transaction, the_transaction_2]
        temp_validating_list = [the_transaction]
        result = find_newly(block, temp_validating_list)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(block.validating_list), 0)
        self.assertEqual(result[0].dump_json(), the_transaction_2.dump_json())

    def test_find_validated_1_node(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(1)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(1):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(1)]
        block = Block("Onur")
        block.validating_list = [the_transaction]
        result = find_validated(block, CandidateBlock, unl_nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].dump_json(), the_transaction.dump_json())

    def test_find_validated(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.validating_list = [the_transaction]
        result = find_validated(block, CandidateBlock, unl_nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].dump_json(), the_transaction.dump_json())

    def test_transactions_main_round_1(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.validating_list = [the_transaction]
        result = transactions_main_round_1(block, CandidateBlock, unl_nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].dump_json(), the_transaction.dump_json())

    def test_round_process_round_1(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.validating_list = [the_transaction]
        custom_TEMP_BLOCK_PATH = "db/test_round_process_round_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_round_process_round_1_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_round_process_round_1_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_round_process_round_1_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        old_block = copy.copy(block)
        SaveAccounts(
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000),
            custom_TEMP_ACCOUNTS_PATH,
        )
        custom_fee_address = "onuratakanulusoy"
        result = round_process_round_1(
            block,
            CandidateBlock,
            unl_nodes,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            custom_fee_address=custom_fee_address,
            clean=False,
        )
        self.assertEqual(len(result.validating_list), 2)
        self.assertEqual(
            result.validating_list[0].dump_json(), the_transaction.dump_json()
        )
        self.assertEqual(result.validating_list[1].toUser, "onuratakanulusoy")
        self.assertEqual(result.validating_list[1].amount, 0.02)
        self.assertEqual(result.round_1, True)
        self.assertNotEqual(
            result.round_2_starting_time, old_block.round_2_starting_time
        )
        self.assertNotEqual(result.hash, old_block.hash)

        the_account_list = GetAccounts(
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH
        )
        the_account_list.execute(
            f"SELECT * FROM account_list WHERE address = '{the_transaction.toUser}'"
        )
        second_list = the_account_list.fetchall()

        self.assertEqual(second_list, [("onur", 0, 5000)])

        block_2 = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

        self.assertEqual(result.dump_json(), block_2.dump_json())

    def test_consensus_round_1_false(self):
        custom_TEMP_BLOCK_PATH = "db/test_consensus_round_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_consensus_round_1_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        custom_UNL_NODES_PATH = UNL_NODES_PATH.replace(".json", "_test.json")

        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(5)], [data_block_hash for i in range(5)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(5):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(5)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)
        self.assertFalse(
            consensus_round_1(
                block,
                custom_candidate_class=CandidateBlock,
                custom_unl_nodes=unl_nodes,
                custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
                custom_server=self.node_0,
                custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
                custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
                custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            )
        )

    def test_consensus_round_1(self):
        custom_TEMP_BLOCK_PATH = "db/test_consensus_round_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_consensus_round_1_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        custom_UNL_NODES_PATH = UNL_NODES_PATH.replace(".json", "_test.json")

        custom_server = None

        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "onur",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur",
            "sequence_number": 58,
            "signature": "onur",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)
        self.assertTrue(
            consensus_round_1(
                block,
                CandidateBlock,
                unl_nodes,
                custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
                custom_server=custom_server,
                custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
                custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
                custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            )
        )

    def test_time_difference_check_round_2_false_time(self):
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2

        self.assertFalse(time_difference_check_round_2(block))

    def test_time_difference_check_round_2(self):
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)

        self.assertTrue(time_difference_check_round_2(block))

    def test_round_check_round_2_false_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }
        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        self.assertFalse(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_round_check_round_2_true_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(6)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        self.assertFalse(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_round_check_round_2_false_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        self.assertFalse(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_round_check_round_2_true_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(6)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        self.assertTrue(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_process_candidate_blocks_hashes_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "signature",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
            "previous_hash": "previous_hash",
            "signature": "signature",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(5)], [data_block_hash for i in range(5)]
        )
        the_new_list = []
        for i in range(5):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        result = process_candidate_blocks_hashes(block, CandidateBlock, unl_nodes)
        self.assertEqual(result["hash"]["hash"], False)

    def test_process_candidate_blocks_hashes(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "signature",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "signature": "signature",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        expected_result = copy.copy(data_block_hash)
        expected_result["sender"] = 5
        self.assertEqual(
            process_candidate_blocks_hashes(block, CandidateBlock, unl_nodes)["hash"],
            expected_result,
        )

    def test_process_candidate_blocks_hashes_change_self_hashes(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "signature",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "signature": "signature",
        }

        data_block_hash_self = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "signature": "self",
        }

        the_candidate_block_hash_list = [data_block_hash for i in range(6)]
        the_candidate_block_hash_list[5] = data_block_hash_self

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], the_candidate_block_hash_list
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            if i == 5:
                the_new_object["signature"] = "self"
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        expected_result = copy.copy(data_block_hash)
        expected_result["sender"] = 0
        self.assertEqual(
            process_candidate_blocks_hashes(block, CandidateBlock, unl_nodes)["hash"],
            expected_result,
        )

    def test_validate_main(self):
        block = Block("Onur")
        old_block = copy.copy(block)
        result = validate_main(block)
        self.assertEqual(result.validated, True)
        self.assertEqual(result.round_2, True)
        self.assertNotEqual(old_block.validated_time, result.validated_time)

    def test_rescue_main(self):
        block = Block("Onur")
        data_block_hash = {
            "action": "myblockhash",
            "hash": {"hash": "onur from tests", "sender": self.node_0.id},
            "sequence_number": 58,
            "sender": self.node_0.id,
        }
        old_block = copy.copy(block)
        result = rescue_main(
            block,
            data_block_hash,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
        )
        self.assertEqual(result.dowload_true_block, data_block_hash["sender"])

    def test_round_process_round_2_false_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "onur from tests",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
            "previous_hash": "previous_hash",
            "signature": "onur from tests",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(5)], [data_block_hash for i in range(5)]
        )
        the_new_list = []
        for i in range(5):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"

        result = round_process_round_2(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )

        self.assertIsNone(result)

    def test_round_process_round_2_false_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "sender": self.node_0.id,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "Different hash"

        result = round_process_round_2(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )

        self.assertEqual(result, False)
        self.assertEqual(block.dowload_true_block, 5)

    def test_round_process_round_2_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "signature",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "sender": self.node_0.id,
            "signature": "signature",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        old_block = copy.copy(block)
        result = round_process_round_2(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )

        self.assertTrue(result)
        self.assertEqual(block.validated, True)
        self.assertEqual(block.round_2, True)
        self.assertNotEqual(old_block.validated_time, block.validated_time)

    def test_consensus_round_2_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequence_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(5)], [data_block_hash for i in range(5)]
        )
        the_new_list = []
        for i in range(5):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        old_block = copy.copy(block)

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        result = consensus_round_2(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )
        self.assertFalse(result)

    def test_consensus_round_2(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur",
            "sequence_number": 58,
            "sender": self.node_0.id,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        old_block = copy.copy(block)

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        result = consensus_round_2(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )
        self.assertTrue(result)
        self.assertEqual(block.validated, True)
        self.assertEqual(block.round_2, True)
        self.assertNotEqual(old_block.validated_time, block.validated_time)

    def test_ongoing_main_round_1(self):
        custom_TEMP_BLOCK_PATH = "db/test_consensus_round_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_consensus_round_1_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        custom_UNL_NODES_PATH = UNL_NODES_PATH.replace(".json", "_test.json")

        custom_server = None

        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        old_block = copy.copy(block)
        time.sleep(4)
        custom_fee_address = "onurtheprofessional"
        result = ongoing_main(
            block,
            CandidateBlock,
            unl_nodes,
            custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
            custom_server=custom_server,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            custom_fee_address=custom_fee_address,
            clean=False,
        )
        self.assertEqual(len(result.validating_list), 2)
        self.assertEqual(
            result.validating_list[0].dump_json(), the_transaction.dump_json()
        )
        self.assertEqual(result.validating_list[1].toUser, "onurtheprofessional")
        self.assertEqual(result.validating_list[1].amount, 0.02)
        self.assertEqual(result.round_1, True)
        self.assertNotEqual(
            result.round_2_starting_time, old_block.round_2_starting_time
        )
        self.assertNotEqual(result.hash, old_block.hash)

    def test_ongoing_main_round_1_clean(self):
        custom_TEMP_BLOCK_PATH = "db/test_consensus_round_1_TEMP_BLOCK_PATH.json"
        custom_TEMP_ACCOUNTS_PATH = "db/test_consensus_round_1_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_consensus_round_1_TEMP_BLOCKSHASH_PART_PATH.json"
        )
        custom_UNL_NODES_PATH = UNL_NODES_PATH.replace(".json", "_test.json")

        custom_server = None

        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "previous_hash",
            "sequence_number": 58,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }
        new_list = []
        for i in range(6):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(6)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        old_block = copy.copy(block)
        time.sleep(4)
        custom_fee_address = "onurtheprofessional"
        result = ongoing_main(
            block,
            CandidateBlock,
            unl_nodes,
            custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
            custom_server=custom_server,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            custom_fee_address=custom_fee_address,
        )
        self.assertEqual(len(result.validating_list), 0)

        self.assertEqual(result.round_1, True)
        self.assertNotEqual(
            result.round_2_starting_time, old_block.round_2_starting_time
        )
        self.assertNotEqual(result.hash, old_block.hash)

    def test_ongoing_main_round_2(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur from tests",
            "sequence_number": 58,
            "sender": self.node_0.id,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.round_1 = True
        block.hash = "onur from tests"
        old_block = copy.copy(block)

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        result = ongoing_main(
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
            pass_sync=True,
        )
        self.assertTrue(result)
        self.assertEqual(block.validated, True)
        self.assertEqual(block.round_2, True)
        self.assertNotEqual(old_block.validated_time, block.validated_time)

    def test_consensus_trigger_ongoing(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        validating_list = [the_transaction_json, the_transaction_json]

        data_block = {
            "transaction": validating_list,
            "sequence_number": 58,
            "signature": "a",
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "previous_hash": "onur",
            "sequence_number": 58,
            "sender": self.node_0.id,
            "signature": "a",
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(6)], [data_block_hash for i in range(6)]
        )
        the_new_list = []
        for i in range(6):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.round_1 = True
        block.hash = "onur from tests"

        block.validating_list = [Transaction.load_json(i) for i in validating_list]
        old_block = copy.copy(block)

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        result = calculate(
            consensus_trigger,
            block,
            CandidateBlock,
            unl_nodes,
            custom_server=self.node_1,
            custom_unl=self.node_1.clients[0],
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertTrue(result[1])
        self.assertLess(result[0], 1)
        self.assertEqual(block.validated, True)
        self.assertEqual(block.round_2, True)
        self.assertNotEqual(old_block.validated_time, block.validated_time)

    def test_consensus_trigger_finished(self):
        custom_TEMP_BLOCK_PATH = "db/test_consensus_trigger_finished.json"
        custom_BLOCKS_PATH = "db/test_consensus_trigger_finished/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_consensus_trigger_finished_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_consensus_trigger_finished_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_consensus_trigger_finished_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onur")
        block.round_1 = True
        block.round_2 = True
        block.validated = True

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_a = copy.copy(the_transaction)
        the_transaction_a.signature = "a"
        block.validating_list = [the_transaction, the_transaction_a]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        time.sleep(1)

        result = calculate(
            consensus_trigger,
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertTrue(result[1])
        self.assertLess(result[0], 2)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

    def test_Remove_Duplicates(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "test_SavePending_GetPending",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)

        block = Block("onur")
        block.validating_list = [the_transaction, copy.copy(the_transaction)]
        block = Remove_Duplicates(block)
        self.assertEqual(len(block.validating_list), 1)

    def test_sync_send_block_exception(self):
        block = Block("onur")
        sync(block, custom_server=self.node_1, send_block_error=True)

    def test_sync_send_block_hash_exception(self):
        block = Block("onur")
        sync(block, custom_server=self.node_1, send_block_hash_error=True)

    def test_sync_send_transaction_exception(self):
        block = Block("onur")
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "test_SavePending_GetPending",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        block.validating_list = [the_transaction, copy.copy(the_transaction)]
        sync(block, custom_server=self.node_1, send_transaction_error=True)

    def test_sync_send_transaction_exception_pending(self):
        block = Block("onur")
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "test_SavePending_GetPending",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        pending_validating_list = [the_transaction, copy.copy(the_transaction)]
        sync(
            block,
            custom_server=self.node_1,
            send_transaction_error=True,
            pending_list_txs=pending_validating_list,
        )


unittest.main(exit=False)
