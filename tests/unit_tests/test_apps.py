#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import threading
import time
import unittest
import urllib

import requests

import decentra_network
from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.get_balance import GetBalance
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.api.main import start
from decentra_network.apps.apps_trigger import AppsTrigger
from decentra_network.apps.remote_app import Integration
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import (GetBlockshash,
                                                           GetBlockshash_part)
from decentra_network.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import (
    CONNECTED_NODES_PATH, LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH, LOADING_BLOCKSHASH_PATH,
    MY_TRANSACTION_EXPORT_PATH, PENDING_TRANSACTIONS_PATH, TEMP_ACCOUNTS_PATH,
    TEMP_BLOCK_PATH, TEMP_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PATH)
from decentra_network.consensus.finished.finished_main import finished_main
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.config_system import get_config
from decentra_network.lib.mix.merkle_root import MerkleTree
from decentra_network.lib.settings_system import (save_settings,
                                                  t_mode_settings,
                                                  the_settings)
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.transactions.pending.delete_pending import DeletePending
from decentra_network.transactions.pending.get_pending import GetPendingLen
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.get_saved_wallet import get_saved_wallet
from decentra_network.wallet.print_wallets import print_wallets
from decentra_network.wallet.save_wallet_list import save_wallet_list
from decentra_network.wallet.wallet_create import wallet_create
from decentra_network.wallet.wallet_import import Address, wallet_import

decentra_network.api.main.custom_block = Block("Onur")
decentra_network.api.main.custom_current_time = int(time.time()) + 25
decentra_network.api.main.custom_sequence_number = 0
decentra_network.api.main.custom_balance = 100000

decentra_network.api.main.custom_TEMP_BLOCK_PATH = "db/test_API_BLOCK_PATH.json"
decentra_network.api.main.custom_TEMP_ACCOUNTS_PATH = "db/test_API_ACCOUNTS_PATH.json"
decentra_network.api.main.custom_TEMP_BLOCKSHASH_PATH = (
    "db/test_API_BLOCKSHASH_PATH.json")
decentra_network.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = (
    "db/test_API_BLOCKSHASH_PART_PATH.json")

the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15, 1)
temp_path = "db/test_API.db"
SaveAccounts(the_account_2, temp_path)

decentra_network.api.main.account_list = GetAccounts(temp_path)

a_account = Account("<address>", 1000)
SaveAccounts([a_account], "db/test_send_coin_data_page_data.db")
the_accounts = GetAccounts("db/test_send_coin_data_page_data.db")
decentra_network.api.main.custom_account_list = the_accounts

decentra_network.api.main.custom_wallet = "test_account_2"


