#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import socket
import sys
import threading
import time
from hashlib import sha256

from blockchain.block.get_block import GetBlock
from config import CONNECTED_NODE_PATH
from config import LOADING_BLOCK_PATH
from config import TEMP_ACCOUNTS_PATH
from config import TEMP_BLOCK_PATH
from config import TEMP_BLOCKSHASH_PATH
from lib.log import get_logger
from lib.merkle_root import MerkleTree
from node.node import *
from node.node_connection import Node_Connection
from node.unl import Unl
from transactions.transaction import Transaction
from wallet.wallet import Ecdsa
from wallet.wallet import PrivateKey
from wallet.wallet import PublicKey
from wallet.wallet import Signature
from wallet.wallet import Wallet_Import

logger = get_logger("NODE")


class Node(threading.Thread):

    main_node = None
    unl_nodes = []

    id = "".join([
        l.strip() for l in Wallet_Import(0, 0).splitlines()
        if l and not l.startswith("-----")
    ])

    def __init__(self, host, port, callback=None):
        self.__class__.main_node = self
        super(Node, self).__init__()

        self.terminate_flag = threading.Event()

        self.host = host
        self.port = port

        self.callback = callback

        self.nodes_inbound = []

        self.nodes_outbound = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()

        self.start()

    def run(self):

        while not self.terminate_flag.is_set():
            try:
                connection, client_address = self.sock.accept()

                connected_node_id = connection.recv(4096).decode("utf-8")
                connection.send(Node.id.encode("utf-8"))
                if Unl.node_is_unl(connected_node_id):
                    thread_client = self.create_the_new_connection(
                        connection,
                        connected_node_id,
                        client_address[0],
                        client_address[1],
                    )
                    thread_client.start()

                    self.nodes_inbound.append(thread_client)
                else:
                    logger.warning(
                        "Node System: Could not connect with node because node is not unl node."
                    )

            except socket.timeout:
                pass

            except Exception as e:
                raise e

            time.sleep(0.01)

        logger.info("Node System: Stopping protocol started by node")
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
        logger.info("Node System: The node is stopped")

    def init_server(self):
        logger.info("Node System: Node server is starting")
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
                logger.info(
                    "Node System: Node send_data_to_nodes: Node is excluded")
            else:
                try:
                    self.send_data_to_node(n, data)
                except:  # lgtm [py/catch-base-exception]
                    pass

        for n in self.nodes_outbound:
            if n in exclude:
                logger.info(
                    "Node System: Node send_data_to_nodes: Node is excluded")
            else:
                try:
                    self.send_data_to_node(n, data)
                except:  # lgtm [py/catch-base-exception]
                    pass

    def send_data_to_node(self, n, data):

        self.delete_closed_connections()
        if n in self.nodes_inbound or n in self.nodes_outbound:
            try:
                n.send(data)

            except Exception as e:
                logger.exception(
                    "Node System: Node send_data_to_node: Could not send data to node"
                )
        else:
            logger.warning(
                "Node System: Node send_data_to_node: Node is not connected")

    def connect_to_node(self, host, port):

        if host == self.host and port == self.port:
            logger.error(
                "Node System: Node connect_to_node: You can not connect to yourself"
            )
            return False

        for node in self.nodes_outbound:
            if node.host == host and node.port == port:
                logger.warning(
                    "Node System: connect_to_node: Node is already connected")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logger.info("Node System: Connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            # Basic information exchange (not secure) of the id's of the nodes!
            # Send my id to the connected node!
            sock.send(Node.id.encode("utf-8"))
            # When a node is connected, it sends it id!
            connected_node_id = sock.recv(4096).decode("utf-8")

            if Unl.node_is_unl(connected_node_id):
                thread_client = self.create_the_new_connection(
                    sock, connected_node_id, host, port)
                thread_client.start()

                self.nodes_outbound.append(thread_client)
            else:
                logger.warning(
                    "Node System: Could not connect with node because node is not unl node."
                )
        except Exception as e:
            logger.exception("Node System: Could not connect with node")

    def disconnect_to_node(self, node):

        if node in self.nodes_outbound:
            node.stop()
            node.join()
            del self.nodes_outbound[self.nodes_outbound.index(node)]

        else:
            print(
                "Node System: Node disconnect_to_node: Node is not connected")

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
        with open(CONNECTED_NODE_PATH, "rb") as connected_node_file:
            return json.load(connected_node_file)

    @staticmethod
    def save_connected_node(host, port, id):
        """
        Saves the connected nodes.
        """

        node_list = Node.get_connected_node()

        already_in_list = False

        for element in node_list:
            if (node_list[element]["host"] == host
                    and node_list[element]["port"] == port):
                already_in_list = True

        if not already_in_list:
            node_list[id] = {}
            node_list[id]["host"] = host
            node_list[id]["port"] = port

            sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

            from lib.config_system import get_config

            os.chdir(get_config()["main_folder"])
            with open(CONNECTED_NODE_PATH, "w") as connected_node_file:
                json.dump(node_list, connected_node_file, indent=4)

    @staticmethod
    def connectionfrommixdb():
        """
        Connects to the mixdb.
        """

        node_list = Node.get_connected_node()
        from node.node import Node

        for element in node_list:
            Node.main_node.connect_to_node(node_list[element]["host"],
                                           node_list[element]["port"])

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
            with open(CONNECTED_NODE_PATH, "w") as connected_node_file:
                json.dump(saved_nodes, connected_node_file, indent=4)

    def message_from_node(self, node, data):

        if str(data) == "sendmefullblock":
            self.send_full_chain(node)

        try:
            if (data["fullblock"] == 1 and Unl.node_is_unl(node.id)
                    and Ecdsa.verify(
                        "fullblock" + data["byte"],
                        Signature.fromBase64(data["signature"]),
                        PublicKey.fromPem(node.id),
                    )):
                print("getting chain")
                self.get_full_chain(data, node)
        except Exception as e:
            print(e)

        try:

            if (data["fullaccounts"] == 1 and Unl.node_is_unl(node.id)
                    and Ecdsa.verify(
                        "fullaccounts" + data["byte"],
                        Signature.fromBase64(data["signature"]),
                        PublicKey.fromPem(node.id),
                    )):
                print("getting chain")
                self.get_full_accounts(data, node)
        except Exception as e:
            print(e)

        try:

            if (data["fullblockshash"] == 1 and Unl.node_is_unl(node.id)
                    and Ecdsa.verify(
                        "fullblockshash" + data["byte"],
                        Signature.fromBase64(data["signature"]),
                        PublicKey.fromPem(node.id),
                    )):
                self.get_full_blockshash(data, node)
        except Exception as e:
            print(e)

        try:
            if data["transactionrequest"] == 1:
                self.get_transaction(data, node)
        except Exception as e:
            print(e)

        try:
            if data["action"] == "myblock":
                self.get_candidate_block(data, node)
        except Exception as e:
            print(e)

        try:
            if data["action"] == "myblockhash":
                self.get_candidate_block_hash(data, node)
        except Exception as e:
            print(e)

    def send_my_block(self, nodes):
        system = GetBlock()

        new_list = []

        signature_list = []

        for element in system.validating_list:
            new_list.append(element.dump_json())
            signature_list.append(element.signature)

        Merkle_signature_list = (MerkleTree(signature_list).getRootHash()
                                 if len(signature_list) != 0 else "0")

        data = {
            "action":
            "myblock",
            "transaction":
            new_list,
            "sequance_number":
            system.sequance_number,
            "signature":
            Ecdsa.sign(
                "myblock" + Merkle_signature_list +
                str(system.sequance_number),
                PrivateKey.fromPem(Wallet_Import(0, 1)),
            ).toBase64(),
        }

        for each_node in nodes:
            self.send_data_to_node(each_node, data)

    def send_my_block_hash(self, nodes):
        system = GetBlock()

        if system.raund_1 and not system.raund_2:

            data = {
                "action":
                "myblockhash",
                "hash":
                system.hash,
                "sequance_number":
                system.sequance_number,
                "signature":
                Ecdsa.sign(
                    "myblockhash" + system.hash + str(system.sequance_number),
                    PrivateKey.fromPem(Wallet_Import(0, 1)),
                ).toBase64(),
            }

            for each_node in nodes:
                self.send_data_to_node(each_node, data)

    def get_candidate_block(self, data, node):

        if (Unl.node_is_unl(node.id)
                and GetBlock().sequance_number == data["sequance_number"]):

            signature_list = []
            for element in data["transaction"]:
                signature_list.append(element["signature"])

            merkle_root_of_signature_list = (
                MerkleTree(signature_list).getRootHash()
                if len(signature_list) != 0 else "0")

            if Ecdsa.verify(
                    "myblock" + merkle_root_of_signature_list +
                    str(data["sequance_number"]),
                    Signature.fromBase64(data["signature"]),
                    PublicKey.fromPem(node.id),
            ):

                temp_tx = []

                for element in data["transaction"]:
                    temp_tx.append(Transaction.load_json(element))

                data["transaction"] = temp_tx

                node.candidate_block = data

    def get_candidate_block_hash(self, data, node):

        if (Unl.node_is_unl(node.id)
                and GetBlock().sequance_number == data["sequance_number"]):

            if Ecdsa.verify(
                    "myblockhash" + data["hash"] +
                    str(data["sequance_number"]),
                    Signature.fromBase64(data["signature"]),
                    PublicKey.fromPem(node.id),
            ):
                data["sender"] = node.id

                node.candidate_block_hash = data

    def send_full_chain(self, node=None):
        file = open(TEMP_BLOCK_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "fullblock":
                1,
                "byte": (SendData.decode(encoding="iso-8859-1")),
                "signature":
                Ecdsa.sign(
                    "fullblock" + str(
                        (SendData.decode(encoding="iso-8859-1"))),
                    PrivateKey.fromPem(Wallet_Import(0, 1)),
                ).toBase64(),
            }
            if not node is None:
                self.send_data_to_node(node, data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "fullblock":
                    1,
                    "byte":
                    "end",
                    "signature":
                    Ecdsa.sign("fullblock" + "end",
                               PrivateKey.fromPem(Wallet_Import(
                                   0, 1))).toBase64(),
                }
                if not node is None:
                    self.send_data_to_node(node, data)
                else:
                    self.send_data_to_nodes(data)

    def send_full_accounts(self, node=None):
        file = open(TEMP_ACCOUNTS_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "fullaccounts":
                1,
                "byte": (SendData.decode(encoding="iso-8859-1")),
                "signature":
                Ecdsa.sign(
                    "fullaccounts" + str(
                        (SendData.decode(encoding="iso-8859-1"))),
                    PrivateKey.fromPem(Wallet_Import(0, 1)),
                ).toBase64(),
            }
            if not node is None:
                self.send_data_to_node(node, data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "fullaccounts":
                    1,
                    "byte":
                    "end",
                    "signature":
                    Ecdsa.sign("fullaccounts" + "end",
                               PrivateKey.fromPem(Wallet_Import(
                                   0, 1))).toBase64(),
                }
                if not node is None:
                    self.send_data_to_node(node, data)
                else:
                    self.send_data_to_nodes(data)

    def send_full_blockshash(self, node=None):
        file = open(TEMP_BLOCKSHASH_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "fullblockshash":
                1,
                "byte": (SendData.decode(encoding="iso-8859-1")),
                "signature":
                Ecdsa.sign(
                    "fullblockshash" + str(
                        (SendData.decode(encoding="iso-8859-1"))),
                    PrivateKey.fromPem(Wallet_Import(0, 1)),
                ).toBase64(),
            }
            if not node is None:
                self.send_data_to_node(node, data)
            else:
                self.send_data_to_nodes(data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "fullblockshash":
                    1,
                    "byte":
                    "end",
                    "signature":
                    Ecdsa.sign(
                        "fullblockshash" + "end",
                        PrivateKey.fromPem(Wallet_Import(0, 1)),
                    ).toBase64(),
                }
                if not node is None:
                    self.send_data_to_node(node, data)
                else:
                    self.send_data_to_nodes(data)

    def get_full_chain(self, data, node):

        get_ok = False

        if not os.path.exists(TEMP_BLOCK_PATH):
            get_ok = True
        else:
            system = GetBlock()
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:

            if str(data["byte"]) == "end":

                os.rename(LOADING_BLOCK_PATH, TEMP_BLOCK_PATH)

                from consensus.consensus_main import consensus_trigger
                from lib.perpetualtimer import perpetualTimer

                system = GetBlock()
                system.newly = True
                from transactions.change_transaction_fee import \
                    ChangeTransactionFee

                ChangeTransactionFee(system)

                system.exclude_validators = []
                perpetualTimer(system.consensus_timer,
                               consensus_trigger).start()
                system.save_block()

            else:
                file = open(LOADING_BLOCK_PATH, "ab")

                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    def get_full_blockshash(self, data, node):

        get_ok = False

        if not os.path.exists(TEMP_BLOCKSHASH_PATH):
            get_ok = True
        else:
            system = GetBlock()
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            file = open(TEMP_BLOCKSHASH_PATH, "ab")

            file.write((data["byte"].encode(encoding="iso-8859-1")))
            file.close()

    def get_full_accounts(self, data, node):

        get_ok = False

        if not os.path.exists(TEMP_ACCOUNTS_PATH):
            get_ok = True
        else:
            system = GetBlock()
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            file = open(TEMP_ACCOUNTS_PATH, "ab")

            file.write((data["byte"].encode(encoding="iso-8859-1")))
            file.close()

    def get_transaction(self, data, node):
        system = GetBlock()
        from transactions.send_transaction_to_the_block import \
            SendTransactiontoTheBlock

        SendTransactiontoTheBlock(
            system,
            sequance_number=data["sequance_number"],
            signature=data["signature"],
            fromUser=data["fromUser"],
            toUser=data["to_user"],
            data=data["data"],
            amount=data["amount"],
            transaction_fee=data["transaction_fee"],
            transaction_sender=node,
            transaction_time=data["transaction_time"],
        )
