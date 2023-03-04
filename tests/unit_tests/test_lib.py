#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import sys
import time


sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest
from unittest import mock

from naruno.blockchain.block.block_main import Block
from naruno.config import (
    CONNECTED_NODES_PATH,
    LOADING_ACCOUNTS_PATH,
    LOADING_BLOCK_PATH,
    LOADING_BLOCKSHASH_PART_PATH,
    LOADING_BLOCKSHASH_PATH,
    MY_TRANSACTION_EXPORT_PATH,
    PENDING_TRANSACTIONS_PATH,
    TEMP_ACCOUNTS_PATH,
    TEMP_BLOCK_PATH,
    TEMP_BLOCKSHASH_PART_PATH,
    TEMP_BLOCKSHASH_PATH,
    UNL_NODES_PATH,
)
from naruno.lib.backup.naruno_export import naruno_export
from naruno.lib.backup.naruno_import import naruno_import
from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.config_system import get_config
from naruno.lib.export import export_the_transactions
from naruno.lib.mix.mixlib import (
    banner_maker,
    ended_text_centered,
    menu_maker,
    menu_seperator,
    menu_space,
    menu_title,
    printcentertext,
    question_maker,
    quit_menu_maker,
    starting_text_centered,
)
from naruno.lib.notification import notification
from naruno.lib.performance_analyzers.heartbeat_db import heartbeat_generic_db_analyzer
from naruno.lib.perpetualtimer import perpetualTimer
from naruno.lib.safety import safety_check
from naruno.lib.settings_system import (
    d_mode_settings,
    dark_mode_settings,
    publisher_mode_settings,
    mt_settings,
    save_settings,
    t_mode_settings,
    the_settings,
)
from naruno.lib.status import Status
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.transaction import Transaction

from naruno.lib.sign import sign
from naruno.lib.verify import verify

from naruno.wallet.wallet_import import Address, wallet_import


def perpetual_time_test():
    os.chdir(get_config()["main_folder"])
    with open("test_perpetual_time_test.txt", "a") as f:
        f.write("Hello World")


class pywall_none:
    def __init__(self):
        self.iface = "eth0"
        self.timeout = 10

    def control(self):
        return None


class pywall_true:
    def __init__(self):
        self.iface = "eth0"
        self.timeout = 10

    def control(self):
        return True


class pywall_false:
    def __init__(self):
        self.iface = "eth0"
        self.timeout = 10

    def control(self):
        return False


