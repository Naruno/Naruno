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

from node.unl import node_is_unl


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


def save_connected_node(host,port,id):
        """
        Saves the connected nodes.
        """

        node_list = get_connected_node()

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




def connectionfrommixdb():
    """
    Connects to the mixdb.
    """

    node_list = get_connected_node()
    from node.myownp2pn import mynode
    for element in node_list:
        mynode.main_node.connect_to_node(node_list[element]["host"], node_list[element]["port"])


def connected_node_delete(node):
    """
    Deletes a connected node.
    """

    saved_nodes = get_connected_node()
    if node in saved_nodes:
        del saved_nodes[node]
        from lib.config_system import get_config
    

        os.chdir(get_config()["main_folder"])
        with open(CONNECTED_NODE_PATH, 'w') as connected_node_file:
            json.dump(saved_nodes, connected_node_file, indent=4)


class Node_Connection(threading.Thread):


    def __init__(self, main_node, sock, id, host, port):


        super(Node_Connection, self).__init__()

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()


        self.id = id

        self.candidate_block = None
        self.candidate_block_hash = None


        self.EOT_CHAR = 0x04.to_bytes(1, 'big')


        self.info = {}

        save_connected_node(host,port,id)

    def send(self, data, encoding_type='utf-8'):

        if isinstance(data, str):
            self.sock.sendall( data.encode(encoding_type) + self.EOT_CHAR )

        elif isinstance(data, dict):
            try:
                json_data = json.dumps(data)
                json_data = json_data.encode(encoding_type) + self.EOT_CHAR
                self.sock.sendall(json_data)

            except TypeError as type_error:
                dprint('Node System: This dict is invalid')
                dprint(type_error)

            except Exception as e:
                print('Node System: Unexpected Error in send message')
                print(e)

        elif isinstance(data, bytes):
            bin_data = data + self.EOT_CHAR
            self.sock.sendall(bin_data)

        else:
            dprint('Node System: Node System: Datatype used is not valid please use str, dict (will be send as json) or bytes')


    def stop(self):
        self.terminate_flag.set()

    def parse_packet(self, packet):
        try:
            packet_decoded = packet.decode('utf-8')

            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                return packet_decoded

        except UnicodeDecodeError:
            return packet

    def run(self):
        self.sock.settimeout(10.0)          
        buffer = b''

        while not self.terminate_flag.is_set():
            chunk = b''

            try:
                chunk = self.sock.recv(4096) 

            except socket.timeout:
                dprint("Node System: Node_Connection: timeout")

            except Exception as e:
                self.terminate_flag.set()
                dprint('Node System: Unexpected error')
                dprint(e)

            # BUG: possible buffer overflow when no EOT_CHAR is found => Fix by max buffer count or so?
            if chunk != b'':
                buffer += chunk
                eot_pos = buffer.find(self.EOT_CHAR)

                while eot_pos > 0:
                    packet = buffer[:eot_pos]
                    buffer = buffer[eot_pos + 1:]

                    self.main_node.message_count_recv += 1
                    self.main_node.message_from_node( self, self.parse_packet(packet) )

                    eot_pos = buffer.find(self.EOT_CHAR)

            time.sleep(0.01)

        # IDEA: Invoke (event) a method in main_node so the user is able to send a bye message to the node before it is closed?

        self.sock.settimeout(None)
        self.sock.close()
        dprint("Node System: Node_Connection: Stopped")

    def set_info(self, key, value):
        self.info[key] = value

    def get_info(self, key):
        return self.info[key]

    def __str__(self):
        return 'Node_Connection: {}:{} <-> {}:{} ({})'.format(self.main_node.host, self.main_node.port, self.host, self.port, self.id)

    def __repr__(self):
        return '<Node_Connection: Node {}:{} <-> Connection {}:{}>'.format(self.main_node.host, self.main_node.port, self.host, self.port)



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


        self.message_count_send = 0
        self.message_count_recv = 0
        self.message_count_rerr = 0


    def init_server(self):
        print("Node System: Initialisation of the Node on port: " + str(self.port) + " on node (" + self.id + ")")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)


    def delete_closed_connections(self):

        for n in self.nodes_inbound:
            if n.terminate_flag.is_set():
                self.inbound_node_disconnected(n)
                n.join()
                del self.nodes_inbound[self.nodes_inbound.index(n)]

        for n in self.nodes_outbound:
            if n.terminate_flag.is_set():
                self.outbound_node_disconnected(n)
                n.join()
                del self.nodes_outbound[self.nodes_inbound.index(n)]

    def send_data_to_nodes(self, data, exclude=[]):

        self.message_count_send = self.message_count_send + 1
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

        self.message_count_send = self.message_count_send + 1
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

            if node_is_unl(connected_node_id):
                thread_client = self.create_the_new_connection(sock, connected_node_id, host, port)
                thread_client.start()

                self.nodes_outbound.append(thread_client)
                self.outbound_node_connected(thread_client)
            else:
                dprint("Node System: Could not connect with node because node is not unl node.")
        except Exception as e:
            dprint("Node System: TcpServer.connect_to_node: Could not connect with node. (" + str(e) + ")")
        




    def disconnect_to_node(self, node):

        if node in self.nodes_outbound:
            self.node_disconnect_to_outbound_node(node)
            node.stop()
            node.join()
            del self.nodes_outbound[self.nodes_outbound.index(node)]

        else:
            print("Node System: Node disconnect_to_node: cannot disconnect with a node with which we are not connected.")

    def stop(self):

        self.node_request_to_stop()
        self.terminate_flag.set()


    def create_the_new_connection(self, connection, id, host, port):

        return Node_Connection(self, connection, id, host, port)

    def run(self):

        while not self.terminate_flag.is_set():
            try:
                connection, client_address = self.sock.accept()
                
                connected_node_id = connection.recv(4096).decode('utf-8')
                connection.send(self.id.encode('utf-8'))
                if node_is_unl(connected_node_id):
                    thread_client = self.create_the_new_connection(connection, connected_node_id, client_address[0], client_address[1])
                    thread_client.start()

                    self.nodes_inbound.append(thread_client)

                    self.inbound_node_connected(thread_client)
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

    def outbound_node_connected(self, node):
        dprint("Node System: outbound_node_connected: " + node.id)
 

    def inbound_node_connected(self, node):
        dprint("Node System: inbound_node_connected: " + node.id)
 

    def inbound_node_disconnected(self, node):
        dprint("Node System: inbound_node_disconnected: " + node.id)


    def outbound_node_disconnected(self, node):
        dprint("Node System: outbound_node_disconnected: " + node.id)


    def message_from_node(self, node, data):
        dprint("Node System: message_from_node: " + node.id + ": " + str(data))
        if self.callback is not None:
            self.callback("message_from_node", self, node, data)

    def node_disconnect_to_outbound_node(self, node):
        dprint("Node System: node wants to disconnect with oher outbound node: " + node.id)


    def node_request_to_stop(self):
        dprint("Node System: node is requested to stop!")


    def __str__(self):
        return 'Node: {}:{}'.format(self.host, self.port)

    def __repr__(self):
        return '<Node {}:{} id: {}>'.format(self.host, self.port, self.id)


    
