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
from decentra_network.config import (LOADING_ACCOUNTS_PATH, LOADING_BLOCK_PATH,
                                     LOADING_BLOCKSHASH_PATH,
                                     TEMP_ACCOUNTS_PATH, TEMP_BLOCK_PATH,
                                     TEMP_BLOCKSHASH_PATH)
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.lib.config_system import get_config
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.clean_up import CleanUp_tests
class Test_Node(unittest.TestCase):

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
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCK_PATH1 = LOADING_BLOCK_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCK_PATH2 = LOADING_BLOCK_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")

        cls.custom_TEMP_ACCOUNTS_PATH0 = TEMP_ACCOUNTS_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH1 = TEMP_ACCOUNTS_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_ACCOUNTS_PATH2 = TEMP_ACCOUNTS_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH0 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH1 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_ACCOUNTS_PATH2 = LOADING_ACCOUNTS_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")

        cls.custom_TEMP_BLOCKSHASH_PATH0 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH1 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_TEMP_BLOCKSHASH_PATH2 = TEMP_BLOCKSHASH_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH0 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_0.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH1 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_1.json").replace("temp_", "test_temp_")
        cls.custom_LOADING_BLOCKSHASH_PATH2 = LOADING_BLOCKSHASH_PATH.replace(
            ".json", "_2.json").replace("temp_", "test_temp_")

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
        )
        Unl.save_new_unl_node(cls.node_0.id)
        Unl.save_new_unl_node(cls.node_1.id)
        Unl.save_new_unl_node(cls.node_2.id)
        time.sleep(2)
        cls.node_0.connect("127.0.0.1", 10001)
        time.sleep(15)
        cls.node_0.connect("127.0.0.1", 10002)
        time.sleep(15)
        cls.node_2.connect("127.0.0.1", 10001)
        time.sleep(15)

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

        for a_client in cls.node_0.clients + cls.node_1.clients + cls.node_2.clients:
            the_dict = {}
            the_dict["id"] = a_client.id
            the_dict["host"] = a_client.host
            the_dict["port"] = a_client.port
            server.connected_node_delete(the_dict)




    def test_node_by_connection_saving_and_unl_nodes_system(self):

        connection_closing_deleting = True
        finded_node = False
        in_unl_list = False
        get_as_node = False

        nodes_list = server.get_connected_nodes()
        for element in nodes_list:
            if element == self.node_1.id or element == self.node_2.id:
                finded_node = True

                temp_unl_node_list = Unl.get_unl_nodes()
                temp_get_as_node_type = Unl.get_as_node_type(
                    temp_unl_node_list)
                for unl_element in temp_unl_node_list:
                    if unl_element == self.node_1.id or unl_element == self.node_2.id:
                        for node_element_of_unl in temp_get_as_node_type:
                            if (self.node_1.host == node_element_of_unl.host
                                    and self.node_1.port
                                    == node_element_of_unl.port):
                                get_as_node = True
                        in_unl_list = True
                        Unl.unl_node_delete(unl_element)
                server.connected_node_delete(nodes_list[element])

        self.assertEqual(finded_node, True,
                         "Problem on connection saving system.")
        self.assertEqual(in_unl_list, True,
                         "Problem on UNL node saving system.")
        self.assertEqual(get_as_node, True,
                         "Problem on UNL get as node system.")

    def test_GetCandidateBlocks(self):
        client_1 = self.node_2.clients[1]
        client_2 = self.node_2.clients[0]
        value_1 = {
            "action":
            "myblock",
            "transaction": [],
            "sequance_number":
            0,
            "id":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEExVJT06DcQ5LoxjXcj2bXrqwWbJoz+/zoSH9drpQ71i/BjjqnUg/E9k7qkUy/+QK3AENc1Gx+eBQ91Y7xlfG7w==",
            "signature":
            "MEUCIQDw33eHJvpfmShxv+CPYNnVa1XAg216teeHrsql78B6EwIgHk2JFQ/+JeqTO70yLFK8wYyxIN5qmvPOy+mdlbqNCuk=",
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
        the_block = Block("onur")
        the_block.consensus_timer = 0
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_send_full_chain_get_full_chain_custom_TEMP_ACCOUNTS_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_send_full_chain_get_full_chain_custom_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_send_full_chain_get_full_chain_custom_TEMP_BLOCKSHASH_PART_PATH.json"
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        client = self.node_0.clients[0]
        self.node_0.send_full_chain(client)
        time.sleep(5)
        self.assertTrue(os.path.isfile(self.custom_TEMP_BLOCK_PATH1))

        self.assertFalse(os.path.isfile(self.custom_TEMP_BLOCK_PATH2))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH0))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH1))
        self.assertFalse(os.path.isfile(self.custom_LOADING_BLOCK_PATH2))

        got_block = GetBlock(
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH1)
        got_block.newly = False

        print(the_block.dump_json())
        print(got_block.dump_json())

        self.assertEqual(
            the_block.dump_json(),
            got_block.dump_json(),
        )

    def test_send_full_accounts_get_full_accounts(self):
        the_block = Block("atakan123321")
        the_block.consensus_timer = 0
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_send_full_chain_get_full_chain_custom_TEMP_BLOCKSHASH_PATH.json"
        )
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_send_full_chain_get_full_chain_custom_TEMP_BLOCKSHASH_PART_PATH.json"
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
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
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH1)

        self.assertEqual(len(got_block), 1)
        self.assertEqual(
            got_block[0].dump_json(),
            {
                "address": "atakan123321",
                "balance": 1000000000,
                "sequence_number": 0
            },
        )

    def test_send_full_blockshash_get_full_blockshash(self):
        the_block = Block("atakan123321222")
        the_block.consensus_timer = 0
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_send_full_chain_get_full_chain_custom_TEMP_BLOCKSHASH_PART_PATH.json"
        SaveBlock(
            the_block,
            custom_TEMP_BLOCK_PATH=self.custom_TEMP_BLOCK_PATH0,
            custom_TEMP_ACCOUNTS_PATH=self.custom_TEMP_ACCOUNTS_PATH0,
            custom_TEMP_BLOCKSHASH_PATH=self.custom_TEMP_BLOCKSHASH_PATH0,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
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


unittest.main(exit=False)
