#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
import unittest
import copy
import time

from node.get_candidate_blocks import GetCandidateBlocks
from node.node import Node
from node.connection import Connection
from node.unl import Unl
from wallet.get_saved_wallet import get_saved_wallet
from wallet.wallet_create import wallet_create
from wallet.wallet_delete import wallet_delete



class Test_Node(unittest.TestCase):

    def test_node_by_connection_saving_and_unl_nodes_system(self):

        password = "123"

        temp_private_key = wallet_create(password)

        node_1 = Node("127.0.0.1", 60001)

        temp_private_key2 = wallet_create(password)

        node_2 = Node("127.0.0.1", 60002)

        Unl.save_new_unl_node(node_1.id)
        Unl.save_new_unl_node(node_2.id)

        connection = node_2.connect_to_node("127.0.0.1", 60001)

        connection_closing_deleting = True
        finded_node = False
        in_unl_list = False
        get_as_node = False

        nodes_list = Node.get_connected_node()

        for element in nodes_list:
            if element == node_1.id or element == node_2.id:
                finded_node = True

                temp_unl_node_list = Unl.get_unl_nodes()
                temp_get_as_node_type = Unl.get_as_node_type(
                    temp_unl_node_list)
                for unl_element in temp_unl_node_list:
                    if unl_element == node_1.id or unl_element == node_2.id:
                        for node_element_of_unl in temp_get_as_node_type:
                            if (node_1.host == node_element_of_unl.host
                                    or node_2 == node_element_of_unl.host):
                                if (node_1.port == node_element_of_unl.port
                                        or node_2 == node_element_of_unl.port):
                                    get_as_node = True
                        in_unl_list = True
                        Unl.unl_node_delete(unl_element)
                Node.connected_node_delete(element)

        for i in node_2.nodes:
            node_2.disconnect_to_node(i)
        node_2.delete_closed_connections()

        for i in node_1.nodes:
            node_1.disconnect_to_node(i)
        node_1.delete_closed_connections()

        connection_closing_deleting = any(element == id for element in nodes_list)

        saved_wallets = get_saved_wallet()

        for each_wallet in saved_wallets:
            if (temp_private_key == saved_wallets[each_wallet]["privatekey"]
                    or temp_private_key2
                    == saved_wallets[each_wallet]["privatekey"]):
                wallet_delete(each_wallet)

        node_2.stop()
        node_1.stop()

        self.assertEqual(connection_closing_deleting, False,
                        "Connection closing deleting")
        self.assertEqual(finded_node, True,
                         "Problem on connection saving system.")
        self.assertEqual(in_unl_list, True,
                         "Problem on UNL node saving system.")
        self.assertEqual(get_as_node, True,
                         "Problem on UNL get as node system.")
        time.sleep(10)

    def test_GetCandidateBlocks(self):

        node_1 = Connection("main_node", "sock", "id", "host", "port")
        node_1.candidate_block = True
        node_1.candidate_block_hash = True
        node_2 = copy.copy(node_1)
        node_2.candidate_block = True
        node_2.candidate_block_hash = False
        nodes_list = [node_1, node_2]

        result = GetCandidateBlocks(nodes_list)
        self.assertEqual(result.candidate_blocks, [True, True])
        self.assertEqual(result.candidate_block_hashes, [True, False])

    def test_parse_packet_unicode(self):
        connection = Connection("main_node", "sock", "id", "host", "port")
        packet = "test"
        packet = packet.encode('utf-16')
        result = connection.parse_packet(packet)
        self.assertEqual(result, b'\xff\xfet\x00e\x00s\x00t\x00')

    def test_parse_packet(self):
        connection = Connection("main_node", "sock", "id", "host", "port")
        packet = "test"
        packet = packet.encode("utf-8")
        result = connection.parse_packet(packet)
        self.assertEqual(result, "test")
        
    def test_send_data_to_nodes(self):
      
        password = "123"

        temp_private_key = wallet_create(password)

        node_1 = Node("127.0.0.1", 60001)

        temp_private_key2 = wallet_create(password)

        node_2 = Node("127.0.0.1", 60002)

        Unl.save_new_unl_node(node_1.id)
        Unl.save_new_unl_node(node_2.id)

        connection = node_2.connect_to_node("127.0.0.1", 60001, save_messages=True)
        time.sleep(2)
        connection_2 = node_1.nodes[0]
        connection_2.save_messages = True

        node_2.send_data_to_nodes(1)
        node_2.send_data_to_nodes("test")
        time.sleep(2)
        node_2.send_data_to_nodes({"test": b'b'})
        node_2.send_data_to_nodes({"test": "test"})
        time.sleep(2)
        node_2.send_data_to_nodes(b"test")


        saved_wallets = get_saved_wallet()

        for each_wallet in saved_wallets:
            if (temp_private_key == saved_wallets[each_wallet]["privatekey"]
                    or temp_private_key2
                    == saved_wallets[each_wallet]["privatekey"]):
                wallet_delete(each_wallet)


        for i in node_2.nodes:
            node_2.disconnect_to_node(i)
        node_2.delete_closed_connections()

        for i in node_1.nodes:
            node_1.disconnect_to_node(i)
        node_1.delete_closed_connections()    
        node_2.stop()
        node_1.stop()
        self.assertEqual(connection_2.messages[0], "test")
        self.assertEqual(connection_2.messages[1], {"test": "test"})
        self.assertEqual(connection_2.messages[2], "test")

    def test_connection_not_unl(self):

        default_id = copy.copy(Node.id)
        Node.id = "id"
        node_1 = Node("127.0.0.1", 60001)
        node_2 = Node("127.0.0.1", 60002)
        connection = node_2.connect_to_node("127.0.0.1", 60001)
        time.sleep(2)



        Node.id = default_id
        for i in node_2.nodes:
            node_2.disconnect_to_node(i)
        node_2.delete_closed_connections()

        for i in node_1.nodes:
            node_1.disconnect_to_node(i)
        node_1.delete_closed_connections()  
        node_2.stop()
        node_1.stop()
        self.assertEqual(node_1.nodes, [])
        self.assertEqual(node_2.nodes, [])
        self.assertEqual(connection, None)
        time.sleep(10)  

unittest.main(exit=False)