class Test_apps(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()
        decentra_network.api.main.account_list = GetAccounts(temp_path)

        cls.custom_TEMP_BLOCK_PATH0 = TEMP_BLOCK_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCK_PATH1 = TEMP_BLOCK_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCK_PATH2 = TEMP_BLOCK_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCK_PATH0 = LOADING_BLOCK_PATH.replace(
            ".json", "_0.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCK_PATH1 = LOADING_BLOCK_PATH.replace(
            ".json", "_1.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCK_PATH2 = LOADING_BLOCK_PATH.replace(
            ".json", "_2.json").replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_ACCOUNTS_PATH0 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_0.db").replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH1 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_1.db").replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH2 = TEMP_ACCOUNTS_PATH.replace(
            ".db", "_2.db").replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH0 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_0.db").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH1 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_1.db").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH2 = LOADING_ACCOUNTS_PATH.replace(
            ".db", "_2.db").replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_BLOCKSHASH_PATH0 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH1 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH2 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH0 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_0.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH1 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_1.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH2 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_2.json").replace("loading_", "test_loading_temp_")

        cls.custom_TEMP_BLOCKSHASH_PART_PATH0 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PART_PATH1 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PART_PATH2 = TEMP_BLOCKSHASH_PART_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH0 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_0.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH1 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_1.json").replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_BLOCKSHASH_PART_PATH2 = LOADING_BLOCKSHASH_PART_PATH.replace(
            ".json", "_2.json").replace("loading_", "test_loading_temp_")

        cls.custom_CONNECTED_NODES_PATH0 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_0")
        cls.custom_CONNECTED_NODES_PATH1 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_1")
        cls.custom_CONNECTED_NODES_PATH2 = CONNECTED_NODES_PATH.replace(
            "connected_nodes", "connected_nodes_test_2")

        cls.custom_PENDING_TRANSACTIONS_PATH0 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_0")
        cls.custom_PENDING_TRANSACTIONS_PATH1 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_1")
        cls.custom_PENDING_TRANSACTIONS_PATH2 = PENDING_TRANSACTIONS_PATH.replace(
            "pending_transactions", "pending_transactions_test_2")

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
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.
            custom_TEMP_BLOCKSHASH_PART_PATH0,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.
            custom_LOADING_BLOCKSHASH_PART_PATH0,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH0,
            custom_PENDING_TRANSACTIONS_PATH=cls.
            custom_PENDING_TRANSACTIONS_PATH0,
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
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.
            custom_TEMP_BLOCKSHASH_PART_PATH1,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.
            custom_LOADING_BLOCKSHASH_PART_PATH1,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH1,
            custom_PENDING_TRANSACTIONS_PATH=cls.
            custom_PENDING_TRANSACTIONS_PATH1,
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
            custom_TEMP_BLOCKSHASH_PART_PATH=cls.
            custom_TEMP_BLOCKSHASH_PART_PATH2,
            custom_LOADING_BLOCKSHASH_PART_PATH=cls.
            custom_LOADING_BLOCKSHASH_PART_PATH2,
            custom_CONNECTED_NODES_PATH=cls.custom_CONNECTED_NODES_PATH2,
            custom_PENDING_TRANSACTIONS_PATH=cls.
            custom_PENDING_TRANSACTIONS_PATH2,
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

        backup = sys.argv
        sys.argv = [sys.argv[0]]

        cls.result = start(port=7776, test=True)
        cls.proc = threading.Thread(target=cls.result.run)
        cls.proc.start()

        sys.argv = backup
        decentra_network.api.main.custom_server = cls.node_0
        time.sleep(2)

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

        cls.result.close()

        CleanUp_tests()

    def test_AppsTrigger_App_not_test_app(self):
        block = Block("onur")
        block.sequence_number = 2
        the_transaction = Transaction(1, 1, 1, 1, 1, 1, 1, 1)
        the_transaction.transaction_time = time.time()
        block.validating_list.append(the_transaction)
        AppsTrigger(block)
        time.sleep(2)
        os.chdir(get_config()["main_folder"])
        self.assertFalse(
            os.path.isfile(
                f"apps/testing_app/{block.validating_list[0].transaction_time}.tx"
            ))

    def test_AppsTrigger_App(self):
        block = Block("onur")
        block.sequence_number = 1
        the_transaction = Transaction(1, 1, 1, 1, 1, 1, 1, 1)
        the_transaction.transaction_time = time.time()
        block.validating_list.append(the_transaction)
        AppsTrigger(block)
        time.sleep(2)
        os.chdir(get_config()["main_folder"])
        self.assertTrue(
            os.path.isfile(
                f"apps/testing_app/{block.validating_list[0].transaction_time}.tx"
            ))

    def test_integration_caching_system(self):
        integration_1 = Integration("test_app")
        integration_1.cache.append("test")
        integration_1.save_cache()
        self.assertEqual(
            os.path.exists(
                f"db/remote_app_cache/{integration_1.cache_name}.cache"),
            True,
        )

        integration_2 = Integration("test_app")
        self.assertEqual(integration_2.cache, ["test"])
        self.assertEqual(
            os.path.exists(
                f"db/remote_app_cache/{integration_1.cache_name}.cache"),
            True,
        )

        integration_2.delete_cache()
        self.assertEqual(
            os.path.exists(
                f"db/remote_app_cache/{integration_1.cache_name}.cache"),
            False,
        )

        integration_3 = Integration("test_app")
        self.assertEqual(integration_3.cache, [])
        integration_3.delete_cache()

    def test_integration_send_and_get_tx_sended_not_validated(self):

        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended_not_validated=True,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(integration.send("hello_text", "hello", "<address>"),
                         True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
        )

        self.assertEqual(second_try, False)

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_sended_validated(self):

        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended_not_validated=False,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(integration.send("hello_text", "hello", "<address>"),
                         True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
        )

        self.assertEqual(second_try, False)

        for txs in GetMyTransaction():
            if txs[0].toUser == "<address>":
                ValidateTransaction(txs[0])

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_received(self):

        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended_not_validated=False,
            sended=False,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(integration.send("hello_text", "hello", "<address>"),
                         True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
        )

        self.assertEqual(second_try, False)

        the_txs = GetMyTransaction()
        for txs in the_txs:
            if txs[0].toUser == "<address>":
                the_txs[the_txs.index(txs)][2] = False
        SaveMyTransaction(the_txs)

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_received_disable_cache(self):

        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended_not_validated=False,
            sended=False,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(integration.send("hello_text", "hello", "<address>"),
                         True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
        )

        self.assertEqual(second_try, False)

        the_txs = GetMyTransaction()
        for txs in the_txs:
            if txs[0].toUser == "<address>":
                the_txs[the_txs.index(txs)][2] = False
        SaveMyTransaction(the_txs)

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        integration.disable_cache()

        second_gettings_data_from_app = integration.get()
        self.assertNotEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)


unittest.main(exit=False)
