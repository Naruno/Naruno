#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import socket
import sys
import time
import threading
import os
import json

from config import CONNECTED_NODE_PATH

from lib.mixlib import dprint

from node.unl import Unl
from node.node_connection import Node_Connection


class Node(threading.Thread):
    
    def __init__(self, host, port, callback=None):
        super(Node, self).__init__()


        self.terminate_flag = threading.Event()

        self.host = host
        self.port = port


        self.callback = callback


        self.nodes_inbound = []

        self.nodes_outbound = []


        from wallet.wallet import Wallet_Import
        self.id = "".join([
            l.strip() for l in Wallet_Import(0,0).splitlines()
            if l and not l.startswith("-----")
        ])


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()



    def run(self):

        while not self.terminate_flag.is_set():
            try:
                connection, client_address = self.sock.accept()
                
                connected_node_id = connection.recv(4096).decode('utf-8')
                connection.send(self.id.encode('utf-8'))
                if Unl.node_is_unl(connected_node_id):
                    thread_client = self.create_the_new_connection(connection, connected_node_id, client_address[0], client_address[1])
                    thread_client.start()

                    self.nodes_inbound.append(thread_client)
                else:
                    dprint("Node System: Could not connect with node because node is not unl node.")
                
            except socket.timeout:
                pass

            except Exception as e:
                raise e

            time.sleep(0.01)

        print("Node System: Node stopping...")
        for t in self.nodes_inbound:
            t.stop()

        for t in self.nodes_outbound:
            t.stop()

        time.sleep(1)

        for t in self.nodes_inbound:
            t.join()

        for t in self.nodes_outbound:
            t.join()

        self.sock.settimeout(None)   
        self.sock.close()
        print("Node System: Node stopped")



    def init_server(self):
        print("Node System: Initialisation of the Node on port: " + str(self.port) + " on node (" + self.id + ")")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)


    def delete_closed_connections(self):

        for n in self.nodes_inbound:
            if n.terminate_flag.is_set():
                n.join()
                del self.nodes_inbound[self.nodes_inbound.index(n)]

        for n in self.nodes_outbound:
            if n.terminate_flag.is_set():
                n.join()
                del self.nodes_outbound[self.nodes_inbound.index(n)]

    def send_data_to_nodes(self, data, exclude=[]):

        for n in self.nodes_inbound:
            if n in exclude:
                dprint("Node System: Node send_data_to_nodes: Excluding node in sending the message")
            else:
                try:
                    self.send_data_to_node(n, data)
                except: # lgtm [py/catch-base-exception]
                    pass

        for n in self.nodes_outbound:
            if n in exclude:
                dprint("Node System: Node send_data_to_nodes: Excluding node in sending the message")
            else:
                try:
                    self.send_data_to_node(n, data)
                except: # lgtm [py/catch-base-exception]
                    pass

    def send_data_to_node(self, n, data):

        self.delete_closed_connections()
        if n in self.nodes_inbound or n in self.nodes_outbound:
            try:
                n.send(data)

            except Exception as e:
                dprint("Node System: Node send_data_to_node: Error while sending data to the node (" + str(e) + ")")
        else:
            dprint("Node System: Node send_data_to_node: Could not send the data, node is not found!")

    def connect_to_node(self, host, port):

        if host == self.host and port == self.port:
            print("Node System: connect_to_node: Cannot connect with yourself!!")
            return False

        # Check if node is already connected with this node!
        for node in self.nodes_outbound:
            if node.host == host and node.port == port:
                print("Node System: connect_to_node: Already connected with this node.")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dprint("Node System: connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            # Basic information exchange (not secure) of the id's of the nodes!
            sock.send(self.id.encode('utf-8')) # Send my id to the connected node!
            connected_node_id = sock.recv(4096).decode('utf-8') # When a node is connected, it sends it id!

            if Unl.node_is_unl(connected_node_id):
                thread_client = self.create_the_new_connection(sock, connected_node_id, host, port)
                thread_client.start()

                self.nodes_outbound.append(thread_client)
            else:
                dprint("Node System: Could not connect with node because node is not unl node.")
        except Exception as e:
            dprint("Node System: TcpServer.connect_to_node: Could not connect with node. (" + str(e) + ")")
        




    def disconnect_to_node(self, node):

        if node in self.nodes_outbound:
            node.stop()
            node.join()
            del self.nodes_outbound[self.nodes_outbound.index(node)]

        else:
            print("Node System: Node disconnect_to_node: cannot disconnect with a node with which we are not connected.")

    def stop(self):
        self.terminate_flag.set()


    def create_the_new_connection(self, connection, id, host, port):

        return Node_Connection(self, connection, id, host, port)


    @staticmethod
    def get_connected_node():
            """
            Returns the connected nodes.
            """

            sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

            from lib.config_system import get_config

            if not os.path.exists(CONNECTED_NODE_PATH):
                temp_json = {}
                return temp_json


            os.chdir(get_config()["main_folder"])
            with open(CONNECTED_NODE_PATH, 'rb') as connected_node_file:
                return json.load(connected_node_file)

    @staticmethod
    def save_connected_node(host,port,id):
            """
            Saves the connected nodes.
            """

            node_list = Node.get_connected_node()

            already_in_list = False

            for element in node_list:
                if node_list[element]["host"] == host and node_list[element]["port"] == port:
                    already_in_list = True

            if not already_in_list:
                node_list[id] = {}
                node_list[id]["host"] = host
                node_list[id]["port"] = port




                

                sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
                
                from lib.config_system import get_config



                os.chdir(get_config()["main_folder"])
                with open(CONNECTED_NODE_PATH, 'w') as connected_node_file:
                    json.dump(node_list, connected_node_file, indent=4)

    @staticmethod
    def connectionfrommixdb():
        """
        Connects to the mixdb.
        """

        node_list = Node.get_connected_node()
        from node.myownp2pn import mynode
        for element in node_list:
            mynode.main_node.connect_to_node(node_list[element]["host"], node_list[element]["port"])

    @staticmethod
    def connected_node_delete(node):
        """
        Deletes a connected node.
        """

        saved_nodes = Node.get_connected_node()
        if node in saved_nodes:
            del saved_nodes[node]
            from lib.config_system import get_config
        

            os.chdir(get_config()["main_folder"])
            with open(CONNECTED_NODE_PATH, 'w') as connected_node_file:
                json.dump(saved_nodes, connected_node_file, indent=4)


    def message_from_node(self, node, data):
        if self.callback is not None:
            self.callback("message_from_node", self, node, data)
