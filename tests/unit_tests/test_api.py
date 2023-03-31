#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import copy
import json
import os
import sys
import time
import zipfile
from urllib import response



sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import threading
import unittest
import urllib

import requests

import naruno
from naruno.accounts.get_sequence_number import GetSequanceNumber
from naruno.accounts.account import Account
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.get_balance import GetBalance
from naruno.accounts.save_accounts import SaveAccounts
from naruno.api.main import start
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import (GetBlockshash,
                                                           GetBlockshash_part)
from naruno.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.config import (
    CONNECTED_NODES_PATH, LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH, LOADING_BLOCKSHASH_PATH,
    MY_TRANSACTION_EXPORT_PATH, PENDING_TRANSACTIONS_PATH, TEMP_ACCOUNTS_PATH,
    TEMP_BLOCK_PATH, TEMP_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PATH)
from naruno.consensus.finished.finished_main import finished_main
from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.config_system import get_config
from naruno.lib.mix.merkle_root import MerkleTree
from naruno.lib.settings_system import (save_settings,
                                                  t_mode_settings,
                                                  the_settings)
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
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
naruno.api.main.custom_TEMP_BLOCKSHASH_PATH = (
    "db/test_API_BLOCKSHASH_PATH.json")
naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = (
    "db/test_API_BLOCKSHASH_PART_PATH.json")

the_account_2 = Account("15562b06dc6b1acd6e8c86031e564e0c451c7a73", 15, 1)
temp_path = "db/test_API.db"
SaveAccounts(the_account_2, temp_path)

naruno.api.main.account_list = GetAccounts(temp_path)

a_account = Account("<address>", 1000, sequence_number=1)
ab_account = Account("<addressb>", 1000, sequence_number=1)
SaveAccounts([a_account, ab_account], "db/test_send_coin_data_page_data.db")
the_accounts = GetAccounts("db/test_send_coin_data_page_data.db")
naruno.api.main.custom_account_list = the_accounts

naruno.api.main.custom_wallet = "test_account_2"


def perpetual_time_test():
    os.chdir(get_config()["main_folder"])
    with open("test_block_get_page_off_test.txt", "w") as f:
        f.write("Hello World")


naruno.api.main.custom_consensus_trigger = perpetual_time_test


