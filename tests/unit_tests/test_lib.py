#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import time

from decentra_network.blockchain.block.block_main import Block

from decentra_network.lib.status import Status
from decentra_network.transactions.transaction import Transaction

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest
from unittest import mock

from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.mix.mixlib import (banner_maker, ended_text_centered,
                                             menu_maker, menu_seperator,
                                             menu_space, menu_title,
                                             printcentertext, question_maker,
                                             quit_menu_maker,
                                             starting_text_centered)

from decentra_network.config import (
    CONNECTED_NODES_PATH, LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH, LOADING_BLOCKSHASH_PATH,
    PENDING_TRANSACTIONS_PATH, TEMP_ACCOUNTS_PATH, TEMP_BLOCK_PATH,
    TEMP_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PATH, UNL_NODES_PATH)
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl


class Test_Lib(unittest.TestCase):

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

    def test_starting_text_centered(self):
        self.assertEqual(starting_text_centered(), "\nSTARTING\n")

    def test_ended_text_centered(self):
        self.assertEqual(ended_text_centered(), "\nENDED\n")

    def test_printcentertext(self):
        self.assertEqual(printcentertext("text"), "\ntext\n")

    def test_banner_maker(self):
        sc_name = "sc_name"
        description = "sc_version"
        author = "sc_description"

        self.assertEqual(
            banner_maker(sc_name, description, author),
            (((((f"""Script Name    : {sc_name}""" + """\n""" +
                 """Description    : """) + description) + """\n""") +
              """Author         : """) + author) + """\n""",
        )

    def test_menu_maker(self):
        menu_number = 1
        menu_text = "menu_text"
        self.assertEqual(
            menu_maker(menu_number, menu_text),
            f"{str(menu_number)}) {menu_text}" + "\n",
        )

    def test_quit_menu_maker_main(self):
        self.assertEqual(quit_menu_maker("main"), "\n0) Quit \n")

    def test_quit_menu_maker_sub(self):
        self.assertEqual(quit_menu_maker("sub"), "\n0) Quit sub menu \n")

    def test_quit_menu_maker_other(self):
        self.assertEqual(quit_menu_maker("maina"), "\n0) Quit \n")

    def test_menu_space(self):
        self.assertEqual(menu_space(), "\n")

    def test_menu_seperator(self):
        self.assertEqual(menu_seperator(), "\n*** \n\n")

    def test_menu_title(self):
        self.assertEqual(menu_title("title"), "\n*** title *** \n\n")

    def test_question_maker_custom_Text(self):
        question_text = "question_text"
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(question_text), 1)

    def test_question_maker_main(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="main"), 1)

    def test_question_maker_sub(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="sub"), 1)

    def test_question_maker_anykeytocontinue(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="anykeytocontinue"), 1)

    def test_question_maker_other(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="maina"), 1)

    def test_status_not_working(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_connections = self.node_0.clients
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Not working")
        self.assertEqual(result["last_transaction_of_block"], str(
            the_transaction.dump_json()))
        self.assertEqual(result["transactions_of_us"], str(
            [f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]
        ))
        self.assertEqual(result["connected_nodes"], [
                         '127.0.0.1:10001', '127.0.0.1:10002'])

    def test_status_empty(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_new_block.empty_block_number += 1
        custom_connections = self.node_0.clients
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Working")
        self.assertEqual(result["last_transaction_of_block"], str(
            the_transaction.dump_json()))
        self.assertEqual(result["transactions_of_us"], str(
            [f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]
        ))
        self.assertEqual(result["connected_nodes"], [
                         '127.0.0.1:10001', '127.0.0.1:10002'])

    def test_status(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_new_block.sequance_number += 1
        custom_connections = self.node_0.clients
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Working")
        self.assertEqual(result["last_transaction_of_block"], str(
            the_transaction.dump_json()))
        self.assertEqual(result["transactions_of_us"], str(
            [f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]
        ))
        self.assertEqual(result["connected_nodes"], [
                         '127.0.0.1:10001', '127.0.0.1:10002'])


unittest.main(exit=False)
