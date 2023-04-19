#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
from hashlib import sha256

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import threading
import time
import unittest
import urllib

import requests

from unittest.mock import MagicMock

import naruno
from naruno.accounts.account import Account
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.get_balance import GetBalance
from naruno.accounts.save_accounts import SaveAccounts
from naruno.api.main import start
from naruno.apps.remote_app import Integration
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import (GetBlockshash,
                                                 GetBlockshash_part)
from naruno.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.config import (CONNECTED_NODES_PATH, LOADING_ACCOUNTS_PATH,
                           LOADING_BLOCK_PATH, LOADING_BLOCKSHASH_PART_PATH,
                           LOADING_BLOCKSHASH_PATH, MY_TRANSACTION_EXPORT_PATH,
                           MY_TRANSACTION_PATH, PENDING_TRANSACTIONS_PATH,
                           TEMP_ACCOUNTS_PATH, TEMP_BLOCK_PATH,
                           TEMP_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PATH)
from naruno.consensus.finished.finished_main import finished_main
from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.config_system import get_config
from naruno.lib.mix.merkle_root import MerkleTree
from naruno.lib.settings_system import (save_settings, t_mode_settings,
                                        the_settings)
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from naruno.transactions.pending.delete_pending import DeletePending
from naruno.transactions.pending.get_pending import GetPendingLen
from naruno.transactions.transaction import Transaction
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.print_wallets import print_wallets
from naruno.wallet.save_wallet_list import save_wallet_list
from naruno.wallet.wallet_create import wallet_create
from naruno.wallet.wallet_import import Address, wallet_import

from naruno.apps.checker import checker

naruno.api.main.custom_block = Block("Onur")
naruno.api.main.custom_current_time = int(time.time()) + 25
naruno.api.main.custom_sequence_number = 0
naruno.api.main.custom_balance = 100000

naruno.api.main.custom_TEMP_BLOCK_PATH = "db/test_API_BLOCK_PATH.json"
naruno.api.main.custom_TEMP_ACCOUNTS_PATH = "db/test_API_ACCOUNTS_PATH.json"
naruno.api.main.custom_TEMP_BLOCKSHASH_PATH = "db/test_API_BLOCKSHASH_PATH.json"
naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = (
    "db/test_API_BLOCKSHASH_PART_PATH.json")

the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15, 1)
temp_path = "db/test_API.db"
SaveAccounts(the_account_2, temp_path)

naruno.api.main.account_list = GetAccounts(temp_path)

a_account = Account("<address>", 1000)
SaveAccounts([a_account], "db/test_send_coin_data_page_data.db")
the_accounts = GetAccounts("db/test_send_coin_data_page_data.db")
naruno.api.main.custom_account_list = the_accounts

naruno.api.main.custom_wallet = "test_account_2"

send_called = False
send_called_txs = []


def custom_send_function(self, a, b, c, d, e):
    global send_called
    global send_called_txs
    send_called = True
    send_called_txs.append([a, b, c, d, e])
    return True


