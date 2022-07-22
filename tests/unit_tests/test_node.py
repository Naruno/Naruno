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
import json
import time
import unittest

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import (CONNECTED_NODES_PATH,
                                     LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
                                     LOADING_BLOCKSHASH_PART_PATH,
                                     LOADING_BLOCKSHASH_PATH,
                                     TEMP_ACCOUNTS_PATH, TEMP_BLOCK_PATH,
                                     TEMP_BLOCKSHASH_PART_PATH,
                                     TEMP_BLOCKSHASH_PATH)
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.config_system import get_config
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl


class Test_Node(unittest.TestCase):
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
            ".json", "_0.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH1 = TEMP_ACCOUNTS_PATH.replace(
            ".json", "_1.json"
        ).replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH2 = TEMP_ACCOUNTS_PATH.replace(
            ".json", "_2.json"
        ).replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH0 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_0.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH1 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_1.json"
        ).replace("loading_", "test_loading_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH2 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_2.json"
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

    def test_multiple_connection_from_same_server(self):
        first_len_clients_0 = len(self.node_0.clients)
        first_len_clients_1 = len(self.node_1.clients)
        first_len_clients_2 = len(self.node_2.clients)
        self.node_0.connect("127.0.0.1", 10001)
        time.sleep(15)
        self.assertEqual(len(self.node_0.clients), first_len_clients_0)
        self.assertEqual(len(self.node_1.clients), first_len_clients_1)
        self.assertEqual(len(self.node_2.clients), first_len_clients_2)

    def test_false_message_type_not_id(self):
        first_message_len = len(self.node_1.messages)
        data = {"signature": "true"}
        self.node_0.send_client(self.node_0.clients[0], data, ready_to_send=True)
        time.sleep(2)
        self.assertEqual(len(self.node_1.messages), first_message_len)

    def test_false_message_type_not_signature(self):
        first_message_len = len(self.node_1.messages)
        data = {"id": "true"}
        self.node_0.send_client(self.node_0.clients[0], data, ready_to_send=True)
        time.sleep(2)
        self.assertEqual(len(self.node_1.messages), first_message_len)

    def test_node_by_connection_saving_and_unl_nodes_system(self):

        connection_closing_deleting = True
        finded_node = False
        in_unl_list = False
        get_as_node = False

        nodes_list = server.get_connected_nodes(
            custom_CONNECTED_NODES_PATH=self.custom_CONNECTED_NODES_PATH2
        )
        for element in nodes_list:
            if element == self.node_1.host + str(self.node_1.port) + self.node_1.id:
                finded_node = True

                temp_unl_node_list = Unl.get_unl_nodes()
                temp_get_as_node_type = Unl.get_as_node_type(temp_unl_node_list)
                for unl_element in temp_unl_node_list:
                    if unl_element == self.node_1.id or unl_element == self.node_2.id:
                        for node_element_of_unl in temp_get_as_node_type:
                            if (
                                self.node_1.host == node_element_of_unl.host
                                and self.node_1.port == node_element_of_unl.port
                            ):
                                get_as_node = True
                        in_unl_list = True
                        Unl.unl_node_delete(unl_element)

        self.assertEqual(finded_node, True, "Problem on connection saving system.")
        self.assertEqual(in_unl_list, True, "Problem on UNL node saving system.")
        self.assertEqual(get_as_node, True, "Problem on UNL get as node system.")

    def test_GetCandidateBlocks(self):
        client_1 = self.node_2.clients[1]
        client_2 = self.node_2.clients[0]
        value_1 = {
            "action": "myblock",
            "transaction": [],
            "sequance_number": 0,
            "id": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEExVJT06DcQ5LoxjXcj2bXrqwWbJoz+/zoSH9drpQ71i/BjjqnUg/E9k7qkUy/+QK3AENc1Gx+eBQ91Y7xlfG7w==",
            "signature": "MEUCIQDw33eHJvpfmShxv+CPYNnVa1XAg216teeHrsql78B6EwIgHk2JFQ/+JeqTO70yLFK8wYyxIN5qmvPOy+mdlbqNCuk=",
        }
        client_2.candidate_block = value_1
        client_2.candidate_block_hash = value_1
        client_1.candidate_block = value_1
        client_1.candidate_block_hash = value_1
        result = GetCandidateBlocks()
        self.assertEqual(result.candidate_blocks, [value_1])
        self.assertEqual(result.candidate_block_hashes, [value_1])

    def test_send_data_all(self):
        result = self.node_2.send({"action": "test"})
        time.sleep(2)

        self.assertEqual(self.node_0.messages[0], result)
        self.assertEqual(self.node_1.messages[0], result)

    def test_send_full_chain_get_full_chain(self):
        CleanUp_tests()
        the_block = Block("onur")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0.replace(
                ".json", "1.json"
            ),
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "1.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "1.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_chain(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCK_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCK_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH2))

        got_block = GetBlock(custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1)
        got_block.newly = False

        print(the_block.dump_json())
        print(got_block.dump_json())

        self.assertEqual(
            the_block.dump_json(),
            got_block.dump_json(),
        )

    def test_send_full_accounts_get_full_accounts(self):
        CleanUp_tests()
        the_block = Block("atakan123321")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "2.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "2.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_accounts(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH2))

        got_block = GetAccounts(
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1
        )

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block[0].dump_json(),
            {"address": "atakan123321", "balance": 1000000000, "sequence_number": 0},
        )

    def test_send_full_blockshash_get_full_blockshash(self):
        CleanUp_tests()
        the_block = Block("atakan123321222")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_LOADING_BLOCKSHASH_PART_PATH0.replace(
                ".json", "3.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block,
            [the_block.previous_hash],
        )

    def test_send_full_blockshash_part_get_full_blockshash_part(self):
        CleanUp_tests()
        the_block = Block("atakan12332122212321")
        the_block.consensus_timer = 0

        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0,
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash_part(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PART_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 0)
        self.assertEqual(
            got_block,
            [],
        )

    def test_send_full_chain_get_full_chain_already_block(self):
        CleanUp_tests()
        the_block = Block("onur1321313213123")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0.replace(
                ".json", "4.json"
            ),
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "4.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "4.json"
            ),
        )
        the_block.dowload_true_block = server.id
        the_block.first_time = True
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1.replace(
                ".json", "4.json"
            ),
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1.replace(
                ".json", "4.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1.replace(
                ".json", "4.json"
            ),
        )
        the_block.dowload_true_block = ""
        client = self.node_0.clients[0]
        self.node_0.send_full_chain(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCK_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCK_PATH2))
        print("\n\n\n")
        print(self.custom_LOADING_BLOCK_PATH0)
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH2))

        got_block = GetBlock(custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1)
        got_block.newly = False

        print(the_block.dump_json())
        print(got_block.dump_json())

        self.assertEqual(
            the_block.dump_json(),
            got_block.dump_json(),
        )

    def test_send_full_accounts_get_full_accounts_already_block(self):
        CleanUp_tests()
        the_block = Block("atakan123321")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "7.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "7.json"
            ),
        )
        the_block.dowload_true_block = server.id
        the_block.first_time = True
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1.replace(
                ".json", "7.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1.replace(
                ".json", "7.json"
            ),
        )
        the_block.dowload_true_block = ""
        client = self.node_0.clients[0]
        self.node_0.send_full_accounts(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH2))

        got_block = GetAccounts(
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1
        )

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block[0].dump_json(),
            {"address": "atakan123321", "balance": 1000000000, "sequence_number": 0},
        )

    def test_send_full_blockshash_get_full_blockshash_already_block(self):
        CleanUp_tests()
        the_block = Block("atakan123321222")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_LOADING_BLOCKSHASH_PART_PATH0.replace(
                ".json", "8.json"
            ),
        )
        the_block.dowload_true_block = server.id
        the_block.first_time = True
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_LOADING_BLOCKSHASH_PART_PATH1.replace(
                ".json", "8.json"
            ),
        )
        the_block.dowload_true_block = ""
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block,
            [the_block.previous_hash],
        )

    def test_send_full_blockshash_part_get_full_blockshash_part_already_block(self):
        CleanUp_tests()
        the_block = Block("atakan12332122212321")
        the_block.consensus_timer = 0

        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0,
        )
        the_block.dowload_true_block = server.id
        the_block.first_time = True
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH1,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH1,
        )
        the_block.dowload_true_block = ""
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash_part(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH2))

        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PART_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 0)
        self.assertEqual(
            got_block,
            [],
        )

    def test_send_full_chain_get_full_chain_all_nodes(self):
        CleanUp_tests()
        the_block = Block("onur")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0.replace(
                ".json", "1.json"
            ),
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "1.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "1.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_chain()
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCK_PATH1))

        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCK_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH2))

        got_block = GetBlock(custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1)
        got_block.newly = False

        print(the_block.dump_json())
        print(got_block.dump_json())

        self.assertEqual(
            the_block.dump_json(),
            got_block.dump_json(),
        )

    def test_send_full_accounts_get_full_accounts_all_nodes(self):
        CleanUp_tests()
        the_block = Block("atakan123321")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0.replace(
                ".json", "2.json"
            ),
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0.replace(
                ".json", "2.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_accounts()
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH1))

        self.assertTrue(os.path.isfile(self.custom_TEMP_ACCOUNTS_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_ACCOUNTS_PATH2))

        got_block = GetAccounts(
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1
        )

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block[0].dump_json(),
            {"address": "atakan123321", "balance": 1000000000, "sequence_number": 0},
        )

    def test_send_full_blockshash_get_full_blockshash_all_nodes(self):
        CleanUp_tests()
        the_block = Block("atakan123321222")
        the_block.consensus_timer = 0
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_LOADING_BLOCKSHASH_PART_PATH0.replace(
                ".json", "3.json"
            ),
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash()
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH1))

        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block,
            [the_block.previous_hash],
        )

    def test_send_full_blockshash_part_get_full_blockshash_part_all_nodes(self):
        CleanUp_tests()
        the_block = Block("atakan12332122212321")
        the_block.consensus_timer = 0

        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=self.custom_TEMP_BLOCKSHASH_PART_PATH0,
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_blockshash_part()
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH1))

        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCKSHASH_PART_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCKSHASH_PART_PATH2))

        # Read custom_TEMP_BLOCKSHASH_PATH1 file
        with open(self.custom_TEMP_BLOCKSHASH_PART_PATH1, "r") as f:
            got_block = json.load(f)

        self.assertEqual(len(got_block), 0)
        self.assertEqual(
            got_block,
            [],
        )

    def test_connection_timeout_client_side(self):
        first_len_of_clients = len(self.node_0.clients)
        temp_server = server("127.0.0.1", 10058, test=True)
        self.node_0.connect("127.0.0.1", 10058)
        time.sleep(10)
        temp_server.sock.close()
        self.assertEqual(len(self.node_0.clients), first_len_of_clients)

    def test_connectionfrommixdb(self):
        temp_node = server("127.0.0.1", 10058)
        server.connectionfrommixdb(
            custom_server=temp_node,
            custom_CONNECTED_NODES_PATH=self.node_0.CONNECTED_NODES_PATH,
        )
        time.sleep(2)
        self.assertEqual(len(self.node_0.clients), 2)
        self.assertEqual(len(temp_node.clients), 2)
        self.assertEqual(len(self.node_1.clients), 3)
        self.assertEqual(len(self.node_2.clients), 3)
        temp_node.stop()
        time.sleep(2)
        temp_node.join()

    def test_connected_node_delete_and_save(self):
        self.node_0.save_connected_node("test", 58, "onur")
        node = {}
        node["host"] = "test"
        node["port"] = 58
        node["id"] = "onur"
        the_list_before_delete = server.get_connected_nodes(
            custom_CONNECTED_NODES_PATH=self.node_0.CONNECTED_NODES_PATH
        )
        self.node_0.connected_node_delete(node)
        the_list_after_delete = server.get_connected_nodes(
            custom_CONNECTED_NODES_PATH=self.node_0.CONNECTED_NODES_PATH
        )
        result = False
        for i in the_list_after_delete:
            if (
                the_list_after_delete[i]["host"] == "test"
                and the_list_after_delete[i]["port"] == 58
                and the_list_after_delete[i]["id"] == "onur"
            ):
                result = True
        self.assertNotEqual(len(the_list_before_delete), len(the_list_after_delete))
        self.assertFalse(result)


unittest.main(exit=False)