class Test_Lib(unittest.TestCase):
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
            (
                (
                    (
                        (
                            (
                                f"""Script Name    : {sc_name}"""
                                + """\n"""
                                + """Description    : """
                            )
                            + description
                        )
                        + """\n"""
                    )
                    + """Author         : """
                )
                + author
            )
            + """\n""",
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Not working")
        self.assertEqual(
            result["last_transaction_of_block"], str(the_transaction.dump_json())
        )
        self.assertEqual(
            result["transactions_of_us"],
            str([f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]),
        )
        self.assertEqual(
            result["connected_nodes"], ["127.0.0.1:10001", "127.0.0.1:10002"]
        )

    def test_status_empty(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_new_block.empty_block_number += 1
        custom_connections = self.node_0.clients
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Working")
        self.assertEqual(
            result["last_transaction_of_block"], str(the_transaction.dump_json())
        )
        self.assertEqual(
            result["transactions_of_us"],
            str([f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]),
        )
        self.assertEqual(
            result["connected_nodes"], ["127.0.0.1:10001", "127.0.0.1:10002"]
        )

    def test_status(self):
        custom_first_block = Block("Onur")
        custom_new_block = Block("Onur")
        custom_new_block.sequence_number += 1
        custom_connections = self.node_0.clients
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
        custom_transactions = [[the_transaction, "validated"]]
        custom_new_block.validating_list = [the_transaction]
        result = Status(
            custom_first_block=custom_first_block,
            custom_new_block=custom_new_block,
            custom_connections=custom_connections,
            custom_transactions=custom_transactions,
        )
        self.assertEqual(result["status"], "Working")
        self.assertEqual(
            result["last_transaction_of_block"], str(the_transaction.dump_json())
        )
        self.assertEqual(
            result["transactions_of_us"],
            str([f"{str(i[0].__dict__)} | {str(i[1])}" for i in custom_transactions]),
        )
        self.assertEqual(
            result["connected_nodes"], ["127.0.0.1:10001", "127.0.0.1:10002"]
        )

    def test_export_the_transactions_false(self):
        custom_MY_TRANSACTION_EXPORT_PATH = MY_TRANSACTION_EXPORT_PATH.replace(
            "my_transaction", "test_my_transaction_false"
        )
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
        custom_transactions = []
        result = export_the_transactions(
            custom_transactions=custom_transactions,
            custom_MY_TRANSACTION_EXPORT_PATH=custom_MY_TRANSACTION_EXPORT_PATH,
        )
        self.assertFalse(result)
        self.assertFalse(os.path.exists(custom_MY_TRANSACTION_EXPORT_PATH))

    def test_export_the_transactions(self):
        custom_MY_TRANSACTION_EXPORT_PATH = MY_TRANSACTION_EXPORT_PATH.replace(
            "my_transaction", "test_my_transaction"
        )
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
        custom_transactions = [[the_transaction, "validated", "not_sended"]]
        result = export_the_transactions(
            custom_transactions=custom_transactions,
            custom_MY_TRANSACTION_EXPORT_PATH=custom_MY_TRANSACTION_EXPORT_PATH,
        )
        self.assertTrue(result)
        # read the file and check the content
        with open(custom_MY_TRANSACTION_EXPORT_PATH, "r") as f:
            content = f.read()
            expected_content = """sequence_number,signature,fromUser,toUser,data,amount,transaction_fee,transaction_time,validated,sended
1,MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=,MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==,onur,blockchain-lab,5000.0,0.02,1656764224,validated,not_sended
"""
            self.assertEqual(content, expected_content)

    def test_safety_check_no_module(self):
        result = safety_check()
        self.assertIsNone(result)

    def test_safety_check_none_false(self):
        result = safety_check(
            custom_pywall=pywall_none,
            custom_debug_mode=False,
            exit_on_error=False,
        )
        self.assertFalse(result)

    def test_safety_check_none_true(self):
        result = safety_check(
            custom_pywall=pywall_none,
            custom_debug_mode=True,
            exit_on_error=False,
        )
        self.assertIsNone(result)

    def test_safety_check_true(self):
        result = safety_check(
            custom_pywall=pywall_true,
            exit_on_error=False,
        )
        self.assertFalse(result)

    def test_safety_check_false(self):
        result = safety_check(
            custom_pywall=pywall_false,
            exit_on_error=False,
        )
        self.assertTrue(result)

    def test_settings_by_creating_settings(self):
        temp_settings = the_settings()
        self.assertIsNotNone(temp_settings["test_mode"], "A problem on the test_mode.")
        self.assertIsNotNone(
            temp_settings["debug_mode"], "A problem on the debug_mode."
        )

    def test_settings_by_saving_and_getting_new_settings(self):
        backup_settings = the_settings()

        temp_settings = the_settings()

        temp_settings["test_mode"] = True
        temp_settings["debug_mode"] = True
        save_settings(temp_settings)

        temp_test_settings = the_settings()
        self.assertEqual(
            temp_test_settings["test_mode"],
            True,
            "A problem on the saving the settings.",
        )
        self.assertEqual(
            temp_test_settings["debug_mode"],
            True,
            "A problem on the saving the settings.",
        )

        temp_test_settings["test_mode"] = False
        temp_test_settings["debug_mode"] = False
        save_settings(temp_test_settings)

        temp_test_settings2 = the_settings()
        self.assertEqual(
            temp_test_settings2["test_mode"],
            False,
            "A problem on the saving the settings.",
        )
        self.assertEqual(
            temp_test_settings2["debug_mode"],
            False,
            "A problem on the saving the settings.",
        )

        temp_test_settings2["test_mode"] = backup_settings["test_mode"]
        temp_test_settings2["debug_mode"] = backup_settings["debug_mode"]
        save_settings(temp_test_settings2)

    def test_t_mode_settings(self):
        temp_settings = the_settings()
        changed_value = True if temp_settings["test_mode"] is False else False
        t_mode_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["test_mode"], changed_value)

        t_mode_settings(temp_settings["test_mode"])

    def test_d_mode_settings(self):
        temp_settings = the_settings()
        changed_value = True if temp_settings["debug_mode"] is False else False
        d_mode_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["debug_mode"], changed_value)

        t_mode_settings(temp_settings["debug_mode"])

    def test_mt_settings(self):
        temp_settings = the_settings()
        changed_value = True if temp_settings["mute_notifications"] is False else False
        mt_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["mute_notifications"], changed_value)

        mt_settings(temp_settings["mute_notifications"])

    def test_dark_mode_settings(self):
        temp_settings = the_settings()
        changed_value = True if temp_settings["dark_mode"] is False else False
        dark_mode_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["dark_mode"], changed_value)

        dark_mode_settings(temp_settings["dark_mode"])

    def test_publisher_mode_settings(self):
        temp_settings = the_settings()
        changed_value = True if temp_settings["publisher_mode"] is False else False
        publisher_mode_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["publisher_mode"], changed_value)

        publisher_mode_settings(temp_settings["publisher_mode"])

    def test_perpetualTimer_0(self):
        the_timer = perpetualTimer(
            0,
            perpetual_time_test,
        )
        time.sleep(2.5)
        self.assertFalse(os.path.exists("test_perpetual_time_test.txt"))
        the_timer.cancel()

    def test_perpetualTimer(self):
        the_timer = perpetualTimer(
            1,
            perpetual_time_test,
        )
        time.sleep(3.5)
        self.assertTrue(os.path.exists("test_perpetual_time_test.txt"))
        # open and read the file after the 2.5 seconds
        with open("test_perpetual_time_test.txt", "r") as f:
            content = f.read()
        self.assertEqual(len(content), 33)
        the_timer.cancel()
        os.remove("test_perpetual_time_test.txt")

    def test_heartbeat_db_analyzer(self):
        block = Block("Onur")
        result = heartbeat_generic_db_analyzer()
        self.assertLess(
            result[0][0] + result[0][1],
            ((block.round_1_time - 2) + block.hard_block_number * block.block_time),
        )
        self.assertLess(result[0][2], 120)
        self.assertLess(result[1][0] + result[1][1], block.round_1_time - 2)

    def test_notification_not(self):
        notification("test", "trest", raise_plyer=True)

    def test_notification_mt_True(self):
        temp_settings = the_settings()
        changed_value = True
        mt_settings(changed_value)

        self.assertEqual(notification("test", "trest"), False)

        mt_settings(temp_settings["mute_notifications"])

    def test_notification_mt_False(self):
        temp_settings = the_settings()
        changed_value = False
        mt_settings(changed_value)

        self.assertNotEqual(notification("test", "trest"), False)

        mt_settings(temp_settings["mute_notifications"])

    def test_export_import(self):
        """
        Test that the `naruno_export` and `naruno_import` functions work correctly.
        """
        backup = naruno_export()
        temp_settings = the_settings()

        changed_value = True if temp_settings["debug_mode"] is False else False
        d_mode_settings(changed_value)
        new_settings = the_settings()

        self.assertEqual(new_settings["debug_mode"], changed_value)
        naruno_import(backup)
        self.assertNotEqual(the_settings()["debug_mode"], changed_value)

    def test_sign_verify(self):
        signed = sign("Onur & Ali Eren", "123")
        result = verify(signed)
        os.remove(signed)
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Onur & Ali Eren")
        self.assertEqual(result[2], wallet_import(-1, 3))

    def test_sign_verify_no_found(self):
        signed = sign("Onur & Ali Eren", "123")
        result = verify(signed + "123")
        os.remove(signed)
        self.assertFalse(result)

    def test_sign_verify_false_pass(self):
        signed = sign("Onur & Ali Eren", str(time.time()))
        self.assertEqual(signed, "None")


unittest.main(exit=False)