class Test_apps(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.integration = Integration("test1", wait_amount=1)
        cls.mock_logger = MagicMock()
        CleanUp_tests()
        naruno.api.main.account_list = GetAccounts(temp_path)

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
        naruno.api.main.custom_server = cls.node_0
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.integration.close()
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

    def test_integration_caching_system(self):
        app_name = f"test_app_{int(time.time())}"
        integration_1 = Integration(app_name, port=7776)
        integration_1.cache.append(
            "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
        )
        integration_1.save_cache()
        self.assertEqual(
            os.path.exists(
                f"db/remote_app_cache/{integration_1.cache_name}.cache"),
            True,
        )

        integration_2 = Integration(app_name, port=7776)
        self.assertEqual(
            integration_2.cache,
            [
                "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
            ],
        )
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

        integration_3 = Integration(app_name, port=7776)
        self.assertEqual(integration_3.cache, [])
        integration_3.delete_cache()

    def test_integration_send_and_get_tx_sended_not_validated(self):
        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended_not_validated=True,
            wait_amount=1,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([], clear=True)

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(
            integration.send("hello_text", "hello", "<address>", force=False),
            True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
            force=False,
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
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_sended_validated(self):
        integration = Integration(
            f"test_app_{int(time.time())}",
            host="localhost",
            port=7776,
            password="123",
            sended=True,
            sended_not_validated=False,
            wait_amount=1,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([], clear=True)

        password = "123"

        self.assertEqual(
            integration.send("hello_text", "hello", "<address>", force=False),
            True)

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
            force=False,
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
        SaveMyTransaction(backup, clear=True)
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
            wait_amount=1,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([], clear=True)

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(
            integration.send("hello_text",
                             "hello",
                             wallet_import(-1, 3),
                             force=False),
            True,
        )

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
            force=False,
        )

        self.assertEqual(second_try, False)

        the_txs = GetMyTransaction()
        for txs in the_txs:
            if txs[0].toUser == wallet_import(-1, 3):
                os.remove(
                    os.path.join(
                        MY_TRANSACTION_PATH,
                        "sended" +
                        sha256(txs[0].signature.encode("utf-8")).hexdigest(),
                    ))

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, wallet_import(-1, 3))

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
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
            wait_amount=1,
        )

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([], clear=True)

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7776/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(
            integration.send("hello_text",
                             "hello",
                             wallet_import(-1, 3),
                             force=False),
            True,
        )

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
            force=False,
        )

        self.assertEqual(second_try, False)

        the_txs = GetMyTransaction()
        for txs in the_txs:
            if txs[0].toUser == wallet_import(-1, 3):
                os.remove(
                    os.path.join(
                        MY_TRANSACTION_PATH,
                        "sended" +
                        sha256(txs[0].signature.encode("utf-8")).hexdigest(),
                    ))

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        integration.get_cache()
        self.assertNotEqual(integration.cache, [])
        integration.disable_cache()
        integration.get_cache()
        self.assertEqual(integration.cache, [])

        print("aaaaaaAAAAAAAAAAAAaaaaaaaaaaAAAAAAAAAAAAAAAAAAaaaaaaaaaaa")

        second_gettings_data_from_app = integration.get()
        self.assertNotEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"{integration.app_name}hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, wallet_import(-1, 3))

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_caching_system_backward_support(self):
        app_name = f"test_app_{int(time.time())}"
        integration_1 = Integration(app_name, port=7776)
        integration_1.cache.append("test")
        integration_1.save_cache()
        self.assertEqual(
            os.path.exists(
                f"db/remote_app_cache/{integration_1.cache_name}.cache"),
            True,
        )

        integration_2 = Integration(app_name, port=7776)
        self.assertEqual(integration_2.cache, [])
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

        integration_3 = Integration(app_name, port=7776)
        self.assertEqual(integration_3.cache, [])
        integration_3.delete_cache()

    def test_checker_with_valid_transactions(self):
        # Create some sample transactions
        sent_tx1 = [1, 2, "userA", 4, 5, 6,
                    '{"action": "foo", "app_data": {"a": 1, "b": 2}}']
        sent_tx2 = [7, 8, "userB", 10, 11, 12,
                    '{"action": "bar", "app_data": {"c": 3, "d": 4}}']
        validated_tx1 = {"toUser": "userA", "data": {
            "action": "foo", "app_data": {"a": 1, "b": 2}}}
        validated_tx2 = {"toUser": "userB", "data": {
            "action": "bar", "app_data": {"c": 3, "d": 4}}}

        # Set up the Integration object with some previously sent and validated transactions
        self.integration.sended_txs = [sent_tx1, sent_tx2]
        new_txs = [validated_tx1, validated_tx2]
        self.integration.get = MagicMock(return_value=new_txs)

        global send_called
        send_called = False
        self.integration.send = custom_send_function

        # Call the checker function
        checker(self.integration)

        # Assert that the send method was not called (since all transactions were validated)
        self.assertFalse(send_called)

    def test_checker_with_invalid_transaction(self):

        # Create a sample transaction and set up the Integration object with it
        sent_tx1 = [1, 2, "userA", 4, 5, 6,
                    '{"action": "foo", "app_data": {"a": 1, "b": 2}}']
        sent_tx2 = [7, 8, "userB", 10, 11, 12,
                    '{"action": "bar", "app_data": {"c": 3, "d": 4}}']
        sent_tx3 = [7, 8, "userC", 10, 11, 12,
                    '{"action": "bar", "app_data": {"c": 3, "d": 4}}']
        validated_tx = {"toUser": "userd", "data": {
            "action": "foo", "app_data": {"a": 1, "b": 2}}}
        self.integration.sended_txs = [sent_tx1, sent_tx2, sent_tx3]
        new_txs = [validated_tx]
        self.integration.get = MagicMock(return_value=new_txs)

        global send_called
        global send_called_txs
        send_called_txs = []
        send_called = False
        self.integration.send = custom_send_function

        # Call the checker function
        checker(self.integration)

        # Assert that the send method was called with the correct arguments
        self.assertTrue(send_called)
        self.assertEqual(send_called_txs, [[2, 'userA', 4, 5, 6], [
                         8, 'userB', 10, 11, 12], [8, 'userC', 10, 11, 12]])

    def test_checker_with_invalid_transaction_limited(self):

        # Create a sample transaction and set up the Integration object with it
        sent_tx1 = [1, 2, "userA", 4, 5, 6,
                    '{"action": "foo", "app_data": {"a": 1, "b": 2}}']
        sent_tx2 = [7, 8, "userB", 10, 11, 12,
                    '{"action": "bar", "app_data": {"c": 3, "d": 4}}']
        sent_tx3 = [7, 8, "userC", 10, 11, 12,
                    '{"action": "bar", "app_data": {"c": 3, "d": 4}}']
        validated_tx = {"toUser": "userd", "data": {
            "action": "foo", "app_data": {"a": 1, "b": 2}}}
        self.integration.sended_txs = [sent_tx1, sent_tx2, sent_tx3]
        new_txs = [validated_tx]
        self.integration.get = MagicMock(return_value=new_txs)

        global send_called
        global send_called_txs
        send_called_txs = []
        send_called = False
        self.integration.send = custom_send_function

        # Call the checker function
        self.integration.max_tx_number = 4
        checker(self.integration)

        # Assert that the send method was called with the correct arguments
        self.assertTrue(send_called)
        self.assertEqual(send_called_txs, [
                         [2, 'userA', 4, 5, 6], [8, 'userB', 10, 11, 12]])

    def test_checker_error_handling(self):
        # Set the get method to raise an exception
        self.integration.get = MagicMock(
            side_effect=Exception("Something went wrong"))

        # Call the checker function and assert that an error was logged
        checker(self.integration, logger=self.mock_logger)
        self.mock_logger.error.assert_called_once()


unittest.main(exit=False)
