#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet

from decentra_network.wallet.ellipticcurve.save_wallet_list import save_wallet_list
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import copy
import time
import unittest

from speed_calculator import calculate

from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.get_block_from_blockchain_db import (
    GetBlockstoBlockchainDB,
)
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import (
    candidate_block,
)
from decentra_network.config import (
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
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.consensus.finished.finished_main import finished_main
from decentra_network.consensus.finished.transactions.transactions_main import (
    transactions_main as transactions_main_finished,
)
from decentra_network.consensus.ongoing.ongoing_main import ongoing_main
from decentra_network.consensus.rounds.round_1.checks.candidate_blocks.candidate_blocks_main import (
    candidate_blocks_check,
)
from decentra_network.consensus.rounds.round_1.checks.checks_main import (
    round_check as round_check_round_1,
)
from decentra_network.consensus.rounds.round_1.checks.time.time_difference.time_difference_main import (
    time_difference_check as time_difference_check_round_1,
)
from decentra_network.consensus.rounds.round_1.process.process_main import (
    round_process as round_process_round_1,
)
from decentra_network.consensus.rounds.round_1.process.transactions.checks.duplicated import (
    Remove_Duplicates,
)
from decentra_network.consensus.rounds.round_1.process.transactions.find_newly.find_newly_main import (
    find_newly,
)
from decentra_network.consensus.rounds.round_1.process.transactions.find_validated.find_validated_main import (
    find_validated,
)
from decentra_network.consensus.rounds.round_1.process.transactions.transactions_main import (
    transactions_main as transactions_main_round_1,
)
from decentra_network.consensus.rounds.round_1.round_1_main import consensus_round_1
from decentra_network.consensus.rounds.round_2.checks.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    candidate_blocks_hashes_check,
)
from decentra_network.consensus.rounds.round_2.checks.checks_main import (
    round_check as round_check_round_2,
)
from decentra_network.consensus.rounds.round_2.checks.time.time_difference.time_difference_main import (
    time_difference_check as time_difference_check_round_2,
)
from decentra_network.consensus.rounds.round_2.process.candidate_blocks_hashes.candidate_blocks_hashes_main import (
    process_candidate_blocks_hashes,
)
from decentra_network.consensus.rounds.round_2.process.process_main import (
    round_process as round_process_round_2,
)
from decentra_network.consensus.rounds.round_2.process.rescue.rescue_main import (
    rescue_main,
)
from decentra_network.consensus.rounds.round_2.process.validate.validate_main import (
    validate_main,
)
from decentra_network.consensus.rounds.round_2.round_2_main import consensus_round_2
from decentra_network.consensus.time.true_time.true_time_main import true_time
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.my_transactions.get_my_transaction import (
    GetMyTransaction,
)
from decentra_network.transactions.my_transactions.save_my_transaction import (
    SaveMyTransaction,
)
from decentra_network.transactions.my_transactions.save_to_my_transaction import (
    SavetoMyTransaction,
)
from decentra_network.transactions.my_transactions.validate_transaction import (
    ValidateTransaction,
)
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


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
        block.sequance_number = 0
        block.empty_block_number = 100
        self.assertFalse(true_time(block=block))

    def test_true_time(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 2
        block.sequance_number = 1
        block.empty_block_number = 1
        time.sleep(7)
        self.assertTrue(true_time(block=block))

    def test_transactions_main_finished(self):
        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"
        wallet_create(password)
        wallet_create(password)

        backup = GetMyTransaction()
        block = Block("Onur")
        the_transaction_json = {
            "sequance_number": 1,
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
        self.assertEqual(
            result,
            [
                [the_transaction.dump_json(), True],
                [the_transaction_2.dump_json(), True],
                [the_transaction_3.dump_json(), True],
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
            "db/test_finished_main_TEMP_BLOCKSHASH_PART_PATH.json"
        )

        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_check(self):

        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, False)

    def test_candidate_blocks_hashes_check_false(self):

        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        unl_nodes = [i for i in range(10)]
        result = candidate_blocks_hashes_check(CandidateBlock, unl_nodes)
        self.assertIsNot(result, True)

    def test_candidate_blocks_hashes_check(self):

        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        self.assertFalse(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_round_check_round_1_false_true(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        CandidateBlock.candidate_blocks = [data_block for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        time.sleep(4)
        self.assertTrue(round_check_round_1(block, CandidateBlock, unl_nodes))

    def test_find_newly(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(1)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(8):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(8):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(8):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
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
        result = round_process_round_1(
            block,
            CandidateBlock,
            unl_nodes,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertEqual(len(result.validating_list), 1)
        self.assertEqual(
            result.validating_list[0].dump_json(), the_transaction.dump_json()
        )
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(7):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(8):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        self.assertFalse(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_round_check_round_2_false_true(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        CandidateBlock.candidate_block_hashes = [data_block_hash for i in range(8)]
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.round_2_starting_time = time.time()
        block.round_2_time = 2
        time.sleep(4)
        self.assertTrue(round_check_round_2(block, CandidateBlock, unl_nodes))

    def test_process_candidate_blocks_hashes_false(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        the_new_list = []
        for i in range(7):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        result = process_candidate_blocks_hashes(block, CandidateBlock, unl_nodes)
        self.assertEqual(result["hash"], False)

    def test_process_candidate_blocks_hashes(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
            the_new_object = copy.copy(data_block_hash)
            the_new_object["sender"] = i
            the_new_list.append(the_new_object)
        CandidateBlock.candidate_block_hashes = the_new_list
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")
        block.hash = "onur from tests"
        expected_result = copy.copy(data_block_hash)
        expected_result["sender"] = 0
        self.assertEqual(
            process_candidate_blocks_hashes(block, CandidateBlock, unl_nodes),
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
            "hash": "onur from tests",
            "sequance_number": 58,
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        the_new_list = []
        for i in range(7):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
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
        self.assertEqual(block.dowload_true_block, 0)

    def test_round_process_round_2_true(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(7)]
        )
        the_new_list = []
        for i in range(7):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
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
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(8)], [data_block_hash for i in range(7)]
        )
        validating_list = [the_transaction, the_transaction]

        data_block = {
            "signature": -1,
            "transaction": validating_list,
            "sequance_number": 58,
        }
        new_list = []
        for i in range(8):
            new_block = copy.copy(data_block)
            new_block["signature"] = i
            new_list.append(new_block)
        CandidateBlock.candidate_blocks = new_list
        CandidateBlock.candidate_blocks_hash = [data_block_hash for i in range(7)]
        unl_nodes = [i for i in range(10)]
        block = Block("Onur")

        block.start_time = time.time()
        block.round_1_time = 2
        old_block = copy.copy(block)
        time.sleep(4)
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
        )
        self.assertEqual(len(result.validating_list), 1)
        self.assertEqual(
            result.validating_list[0].dump_json(), the_transaction.dump_json()
        )
        self.assertEqual(result.round_1, True)
        self.assertNotEqual(
            result.round_2_starting_time, old_block.round_2_starting_time
        )
        self.assertNotEqual(result.hash, old_block.hash)

    def test_ongoing_main_round_2(self):
        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
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
        )
        self.assertTrue(result)
        self.assertEqual(block.validated, True)
        self.assertEqual(block.round_2, True)
        self.assertNotEqual(old_block.validated_time, block.validated_time)

    def test_consensus_trigger_ongoing(self):

        the_transaction_json = {
            "sequance_number": 1,
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
            "sequance_number": 58,
        }

        data_block_hash = {
            "action": "myblockhash",
            "hash": "onur from tests",
            "sequance_number": 58,
            "sender": self.node_0.id,
        }

        CandidateBlock = candidate_block(
            [data_block for i in range(7)], [data_block_hash for i in range(8)]
        )
        the_new_list = []
        for i in range(8):
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
        block.validated = True

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        the_transaction_json = {
            "sequance_number": 1,
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
        )
        self.assertTrue(result[1])
        self.assertLess(result[0], 1)

        result_2 = GetBlockstoBlockchainDB(
            sequance_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        self.assertIsNot(result_2, False)

    def test_Remove_Duplicates(self):

        the_transaction_json = {
            "sequance_number": 1,
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


unittest.main(exit=False)
