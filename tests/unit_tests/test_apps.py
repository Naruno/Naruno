#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import json
import os
import sys
from hashlib import sha256

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import threading
import time
import unittest
import urllib
from unittest.mock import MagicMock

import requests

import naruno
from naruno.accounts.account import Account
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.get_balance import GetBalance
from naruno.accounts.save_accounts import SaveAccounts
from naruno.api.main import start
from naruno.apps.checker import checker
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
from naruno.transactions.my_transactions.get_my_transaction import (
    GetMyTransaction, mytransactions_db)
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

naruno.api.main.custom_block = Block("Onur")
naruno.api.main.custom_current_time = int(time.time()) + 25
naruno.api.main.custom_sequence_number = 0
naruno.api.main.custom_balance = 100000

naruno.api.main.custom_TEMP_BLOCK_PATH = "db/test_API_BLOCK_PATH.json"
naruno.api.main.custom_TEMP_ACCOUNTS_PATH = "db/test_API_ACCOUNTS_PATH.json"
naruno.api.main.custom_TEMP_BLOCKSHASH_PATH = "db/test_API_BLOCKSHASH_PATH.json"
naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = (
    "db/test_API_BLOCKSHASH_PART_PATH.json"
)

the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15, 1)
temp_path = "db/test_API.db"
SaveAccounts(the_account_2, temp_path)

naruno.api.main.account_list = GetAccounts(temp_path)

a_account = Account("<address>remoteapp", 1000)
SaveAccounts([a_account], "db/test_send_coin_data_page_data.db")
the_accounts = GetAccounts("db/test_send_coin_data_page_data.db")
naruno.api.main.custom_account_list = the_accounts

naruno.api.main.custom_wallet = "test_account_2"

send_called = False
send_called_txs = []


def custom_send_function(self, a, b, c, d, e):
    """

    :param a: param b:
    :param c: param d:
    :param e: param b:
    :param d: param b:
    :param b:

    """
    print("aaaaaaaaaaaaaaaa")
    global send_called
    global send_called_txs
    send_called = True
    send_called_txs.append([a, b, c, d, e])
    return True


custom_send_function_2_call_number = 0


def custom_send_function_2(self, a, b, force=False):
    """

    :param a: param b:
    :param force: Default value = False)
    :param b:

    """
    global custom_send_function_2_call_number
    if custom_send_function_2_call_number >= 1:
        return True
    custom_send_function_2_call_number += 1

    return False


custom_send_function_3_call_list = []


def custom_send_function_3(action, app_data, to_user, force, retrysecond):
    """

    :param action: param app_data:
    :param to_user: param force:
    :param retrysecond: param app_data:
    :param force: param app_data:
    :param app_data:

    """
    global custom_send_function_3_call_list
    custom_send_function_3_call_list.append(
        [action, app_data, to_user, force, retrysecond]
    )
    return True


def custom_checker_3(a):
    """

    :param a:

    """
    return None