class Test_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
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

        cls.result = start(port=7777, test=True)
        cls.proc = threading.Thread(target=cls.result.run)
        cls.proc.start()

        sys.argv = backup
        naruno.api.main.custom_server = cls.node_0
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

    def test_send_coin_data_page(self):

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        request_body = {
            "data": "<data>",
            "to_user": "<address>",
            "amount": 5000,
            "password": password,
        }
        response = requests.post("http://localhost:7777/send/",
                                 data=request_body)
        response_result = response.text
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(response_result)
        time.sleep(3)

        self.assertNotEqual(response_result, "false")
        the_tx = Transaction.load_json(json.loads(response_result))
        self.assertEqual(the_tx.data, "<data>")

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_send_coin_data_page_data_no_arg(self):

        backup = GetMyTransaction()
        backup_settings = the_settings()

        original_saved_wallets = get_saved_wallet()
        save_wallet_list({})
        SaveMyTransaction([])

        password = "123"
        response = urllib.request.urlopen(
            f"http://localhost:7777/wallet/create/{password}")
        request_body = {
            "to_user": "<address>",
            "password": password,
        }
        response = requests.post("http://localhost:7777/send/",
                                 data=request_body)
        response_result = response.text
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(response_result)
        time.sleep(3)

        self.assertNotEqual(response_result, "false")
        the_tx = Transaction.load_json(json.loads(response_result))
        self.assertEqual(the_tx.data, "")
        self.assertEqual(the_tx.amount, 0.0)

        new_my_transactions = GetMyTransaction()
        self.assertEqual(len(new_my_transactions), 1)

        DeletePending(the_tx)
        SaveMyTransaction(backup, clear=True)
        save_settings(backup_settings)
        save_wallet_list(original_saved_wallets)

    def test_balance_wallets_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/wallet/balance")
        response_result = response.read()
        the_balance_int = float(
            (response_result.decode("utf-8")).replace("\n", ""))

        self.assertEqual(
            the_balance_int,
            float(
                GetBalance(
                    naruno.api.main.custom_wallet,
                    account_list=naruno.api.main.account_list,
                    block=naruno.api.main.custom_block,
                )),
        )

    def test_node_start_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/node/start/localhost/7778")
        first_len = len(self.node_0.clients)
        time.sleep(2)
        self.node_0.connect("localhost", 7778)
        time.sleep(2)
        second_len = len(self.node_0.clients)
        self.assertNotEqual(first_len, second_len)

    def test_node_stop_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/node/start/localhost/7779")
        time.sleep(2)
        response = urllib.request.urlopen("http://localhost:7777/node/stop")
        time.sleep(2)
        first_len = len(self.node_0.clients)
        with contextlib.suppress(ConnectionRefusedError):
            self.node_0.connect("localhost", 7779)
        time.sleep(2)
        second_len = len(self.node_0.clients)
        self.assertEqual(first_len, second_len)

    def test_node_connect_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/node/start/localhost/7780")
        first_len = len(self.node_0.clients)
        time.sleep(2)
        response = urllib.request.urlopen(
            "http://localhost:7777/node/connect/127.0.0.1/10000")
        time.sleep(2)
        second_len = len(self.node_0.clients)
        self.assertNotEqual(first_len, second_len)

    def test_node_connectmixdb_page(self):
        first_len_0 = len(self.node_0.clients)
        first_len_1 = len(self.node_1.clients)
        first_len_2 = len(self.node_2.clients)

        temp_node = server("127.0.0.1", 10058)
        backup_1 = copy.copy(naruno.api.main.custom_server)
        backup_2 = copy.copy(
            naruno.api.main.custom_CONNECTED_NODES_PATH)
        naruno.api.main.custom_server = temp_node
        naruno.api.main.custom_CONNECTED_NODES_PATH = (
            self.node_0.CONNECTED_NODES_PATH)
        response = urllib.request.urlopen(
            "http://localhost:7777/node/connectmixdb")
        time.sleep(2)

        second_len_0 = len(self.node_0.clients)
        second_len_1 = len(self.node_1.clients)
        second_len_2 = len(self.node_2.clients)
        self.assertEqual(first_len_0, second_len_0)
        self.assertNotEqual(first_len_1, second_len_1)
        self.assertNotEqual(first_len_2, second_len_2)
        temp_node.stop()
        time.sleep(2)
        temp_node.join()

        naruno.api.main.custom_server = backup_1
        naruno.api.main.custom_CONNECTED_NODES_PATH = backup_2

    def test_node_newunl_page(self):
        key = f"onuratakan{str(int(time.time()))}"
        response = urllib.request.urlopen(
            f"http://localhost:7777/node/newunl/?{key}")
        self.assertTrue(Unl.node_is_unl(key))
        Unl.unl_node_delete(key)

    def test_node_id_page(self):
        response = urllib.request.urlopen(f"http://localhost:7777/node/id")
        self.assertEqual(
            ((((response.read()).decode("utf-8")).replace("'", "")).replace(
                """\"""", "")).replace("\n", ""),
            server.id,
        )

    def test_settings_test_on_off_page(self):
        temp_settings = the_settings()
        changed_value = "on" if temp_settings["test_mode"] is False else "off"
        response = urllib.request.urlopen(
            f"http://localhost:7777/settings/test/{changed_value}")
        new_settings = the_settings()
        expected_alue = True if changed_value == "on" else False
        self.assertEqual(new_settings["test_mode"], expected_alue)

        default = "off" if temp_settings["test_mode"] is False else "on"
        response = urllib.request.urlopen(
            f"http://localhost:7777/settings/test/{default}")

        new_settings = the_settings()
        self.assertEqual(new_settings["test_mode"], temp_settings["test_mode"])

    def test_settings_debug_on_off_page(self):
        temp_settings = the_settings()
        changed_value = "on" if temp_settings["debug_mode"] is False else "off"
        response = urllib.request.urlopen(
            f"http://localhost:7777/settings/debug/{changed_value}")
        new_settings = the_settings()
        expected_alue = True if changed_value == "on" else False
        self.assertEqual(new_settings["debug_mode"], expected_alue)

        default = "off" if temp_settings["debug_mode"] is False else "on"
        response = urllib.request.urlopen(
            f"http://localhost:7777/settings/debug/{default}")

        new_settings = the_settings()
        self.assertEqual(new_settings["debug_mode"],
                         temp_settings["debug_mode"])

    def test_block_get_page_off_test(self):
        temp_settings = the_settings()
        t_mode_settings(False)
        first_len = len(self.node_0.our_messages)

        response = urllib.request.urlopen("http://localhost:7777/block/get")
        time.sleep(2)
        second_len = len(self.node_0.our_messages)

        self.assertNotEqual(first_len, second_len)

        self.assertEqual(self.node_0.our_messages[-1]["action"],
                         "sendmefullblock")

        t_mode_settings(temp_settings["test_mode"])

    def test_block_get_page(self):

        backup_1 = copy.copy(naruno.api.main.custom_TEMP_BLOCK_PATH)
        backup_2 = copy.copy(
            naruno.api.main.custom_TEMP_ACCOUNTS_PATH)
        backup_3 = copy.copy(
            naruno.api.main.custom_TEMP_BLOCKSHASH_PATH)
        backup_4 = copy.copy(
            naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH)

        naruno.api.main.custom_TEMP_BLOCK_PATH = self.node_0.TEMP_BLOCK_PATH
        naruno.api.main.custom_TEMP_ACCOUNTS_PATH = (
            self.node_0.TEMP_ACCOUNTS_PATH)
        naruno.api.main.custom_TEMP_BLOCKSHASH_PATH = (
            self.node_0.TEMP_BLOCKSHASH_PATH)
        naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = (
            self.node_0.TEMP_BLOCKSHASH_PART_PATH)

        temp_settings = the_settings()
        t_mode_settings(True)

        response = urllib.request.urlopen("http://localhost:7777/block/get")
        time.sleep(2)

        self.assertTrue(os.path.exists("test_block_get_page_off_test.txt"))
        os.remove("test_block_get_page_off_test.txt")

        t_mode_settings(temp_settings["test_mode"])
        naruno.api.main.custom_consensus_trigger_result.cancel()

        naruno.api.main.custom_TEMP_BLOCK_PATH = backup_1
        naruno.api.main.custom_TEMP_ACCOUNTS_PATH = backup_2
        naruno.api.main.custom_TEMP_BLOCKSHASH_PATH = backup_3
        naruno.api.main.custom_TEMP_BLOCKSHASH_PART_PATH = backup_4

        self.assertEqual(self.node_0.our_messages[-1]["action"], "fullblock")
        self.assertEqual(self.node_0.our_messages[-1]["byte"], "end")

    def test_export_the_transactions(self):
        custom_MY_TRANSACTION_EXPORT_PATH = MY_TRANSACTION_EXPORT_PATH.replace(
            "my_transaction", "test_export_the_transactions")
        the_transaction_json = {
            "sequence_number": 1,
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
        custom_transactions = [[the_transaction, "validated", "not_sended"]]
        naruno.api.main.custom_transactions = custom_transactions
        naruno.api.main.custom_MY_TRANSACTION_EXPORT_PATH = (
            custom_MY_TRANSACTION_EXPORT_PATH)
        response = urllib.request.urlopen(
            "http://localhost:7777/export/transactions/csv")
        # read the file and check the content
        with open(custom_MY_TRANSACTION_EXPORT_PATH, "r") as f:
            content = f.read()
            expected_content = """sequence_number,signature,fromUser,toUser,data,amount,transaction_fee,transaction_time,validated,sended
1,MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=,MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==,onur,blockchain-lab,5000.0,0.02,1656764224,validated,not_sended
"""
            self.assertEqual(content, expected_content)

    def test_status_page(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_new_block.sequence_number += 1
        custom_connections = self.node_0.clients
        the_transaction_json = {
            "sequence_number": 1,
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        naruno.api.main.custom_first_block = custom_first_block
        naruno.api.main.custom_new_block = custom_new_block
        naruno.api.main.custom_connections = custom_connections
        naruno.api.main.custom_transactions = custom_transactions
        result = urllib.request.urlopen("http://localhost:7777/status")
        result = json.loads(result.read().decode("utf-8"))
        self.assertEqual(result["status"], "Working")
        self.assertEqual(result["last_transaction_of_block"],
                         str(the_transaction.dump_json()))
        self.assertEqual(
            result["transactions_of_us"],
            str([
                f"{str(i[0].__dict__)} | {str(i[1])}"
                for i in custom_transactions
            ]),
        )

    def test_404_page(self):
        response = requests.get("http://localhost:7777/404")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, '"404"\n')

    def test_405_page(self):
        response = requests.post("http://localhost:7777/status",
                                 data={"data": "test"})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.text, '"405"\n')

    def test_500_page(self):
        response = requests.post("http://localhost:7777/send/",
                                 data={"data": "test"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.text, '"500"\n')

    def test_transaction_sended_validated_page(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "cf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "cff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "c", "", "", {"data": "dadata"}, 1, 1,
                                      1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        response = urllib.request.urlopen(
            "http://localhost:7777/transactions/sended/validated")

        result = response.read()

        result = json.loads(result)

        self.assertEqual(
            result["0"]["transaction"]["data"],
            "{'data': 'dadata'}",
        )

        self.assertEqual(
            str(result),
            """{'0': {'sended': True, 'transaction': {'amount': 1.0, 'data': "{'data': 'dadata'}", 'fromUser': '', 'sequence_number': 1, 'signature': 'c', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': True}}""",
        )

        SaveMyTransaction(backup, clear=True)

    def test_transaction_sended_not_validated_page(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "df", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "dff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "c", "", "", {"data": "dadata"}, 1, 1,
                                      1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        response = urllib.request.urlopen(
            "http://localhost:7777/transactions/sended/not_validated")

        result = response.read()

        result = json.loads(result)

        self.assertEqual(
            result["0"]["transaction"]["data"],
            "{'data': 'dadata'}",
        )

        self.assertEqual(
            str(result),
            """{'0': {'sended': True, 'transaction': {'amount': 1.0, 'data': "{'data': 'dadata'}", 'fromUser': '', 'sequence_number': 1, 'signature': 'c', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': False}}""",
        )

        SaveMyTransaction(backup, clear=True)

    def test_transaction_received_page(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "ff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "fff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "c", "", "", {"data": "dadata"}, 1, 1,
                                      1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        response = urllib.request.urlopen(
            "http://localhost:7777/transactions/received")

        result = response.read()

        result = json.loads(result)

        self.assertEqual(
            result["1"]["transaction"]["data"],
            "{'data': 'dadata'}",
        )

        self.assertEqual(
            str(result),
            """{'0': {'sended': False, 'transaction': {'amount': 1.0, 'data': '', 'fromUser': '', 'sequence_number': 1, 'signature': 'fff', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': False}, '1': {'sended': False, 'transaction': {'amount': 1.0, 'data': "{'data': 'dadata'}", 'fromUser': '', 'sequence_number': 1, 'signature': 'c', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': True}}""",
        )

        SaveMyTransaction(backup, clear=True)

    def test_transaction_all_page(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "gf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "gff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "c", "", "", {"data": "dadata"}, 1, 1,
                                      1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        response = urllib.request.urlopen(
            "http://localhost:7777/transactions/all")

        result = response.read()

        result = json.loads(result)

        self.assertEqual(
            result["0"]["transaction"]["data"],
            "",
        )

        self.assertEqual(
            result["1"]["transaction"]["data"],
            "",
        )

        self.assertEqual(
            result["2"]["transaction"]["data"],
            "{'data': 'dadata'}",
        )

        self.assertEqual(
            str(result),
            """{'0': {'sended': True, 'transaction': {'amount': 1.0, 'data': '', 'fromUser': '', 'sequence_number': 1, 'signature': 'gf', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': False}, '1': {'sended': False, 'transaction': {'amount': 1.0, 'data': '', 'fromUser': '', 'sequence_number': 1, 'signature': 'gff', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': True}, '2': {'sended': False, 'transaction': {'amount': 1.0, 'data': "{'data': 'dadata'}", 'fromUser': '', 'sequence_number': 1, 'signature': 'c', 'toUser': '', 'transaction_fee': 1.0, 'transaction_time': 1}, 'validated': False}}""",
        )

        SaveMyTransaction(backup, clear=True)

    def test_GetProof_CheckProof_page(self):

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
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
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
        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "aaa"
        block.validating_list = [the_transaction, the_transaction_2]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=
                               custom_TEMP_BLOCKSHASH_PART_PATH),
            GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True
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
            dont_clean=True
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True
        )
        self.assertIsNot(result_2, False)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash,
             hash_1]).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_1])

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

        request_body = {
            "signature": the_transaction.signature,
            "custom_BLOCKS_PATH": custom_BLOCKS_PATH,
        }
        result = json.loads((requests.post("http://localhost:7777/proof/get/",
                                           data=request_body)).text)

        self.assertIsNotNone(result)

        # Open result zip file
        zip_file = zipfile.ZipFile(result, "r")
        # Extract all files
        zip_file.extractall("db/test_proof_extracted/")
        # Close the zip file
        zip_file.close()

        list_of_files = []
        custom_BLOCKS_PATH_from_proof = None
        for file in os.listdir("db/test_proof_extracted/db/"):
            if os.path.isdir("db/test_proof_extracted/db/" + file):
                custom_BLOCKS_PATH_from_proof = (
                    "db/test_proof_extracted/db/" + file + "/")
                for file_2 in os.listdir("db/test_proof_extracted/db/" + file):

                    list_of_files.append(file_2)

        self.assertIn("0.block.json", list_of_files)
        self.assertIn("0.blockshashpart.json", list_of_files)
        self.assertIn("0.accounts.db", list_of_files)
        self.assertIn("0.blockshash.json", list_of_files)
        self.assertIn("1.blockshash_full.json", list_of_files)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH_from_proof,
            dont_clean=True
        )
        self.assertIsNot(result_2, False)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH_from_proof +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(len(result_2[0].validating_list), 2)
        self.assertEqual(result_2[0].validating_list[0].dump_json(),
                         the_transaction.dump_json())
        self.assertEqual(result_2[0].validating_list[1].dump_json(),
                         the_transaction_2.dump_json())

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_2])
        self.assertEqual(hash_2, hash_1)
        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_2]).getRootHash()

        # Check the_hash_part is in the the_blockshash_part
        is_in = False
        for i in the_blockshash_part:
            if i == the_hash_part:
                is_in = True
        self.assertTrue(is_in)

        request_body = {
            "path": result,
            "custom_TEMP_BLOCKSHASH_PART_PATH":
            custom_TEMP_BLOCKSHASH_PART_PATH,
        }
        result_check_proof = json.loads(
            (requests.post("http://localhost:7777/proof/check/",
                           data=request_body)).text)

        self.assertEqual(
            result_check_proof,
            True,
        )

        SaveMyTransaction(backup, clear=True)

    def test_export_block_json_page(self):
        response = urllib.request.urlopen(
            "http://localhost:7777/export/block/json")
        response_result = json.loads((response.read()).decode("utf-8"))
        retrivied_block = Block.load_json(response_result)
        true_block = naruno.api.main.custom_block

        self.assertEqual(
            retrivied_block.dump_json(),
            true_block.dump_json(),
        )

    def test_sign_verify(self):

        request_body = {
            "data": "Onur Atakan",
            "password": "123",
        }
        request = json.loads(
            requests.post("http://localhost:7777/sign/",
                          data=request_body).text)

        request_body = {
            "path": request,
        }
        response = json.loads(
            requests.post("http://localhost:7777/verify/",
                          data=request_body).text)

        self.assertTrue(response[0])
        self.assertEqual(response[1], "Onur Atakan")
        self.assertEqual(response[2], wallet_import(-1, 3))


    def test_balance_page(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["publisher_mode"] = True
        save_settings(settings)
  

        response = urllib.request.urlopen(
            "http://localhost:7777/balance/get/?address=<addressb>")
        response_result = response.read()
        print(response_result)
        the_balance_int = float(
            (response_result.decode("utf-8")).replace("\n", ""))

        save_settings(backup_the_settings)      

        self.assertEqual(
            the_balance_int,
            0.0,
        )


    def test_sequance_number_page(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["publisher_mode"] = True
        save_settings(settings)
  

        response = urllib.request.urlopen(
            "http://localhost:7777/sequence/get/?address=<address>")
        response_result = response.read()
        print(response_result)
        the_balance_int = int(
            (response_result.decode("utf-8")).replace("\n", ""))

        save_settings(backup_the_settings)      

        self.assertEqual(
            the_balance_int,
            1
        )


unittest.main(exit=False)
