#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from threading import Thread
import socket
import json
from hashlib import sha256
import os

from decentra_network.blockchain.block.change_transaction_fee import \
    ChangeTransactionFee
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import CONNECTED_NODES_PATH
from decentra_network.config import LOADING_BLOCK_PATH
from decentra_network.config import LOADING_ACCOUNTS_PATH
from decentra_network.config import LOADING_BLOCKSHASH_PATH
from decentra_network.config import LOADING_BLOCKSHASH_PART_PATH
from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.config import TEMP_BLOCKSHASH_PATH
from decentra_network.config import TEMP_BLOCKSHASH_PART_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from decentra_network.lib.mix.merkle_root import MerkleTree
from decentra_network.node.unl import Unl
from decentra_network.transactions.check.check_transaction import \
    CheckTransaction
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.ecdsa import Ecdsa
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey
from decentra_network.wallet.ellipticcurve.publicKey import PublicKey
from decentra_network.wallet.ellipticcurve.signature import Signature
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.node.client.client import client
import time
import contextlib

logger = get_logger("NODE")




class server(Thread):
    Server = None
    id = wallet_import(0, 0)
    def __init__(self, host, port, save_messages=False, test=False):
        self.__class__.Server = self      
        Thread.__init__(self)
        self.running = True
        
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.clients = []

        self.messages = []
        self.save_messages = False

        self.start()

    def run(self):
        self.sock.settimeout(10.0)
        while self.running:
            with contextlib.suppress(socket.timeout):
                conn, addr = self.sock.accept()
                connected = any(a_client.socket == conn for a_client in self.clients)
                data = conn.recv(4096)
                conn.send(server.id.encode("utf-8"))
                client_id = data.decode("utf-8")
                if Unl.node_is_unl(client_id):
                    self.clients.append(client(conn, addr, client_id, self))
                    server.save_connected_node(addr[0], addr[1], client_id)
            time.sleep(0.01)
        for c in self.clients:
            c.stop()
        time.sleep(1)
        for c in self.clients:
            c.join()
        self.sock.settimeout(None)
        self.sock.close()

    def stop(self):
        self.running = False
    
    def send(self, data):
        data["id"] = server.id
        sign = Ecdsa.sign(
                        str(data),
                        PrivateKey.fromPem(wallet_import(0, 1)),
                    ).toBase64()

        data["signature"] = sign
        for a_client in self.clients:
            a_client.socket.sendall(json.dumps(data).encode("utf-8"))
        return data

    def send_client(self, node, data):
        data["id"] = server.id
        sign = Ecdsa.sign(
                        str(data),
                        PrivateKey.fromPem(wallet_import(0, 1)),
                    ).toBase64()

        data["signature"] = sign
        node.socket.sendall(json.dumps(data).encode("utf-8"))
        return data

    def get_message(self, client, data):
        if self.check_message(data):
            logger.info("New message: {}".format(data))
            self.messages.append(data)
            self.direct_message(client, data)

    def check_message(self, data):
        # remove sign from data
        sign = data["signature"]
        del data["signature"]
        message = str(data)
        data["signature"] = sign
        return Ecdsa.verify(
                        message,
                        Signature.fromBase64(sign),
                        PublicKey.fromPem(data["id"]),
                    )
    
    def connect(self, host, port):
        connected = any(a_client.host == host and a_client.port == port for a_client in self.clients)
        if not connected:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = (host, port)
            conn.connect(addr)
            conn.send(server.id.encode("utf-8"))
            client_id = conn.recv(4096).decode("utf-8")                
            if Unl.node_is_unl(client_id):
                    self.clients.append(client(conn, addr, client_id, self))


    @staticmethod
    def get_connected_nodes():
        """
        Returns the connected nodes.
        """

        if not os.path.exists(CONNECTED_NODES_PATH):
            return {}

        the_pending_list = {}
        os.chdir(get_config()["main_folder"])
        for entry in os.scandir(CONNECTED_NODES_PATH):
            if entry.name != "README.md":
                with open(entry.path, "r") as my_transaction_file:
                    loaded_json = json.load(my_transaction_file)
                    the_pending_list[loaded_json["id"]] = loaded_json

        return the_pending_list



    @staticmethod
    def save_connected_node(host, port, node_id):
        """
        Saves the connected nodes.
        """

        node_list = {}
        node_list["id"] = node_id
        node_list["host"] = host
        node_list["port"] = port

        node_id = sha256((node_id).encode("utf-8")).hexdigest()
        file_name = CONNECTED_NODES_PATH + f"{node_id}.json"
        os.chdir(get_config()["main_folder"])
        with open(file_name, "w") as connected_node_file:
            json.dump(node_list, connected_node_file, indent=4)

    @staticmethod
    def connectionfrommixdb():
        """
        Connects to the mixdb.
        """

        node_list = server.Server.get_connected_nodes()

        for element in node_list:
            server.Server.connect(node_list[element]["host"],
                                           node_list[element]["port"])

    @staticmethod
    def connected_node_delete(node_id):
        """
        Deletes a connected node.
        """
        os.chdir(get_config()["main_folder"])
        node_id = sha256((node_id).encode("utf-8")).hexdigest()
        for entry in os.scandir(CONNECTED_NODES_PATH):
            if entry.name == f"{node_id}.json":
                os.remove(entry.path)


    def direct_message(self, node, data):
        logger.info("Directing message: {}".format(data["action"]))
        if "sendmefullblock" == data["action"]:
            self.send_block_to_other_nodes(node)

        if "fullblock" == data["action"]:
            self.get_full_chain(data, node)

        if "fullaccounts" == data["action"]:
            self.get_full_accounts(data, node)

        if "fullblockshash" == data["action"]:
            self.get_full_blockshash(data, node)

        if "fullblockshash_part" == data["action"]:
            self.get_full_blockshash_part(data, node)

        if "transactionrequest" == data["action"]:
            self.get_transaction(data, node)

        if "myblock" == data["action"]:
            self.get_candidate_block(data, node)

        if "myblockhash" == data["action"]:
            self.get_candidate_block_hash(data, node)


    def send_my_block(self, block):
        system = block

        new_list = []

        signature_list = []

        for element in system.validating_list:
            new_list.append(element.dump_json())
            signature_list.append(element.signature)


        data = {
            "action":
            "myblock",
            "transaction":
            new_list,
            "sequance_number":
            system.sequance_number,
        }
        self.send(data)

    def send_my_block_hash(self, block):
        system = block

        if system.raund_1 and not system.raund_2:

            data = {
                "action":
                "myblockhash",
                "hash":
                system.hash,
                "sequance_number":
                system.sequance_number,
            }

            
            self.send(data)

    def get_candidate_block(self, data, node):
        logger.info("Getting candidate block: {}".format(data["sequance_number"]))
        if GetBlock().sequance_number != data["sequance_number"]:
            logger.info("Candidate block sequance number is not correct")
            return False

        temp_tx = [
            Transaction.load_json(element)
            for element in data["transaction"]
        ]

        data["transaction"] = temp_tx

        node.candidate_block = data

    def get_candidate_block_hash(self, data, node):

        if GetBlock().sequance_number == data["sequance_number"]:
            data["sender"] = node.id
            node.candidate_block_hash = data

    def send_full_chain(self, node=None):
        file = open(TEMP_BLOCK_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "action":"fullblock",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }
            if node is None:
                self.send(data)
            else:
                self.send_client(node, data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "action":"fullblock",
                    "byte":"end",
                }
                if node is None:
                    self.send(data)
                else:
                    self.send_client(node, data)

    def send_full_accounts(self, node=None):
        file = open(TEMP_ACCOUNTS_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "action":"fullaccounts",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }
            if node is None:
                self.send(data)
            else:
                self.send_client(node, data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "action":"fullaccounts",
                    "byte":
                    "end"
                }
                if node is None:
                    self.send(data)
                else:
                    self.send_client(node, data)

    def send_full_blockshash(self, node=None):
        file = open(TEMP_BLOCKSHASH_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "action":"fullblockshash",
                "byte": (SendData.decode(encoding="iso-8859-1"))
            }
            if node is None:
                self.send(data)
            else:
                self.send_client(node, data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "action":"fullblockshash",
                    "byte":
                    "end"
                }
                if node is None:
                    self.send(data)
                else:
                    self.send_client(node, data)

    def send_full_blockshash_part(self, node=None):
        file = open(TEMP_BLOCKSHASH_PART_PATH, "rb")
        SendData = file.read(1024)
        while SendData:

            data = {
                "action":"fullblockshash_part",
                "byte": (SendData.decode(encoding="iso-8859-1"))
            }
            if node is None:
                self.send(data)
            else:
                self.send_client(node, data)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "action":"fullblockshash_part",
                    "byte":
                    "end"
                }
                if node is None:
                    self.send(data)
                else:
                    self.send_client(node, data)

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

                from decentra_network.lib.perpetualtimer import perpetualTimer

                system = GetBlock()
                system.newly = True

                ChangeTransactionFee(system)

                system.exclude_validators = []
                perpetualTimer(system.consensus_timer,
                               consensus_trigger).start()
                SaveBlock(system)

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
            if str(data["byte"]) == "end":
                os.rename(LOADING_BLOCKSHASH_PATH, TEMP_BLOCKSHASH_PATH)
            else:
                file = open(LOADING_BLOCKSHASH_PATH, "ab")
                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()
                            

    def get_full_blockshash_part(self, data, node):

        get_ok = False

        if not os.path.exists(TEMP_BLOCKSHASH_PART_PATH):
            get_ok = True
        else:
            system = GetBlock()
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            if str(data["byte"]) == "end":
                os.rename(LOADING_BLOCKSHASH_PART_PATH, TEMP_BLOCKSHASH_PART_PATH)
            else:
                file = open(LOADING_BLOCKSHASH_PART_PATH, "ab")
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
            if str(data["byte"]) == "end":
                os.rename(LOADING_ACCOUNTS_PATH, TEMP_ACCOUNTS_PATH)
            else:
                file = open(LOADING_ACCOUNTS_PATH, "ab")
                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    @staticmethod
    def send_transaction(tx):
        """
        Sends the given transaction to UNL nodes.
        """

        items = {
            "action":"transactionrequest",
            "sequance_number": tx.sequance_number,
            "txsignature": tx.signature,
            "fromUser": tx.fromUser,
            "to_user": tx.toUser,
            "data": tx.data,
            "amount": tx.amount,
            "transaction_fee": tx.transaction_fee,
            "transaction_time": tx.transaction_time,
        }
        for each_node in Unl.get_as_node_type(Unl.get_unl_nodes()):
            server.Server.send_client(each_node, items)

    def get_transaction(self, data, node):
        block = GetBlock()
        the_transaction = Transaction(
            data["sequance_number"],
            data["txsignature"],
            data["fromUser"],
            data["to_user"],
            data["data"],
            data["amount"],
            data["transaction_fee"],
            data["transaction_time"],
        )
        if GetTransaction(block, the_transaction):
            server.send_transaction(the_transaction)
            SaveBlock(block)

    def send_block_to_other_nodes(self, node=None):
        """
        Sends the block to the other nodes.
        """
        self.send_full_chain(node=node)
        self.send_full_accounts(node=node)
        self.send_full_blockshash(node=node)
        self.send_full_blockshash_part(node=node)