class Test_apps(unittest.TestCase):
    """ """

    @classmethod
    def setUpClass(cls):
        """ """
        cls.integration = Integration("test1", wait_amount=1)
        cls.mock_logger = MagicMock()
        CleanUp_tests()
        naruno.api.main.account_list = GetAccounts(temp_path)

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

        cls.custom_PENDING_TRANSACTIONS_PATH0 = "pending_transactions_test_0"
        cls.custom_PENDING_TRANSACTIONS_PATH1 = "pending_transactions_test_1"
        cls.custom_PENDING_TRANSACTIONS_PATH2 = "pending_transactions_test_2"

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
        """ """
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
        """ """
        app_name = f"test_app_{int(time.time())}"
        integration_1 = Integration(app_name, port=7776)
        integration_1.cache.append(
            "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
        )
        integration_1.save_cache()
        self.assertEqual(
            integration_1.integrationcache_db.get("cache"),
            [
                "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
            ],
        )

        integration_2 = Integration(app_name, port=7776)
        self.assertEqual(
            integration_2.cache,
            [
                "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
            ],
        )

        integration_2.delete_cache()
        self.assertEqual(
            integration_1.integrationcache_db.get("cache"),
            None,
        )
        self.assertEqual(
            integration_2.cache,
            [
                "MEUCIQDXR4toTO/LlWaXU9PeWFruW9/RMbBGtvKCKE70ZSnvMgIgO3A0bHB+nwbE5L/PJ9i65FRgAp/Ac/6NWdN0dj7TSdg="
            ],
        )

        integration_3 = Integration(app_name, port=7776)
        self.assertEqual(integration_3.cache, [])
        integration_3.delete_cache()

    def test_integration_send_and_get_tx_sended_not_validated(self):
        """ """
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
            f"http://localhost:7776/wallet/create/{password}"
        )
        request_body = {
            "data": "<data>",
            "to_user": "<address>remoteapp",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(
            integration.send(
                "hello_text", "hello", "<address>remoteapp", amount=5, force=False
            ),
            True,
        )

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
        text = f"hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>remoteapp")
        self.assertEqual(the_tx.amount, 5)

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_sended_validated(self):
        """ """
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
            integration.send("hello_text", "hello", "<address>remoteapp", force=False),
            True,
        )

        second_try = integration.send(
            "hello_text",
            "hello",
            "<address><address><address><address><address><address><address><address><address><address><address><address><address><address>",
            force=False,
        )

        self.assertEqual(second_try, False)

        for txs in GetMyTransaction():
            if txs[0].toUser == "<address>remoteapp":
                ValidateTransaction(txs[0])

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, "<address>remoteapp")
        self.assertEqual(the_tx.amount, 0.0)

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_received(self):
        """ """
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
            f"http://localhost:7776/wallet/create/{password}"
        )
        request_body = {
            "data": "<data>",
            "to_user": "<address>remoteapp",
            "amount": 5000,
            "password": password,
        }
        self.assertEqual(
            integration.send("hello_text", "hello", wallet_import(-1, 3), force=False),
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
                mytransactions_db.delete(
                    sha256(txs[0].signature.encode("utf-8")).hexdigest() + "sended"
                )

        first_gettings_data_from_app = integration.get()
        self.assertNotEqual(first_gettings_data_from_app, [])

        second_gettings_data_from_app = integration.get()
        self.assertEqual(second_gettings_data_from_app, [])

        integration.delete_cache()

        the_tx = Transaction.load_json(first_gettings_data_from_app[0])
        text = f"hello_text"
        self.assertEqual(the_tx.data, {"action": text, "app_data": "hello"})
        self.assertEqual(the_tx.toUser, wallet_import(-1, 3))

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_integration_send_and_get_tx_received_disable_cache(self):
        """ """
        cache_backup = copy.copy(self.integration.cache)
        self.integration.cache = ["a" * 96]
        self.integration.save_cache()

        self.integration.get_cache()
        self.assertNotEqual(self.integration.cache, [])
        self.integration.disable_cache()
        self.integration.get_cache()
        self.assertEqual(self.integration.cache, [])

        self.integration.cache = cache_backup

    def test_checker_with_valid_transactions(self):
        """ """
        # Create some sample transactions
        sent_tx1 = [
            1,
            2,
            "userA",
            4,
            5,
            6,
            '{"action": "test1foo", "app_data": {"a": 1, "b": 2}}',
        ]
        sent_tx2 = [
            7,
            8,
            "userB",
            10,
            11,
            12,
            '{"action": "test1bar", "app_data": {"c": 3, "d": 4}}',
        ]
        validated_tx1 = {
            "toUser": "userA",
            "data": {"action": "foo", "app_data": {"a": 1, "b": 2}},
        }
        validated_tx2 = {
            "toUser": "userB",
            "data": {"action": "bar", "app_data": {"c": 3, "d": 4}},
        }

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
        """ """
        # Create a sample transaction and set up the Integration object with it
        sent_tx1 = [
            1,
            2,
            "userA",
            4,
            5,
            6,
            '{"action": "foo", "app_data": {"a": 1, "b": 2}}',
        ]
        sent_tx2 = [
            7,
            8,
            "userB",
            10,
            11,
            12,
            '{"action": "bar", "app_data": {"c": 3, "d": 4}}',
        ]
        sent_tx3 = [
            7,
            8,
            "userC",
            10,
            11,
            12,
            '{"action": "bar", "app_data": {"c": 3, "d": 4}}',
        ]
        validated_tx = {
            "toUser": "userd",
            "data": {"action": "foo", "app_data": {"a": 1, "b": 2}},
        }
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
        self.assertEqual(
            send_called_txs,
            [[2, "userA", 4, 5, 6], [8, "userB", 10, 11, 12], [8, "userC", 10, 11, 12]],
        )

    def test_checker_with_invalid_transaction_limited(self):
        """ """
        # Create a sample transaction and set up the Integration object with it
        sent_tx1 = [
            1,
            2,
            "userA",
            4,
            5,
            6,
            '{"action": "foo", "app_data": {"a": 1, "b": 2}}',
        ]
        sent_tx2 = [
            7,
            8,
            "userB",
            10,
            11,
            12,
            '{"action": "bar", "app_data": {"c": 3, "d": 4}}',
        ]
        sent_tx3 = [
            7,
            8,
            "userC",
            10,
            11,
            12,
            '{"action": "bar", "app_data": {"c": 3, "d": 4}}',
        ]
        validated_tx = {
            "toUser": "userd",
            "data": {"action": "foo", "app_data": {"a": 1, "b": 2}},
        }
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
        self.assertEqual(
            send_called_txs, [[2, "userA", 4, 5, 6], [8, "userB", 10, 11, 12]]
        )

    def test_checker_error_handling(self):
        """ """
        # Set the get method to raise an exception
        self.integration.get = MagicMock(side_effect=Exception("Something went wrong"))

        # Call the checker function and assert that an error was logged
        checker(self.integration, logger=self.mock_logger)
        self.mock_logger.error.assert_called_once()

    def test_send_forcer_unsuccess_success(self):
        """ """
        global custom_send_function_2_call_number
        custom_send_function_2_call_number = 0

        self.integration.send = custom_send_function_2
        first_time = time.time()
        result = self.integration.send_forcer("test", "app_data", "user1", 5)
        result_time = time.time()
        # assert that send_forcer() returned True
        self.assertTrue(result)

        # assert that time.sleep() was not called
        self.assertEqual(custom_send_function_2_call_number, 1)
        self.assertGreaterEqual(result_time - first_time, 4)

    def test_send_forcer_success(self):
        """ """
        global custom_send_function_2_call_number
        custom_send_function_2_call_number = 1

        self.integration.send = custom_send_function_2
        first_time = time.time()
        result = self.integration.send_forcer("test", "app_data", "user1", 5)
        result_time = time.time()
        # assert that send_forcer() returned True
        self.assertTrue(result)

        # assert that time.sleep() was not called
        self.assertEqual(custom_send_function_2_call_number, 1)
        self.assertLessEqual(result_time - first_time, 4)

    def test_send_splitter(self):
        """ """
        global custom_send_function_3_call_list
        self.integration.send = custom_send_function_3

        data = {"action": self.integration.app_name + "sddaad", "app_data": "sddaad"}

        system_length = len(
            json.dumps({"action": self.integration.app_name + "sddaad", "app_data": ""})
        )

        true_length = (100 - system_length) - 10
        the_data = ""
        for i in range(150):
            the_data += str(i) + "-"
        result = self.integration.send_splitter(
            "test",
            the_data,
            "user1",
            5,
            true_length,
            system_length,
            custom_checker=custom_checker_3,
            custom_random="11123",
        )

        self.assertEqual(
            custom_send_function_3_call_list,
            [
                ["test", "split-0-11123-", "user1", 41, 10],
                [
                    "test",
                    "split-2-11123-0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-3-11123-15-16-17-18-19-20-21-22-23-24-25-26",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-4-11123--27-28-29-30-31-32-33-34-35-36-37-3",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-5-11123-8-39-40-41-42-43-44-45-46-47-48-49-",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-6-11123-50-51-52-53-54-55-56-57-58-59-60-61",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-7-11123--62-63-64-65-66-67-68-69-70-71-72-7",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-8-11123-3-74-75-76-77-78-79-80-81-82-83-84-",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-9-11123-85-86-87-88-89-90-91-92-93-94-95-96",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-10-11123--97-98-99-100-101-102-103-104-105-1",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-11-11123-06-107-108-109-110-111-112-113-114-",
                    "user1",
                    41,
                    10,
                ],
                [
                    "test",
                    "split-12-11123-115-116-117-118-119-120-121-122-123",
                    "user1",
                    41,
                    10,
                ],
                ["test", "split-1-11123-", "user1", 41, 10],
            ],
        )

    def test_generate_random_split_key(self):
        """ """
        split_key = self.integration.generate_random_split_key()
        self.assertEqual(len(split_key), 5)
        self.assertTrue(split_key.isalpha())

    def test_wait_until_true_time(self):
        """ """
        backup_wait_amount = copy.copy(self.integration.wait_amount)
        backup_last_sended = copy.copy(self.integration.last_sended)

        self.integration.wait_amount = 5
        self.integration.last_sended = time.time() - 3
        start_time = time.time()
        self.integration.wait_until_true_time()
        end_time = time.time()

        self.integration.wait_amount = backup_wait_amount
        self.integration.last_sended = backup_last_sended

        self.assertAlmostEqual(end_time - start_time, 2, delta=0.3)

    def test_wait_until_complated(self):
        """ """
        backup_sending_wait_time = copy.copy(self.integration.sending_wait_time)
        backup_sended_txs = copy.copy(self.integration.sended_txs)
        backup_check_thread = self.integration.check_thread
        self.integration.sending_wait_time = 2
        self.integration.sended_txs = [1, 2, 3]

        custom_list = []
        self.integration.check_thread = threading.Timer(0.5, print)
        self.integration.check_thread.start()
        start_time = time.time()
        self.integration.wait_until_complated(custom_list)
        end_time = time.time()

        self.assertFalse(self.integration.check_thread.is_alive())

        self.integration.sending_wait_time = backup_sending_wait_time
        self.integration.sended_txs = backup_sended_txs
        self.integration.check_thread = backup_check_thread

        self.assertEqual(self.integration.sended_txs, custom_list)
        self.assertAlmostEqual(end_time - start_time, 2, delta=0.3)


backup = sys.argv
sys.argv = [sys.argv[0]]
unittest.main(exit=False)
sys.argv = backup
