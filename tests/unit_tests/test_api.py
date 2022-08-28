#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import threading
import unittest
import urllib

import decentra_network
from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.api.main import start
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import (
    CONNECTED_NODES_PATH, LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH, LOADING_BLOCKSHASH_PATH,
    PENDING_TRANSACTIONS_PATH, TEMP_ACCOUNTS_PATH, TEMP_BLOCK_PATH,
    TEMP_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PATH)
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.settings_system import save_settings, the_settings
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from decentra_network.transactions.pending.delete_pending import DeletePending
from decentra_network.transactions.pending.get_pending import GetPendingLen
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.get_saved_wallet import \
    get_saved_wallet
from decentra_network.wallet.ellipticcurve.save_wallet_list import \
    save_wallet_list
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create
from decentra_network.wallet.print_wallets import print_wallets

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
temp_path = "db/Test_API.db"
SaveAccounts(the_account_2, temp_path)

decentra_network.api.main.account_list = GetAccounts(temp_path)

decentra_network.api.main.custom_wallet = "test_account_2"


class Test_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

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

        cls.result = start(port=7777, test=True)
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

    def test_print_wallets_page(self):
        response = urllib.request.urlopen("http://localhost:7777/wallet/print")
        result = str(json.loads(response.read())).replace("'", """\"""")

        data = str(json.dumps(print_wallets()))

        self.assertEqual(result, data)

    def test_change_wallet_page(self):
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        temp_private_key = wallet_create(password)
        temp_private_key_2 = wallet_create(password)

        response = urllib.request.urlopen(
            "http://localhost:7777/wallet/change/1")
        result = str(json.loads(response.read())).replace("'", """\"""")

        data = str(json.dumps(print_wallets()))

        self.assertEqual(result, data)

        control = False
        if "CURRENTLY USED" in print_wallets()[1]:
            control = True

        self.assertTrue(control)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_create_wallet_page(self):
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        result = str(json.loads(response.read())).replace("'", """\"""")

        data = str(json.dumps(print_wallets()))

        self.assertEqual(result, data)
        self.assertEqual(len(print_wallets()), 2)

        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_delete_wallets_page(self):
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})

        password = "123"

        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        response = urllib.request.urlopen(
            "http://localhost:7777/wallet/change/1")
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/delete")
        result = str(json.loads(response.read())).replace("'", """\"""")

        data = str(json.dumps(print_wallets()))

        self.assertEqual(result, data)
        self.assertEqual(len(print_wallets()), 1)

        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_send_coin_page(self):

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        response = urllib.request.urlopen(
            f"http://localhost:7777/send/coin/<address>/5000/{password}")
        response_result = response.read()

        time.sleep(3)

        self.assertNotEqual(response_result, b"false\n")
        the_tx = Transaction.load_json(
            json.loads(response_result.decode("utf-8")))

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_send_coin_data_page(self):

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        response = urllib.request.urlopen(
            f"http://localhost:7777/send/coin-data/<address>/5000/<data>/{password}"
        )
        response_result = response.read()

        time.sleep(3)

        self.assertNotEqual(response_result, b"false\n")
        the_tx = Transaction.load_json(
            json.loads(response_result.decode("utf-8")))
        self.assertEqual(the_tx.data, "<data>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_balance_wallets_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/wallet/balance")
        response_result = response.read()

        self.assertEqual(response_result, b"-985\n")

    def test_node_start_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/node/start/0.0.0.0/7778")
        first_len = len(self.node_0.clients)
        self.node_0.connect("0.0.0.0", 7778)
        time.sleep(2)
        second_len = len(self.node_0.clients)
        self.assertNotEqual(first_len, second_len)

    def test_node_stop_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/node/start/0.0.0.0/7779")
        response = urllib.request.urlopen(
            "http://localhost:7777/node/stop")            
        first_len = len(self.node_0.clients)
        with contextlib.suppress(ConnectionRefusedError):
            self.node_0.connect("0.0.0.0", 7779)
        time.sleep(2)
        second_len = len(self.node_0.clients)
        self.assertEqual(first_len, second_len)

unittest.main(exit=False)
