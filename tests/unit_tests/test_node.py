#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest
import copy
import time

from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.node import Node
from decentra_network.node.connection import Connection
from decentra_network.node.unl import Unl



class Test_Node(unittest.TestCase):

    def setUp(self):
        self.node_1 = Node("127.0.0.1", 10001)
        time.sleep(2)
        self.node_2 = Node("127.0.0.1", 10002)

    def tearDown(self):
        self.node_2.stop()
        self.node_2.join()
        self.node_1.stop()
        self.node_1.join()
        Node.connected_node_delete("id5")
        Node.connected_node_delete("id2")

    def reset_node_connections(self):
        for node_1_node in self.node_1.nodes:
            self.node_1.disconnect_to_node(node_1_node)
        self.node_1.delete_closed_connections()
        for node_2_node in self.node_2.nodes:
            self.node_2.disconnect_to_node(node_2_node)
        self.node_2.delete_closed_connections()  
        time.sleep(2)    

    def test_node_by_connection_saving_and_unl_nodes_system(self):

        Node.id = "id"
        Unl.save_new_unl_node(Node.id)
        Node.id = "id2"
        Unl.save_new_unl_node(Node.id )
        time.sleep(2)
        self.node_2.connect_to_node("127.0.0.1", 10001)
        time.sleep(2)
        connection_closing_deleting = True
        finded_node = False
        in_unl_list = False
        get_as_node = False

        nodes_list = Node.get_connected_node()
        print(nodes_list)
        for element in nodes_list:
            print(element)
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
                                    or self.node_2 == node_element_of_unl.host):
                                if (self.node_1.port == node_element_of_unl.port
                                        or self.node_2 == node_element_of_unl.port):
                                    get_as_node = True
                        in_unl_list = True
                        Unl.unl_node_delete(unl_element)
                Node.connected_node_delete(element)





        self.reset_node_connections()
        connection_closing_deleting = any(element.id == Node.id for element in self.node_2.nodes)

        self.assertEqual(connection_closing_deleting, False,
                        "Connection closing deleting")
        self.assertEqual(finded_node, True,
                         "Problem on connection saving system.")
        self.assertEqual(in_unl_list, True,
                         "Problem on UNL node saving system.")
        self.assertEqual(get_as_node, True,
                         "Problem on UNL get as node system.")


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
      

        Unl.save_new_unl_node(self.node_1.id)
        Unl.save_new_unl_node(self.node_2.id)

        self.node_2.connect_to_node("127.0.0.1", 10001, save_messages=True)
        time.sleep(2)
        connection_2 = self.node_1.nodes[0]
        connection_2.save_messages = True

        self.node_2.send_data_to_nodes(1)
        self.node_2.send_data_to_nodes("test")
        time.sleep(2)
        self.node_2.send_data_to_nodes({"test": b'b'})
        self.node_2.send_data_to_nodes({"test": "test"})
        time.sleep(2)
        self.node_2.send_data_to_nodes(b"test")



        self.reset_node_connections()
        self.assertEqual(connection_2.messages[0], "test")
        self.assertEqual(connection_2.messages[1], {"test": "test"})
        self.assertEqual(connection_2.messages[2], "test")

    def test_connection_not_unl(self):

        Node.id = "id3"
        connection = self.node_2.connect_to_node("127.0.0.1", 10001)
        time.sleep(2)

        self.reset_node_connections()
        self.assertEqual(self.node_1.nodes, [])
        self.assertEqual(self.node_2.nodes, [])
        self.assertEqual(connection, None)


    def test_closing_connections_when_node_close(self):
        
        
        Node.id = "id4"
        node_1 = Node("127.0.0.1", 10003)
        time.sleep(2)
        Node.id = "id5"
        node_2 = Node("127.0.0.1", 10004)

        Unl.save_new_unl_node(node_1.id)
        Unl.save_new_unl_node(node_2.id)

        connection = node_2.connect_to_node("127.0.0.1", 10003, save_messages=True)
        time.sleep(2)


        node_1.stop()
        node_1.join()
        node_2.stop()
        node_2.join()
        time.sleep(2)
        self.assertEqual(connection.terminate_flag.is_set(), True)


unittest.main(exit=False)
