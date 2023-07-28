#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import copy
import json
import os
import random
import socket
import time
from hashlib import sha256
from shutil import move
from threading import Thread
import traceback

from naruno.accounts.save_accounts import accounts_db
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import blockshash_db
from naruno.blockchain.block.change_transaction_fee import ChangeTransactionFee
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.save_block import SaveBlock
from naruno.config import CONNECTED_NODES_PATH
from naruno.config import LOADING_ACCOUNTS_PATH
from naruno.config import LOADING_BLOCK_PATH
from naruno.config import LOADING_BLOCKSHASH_PART_PATH
from naruno.config import LOADING_BLOCKSHASH_PATH
from naruno.config import PENDING_TRANSACTIONS_PATH
from naruno.config import TEMP_ACCOUNTS_PATH
from naruno.config import TEMP_BLOCK_PATH
from naruno.config import TEMP_BLOCKSHASH_PART_PATH
from naruno.config import TEMP_BLOCKSHASH_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT
from naruno.lib.log import get_logger
from naruno.node.client.client import client
from naruno.node.unl import Unl
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.ellipticcurve.ecdsa import Ecdsa
from naruno.wallet.ellipticcurve.privateKey import PrivateKey
from naruno.wallet.ellipticcurve.publicKey import PublicKey
from naruno.wallet.ellipticcurve.signature import Signature
from naruno.wallet.wallet_import import wallet_import

from naruno.node.get_candidate_blocks import self_candidates
import naruno

connectednodes_db = KOT("connectednodes",
                        folder=get_config()["main_folder"] + "/db")
 


tx_signature_list = {}



class server(Thread):
    Server = None
    id = wallet_import(0, 0)

    def __init__(
        self,
        host,
        port,
        save_messages=False,
        test=False,
        custom_variables=False,
        custom_TEMP_BLOCK_PATH=None,
        custom_TEMP_ACCOUNTS_PATH=None,
        custom_TEMP_BLOCKSHASH_PATH=None,
        custom_TEMP_BLOCKSHASH_PART_PATH=None,
        custom_LOADING_BLOCK_PATH=None,
        custom_LOADING_ACCOUNTS_PATH=None,
        custom_LOADING_BLOCKSHASH_PATH=None,
        custom_LOADING_BLOCKSHASH_PART_PATH=None,
        custom_CONNECTED_NODES_PATH=None,
        custom_PENDING_TRANSACTIONS_PATH=None,
        time_control=None,
        custom_id=None,
    ):
        Thread.__init__(self)
        self.running = True

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.clients = []
        self.sync_clients = []

        self.messages = []
        self.our_messages = []
        self.save_messages = save_messages

        self.TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH
                                is None else custom_TEMP_BLOCK_PATH)
        self.TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH
                                   if custom_TEMP_ACCOUNTS_PATH is None else
                                   custom_TEMP_ACCOUNTS_PATH)
        self.TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                     if custom_TEMP_BLOCKSHASH_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PATH)
        self.TEMP_BLOCKSHASH_PART_PATH = (
            TEMP_BLOCKSHASH_PART_PATH if custom_TEMP_BLOCKSHASH_PART_PATH
            is None else custom_TEMP_BLOCKSHASH_PART_PATH)
        self.LOADING_BLOCK_PATH = (LOADING_BLOCK_PATH
                                   if custom_LOADING_BLOCK_PATH is None else
                                   custom_LOADING_BLOCK_PATH)
        self.LOADING_ACCOUNTS_PATH = (LOADING_ACCOUNTS_PATH
                                      if custom_LOADING_ACCOUNTS_PATH is None
                                      else custom_LOADING_ACCOUNTS_PATH)
        self.LOADING_BLOCKSHASH_PATH = (LOADING_BLOCKSHASH_PATH if
                                        custom_LOADING_BLOCKSHASH_PATH is None
                                        else custom_LOADING_BLOCKSHASH_PATH)
        self.LOADING_BLOCKSHASH_PART_PATH = (
            LOADING_BLOCKSHASH_PART_PATH if custom_LOADING_BLOCKSHASH_PART_PATH
            is None else custom_LOADING_BLOCKSHASH_PART_PATH)

        self.CONNECTED_NODES_PATH = (None if custom_CONNECTED_NODES_PATH
                                     is None else custom_CONNECTED_NODES_PATH)

        self.PENDING_TRANSACTIONS_PATH = (
            PENDING_TRANSACTIONS_PATH if custom_PENDING_TRANSACTIONS_PATH
            is None else custom_PENDING_TRANSACTIONS_PATH)

        self.custom_variables = custom_variables

        self.time_control = 10 if time_control is None else time_control

        if custom_id is not None:
            self.id = custom_id
        else:
            self.id = server.id

        self.logger = get_logger(f"NODE_{self.host}_{self.port}")

        self.logger.info(f"Server started as {server.id}")

        self.logger.debug("Save messages: " + str(save_messages))
        self.logger.debug("Test mode: " + str(test))


        self.send_busy = []


        a_block = Block("onur")
        self.logger.debug(f"Block max_data_size: {a_block.max_data_size}")
        self.logger.debug(f"Block max_tx_number: {a_block.max_tx_number}")
        self.buffer_size = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 1.5)
        self.buffer_size_2 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 1.5)
        self.buffer_size_3 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 5)    
        self.buffer_size_4 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 0.5)   

      
        if not test:
            self.__class__.Server = self
            self.start()

    def check_connected(self, host, port):
        for a_client in self.clients:
            if a_client.host == host and a_client.port == port:
                return True

        return False

    def run(self):
        self.logger.info("Server ear started")
        self.sock.settimeout(10.0)
        while self.running:
            with contextlib.suppress(Exception):
                conn, addr = self.sock.accept()
                self.logger.debug(f"New connection request: {addr}")
                data = conn.recv(1024)
                
                raw_id = data.decode("utf-8")
                client_id = raw_id.split("-")[0]
                client_type = int(raw_id.split("-")[1])
                conn.send((self.id+"-"+str(client_type)).encode("utf-8"))
                self.logger.debug(f"New connection id: {client_id}")
                if Unl.node_is_unl(client_id):
                    self.logger.info(f"Confirmed")
                    self.clients.append(client(conn, addr, client_id, self, c_type=client_type))
                    self.save_connected_node(addr[0], addr[1], client_id)
                else:
                    self.logger.warning(f"Rejected")
            time.sleep(0.01)

    def stop(self):
        self.running = False
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            (self.host, self.port))
        for c in self.clients:
            c.stop()
        time.sleep(1)
        for c in self.clients:
            c.join()
        self.sock.close()

    def prepare_message(self, data):
        data["id"] = server.id
        data["timestamp"] = str(time.time())
        sign = Ecdsa.sign(
            str(data),
            PrivateKey.fromPem(wallet_import(0, 1)),
        ).toBase64()

        data["signature"] = sign
        return data

    def send(self, data, except_client=None, c_type=0):
        data = self.prepare_message(data)

        for a_client in self.clients:
            if a_client != except_client:
                if a_client.c_type == c_type:
                    self.send_client(a_client, data, ready_to_send=True, c_type=c_type)
        try:
            del data["buffer"]
        except KeyError:
            pass
        return data

    def send_client(self, node, data, ready_to_send=False, c_type=0):
        self.logger.debug(
            f"Sending message: {data} to {node.host}:{node.port}={node.id}")
        if not ready_to_send:
            data = self.prepare_message(data)



        if c_type == 0:
            the_buffer = self.buffer_size
        elif c_type == 1:
            the_buffer = self.buffer_size_2
        elif c_type == 2:
            the_buffer = self.buffer_size_3
        elif c_type == 3:
            the_buffer = self.buffer_size_4

        before_buffer_size = len(json.dumps(data).encode("utf-8"))
        self.logger.debug(
            f"Before buffer size: {before_buffer_size}")

        if before_buffer_size < the_buffer:
            self.logger.debug("Buffer is not full")
            self.logger.debug(f"the_buffer: {the_buffer}")
            self.logger.debug(f"before_buffer_size: {before_buffer_size}")
            result = ((the_buffer - before_buffer_size) - 14)
            self.logger.debug(f"result: {result}")
            data["buffer"] = "0" * result
            self.logger.debug(
                f"After buffer size: {len(json.dumps(data).encode('utf-8'))}")
        while node.id+str(c_type) in self.send_busy:
            time.sleep(0.01)
        self.send_busy.append(node.id+str(c_type))
        try:
            with contextlib.suppress(socket.timeout):
                node.socket.sendall(json.dumps(data).encode("utf-8"))
                time.sleep(0.02)
        except:
            traceback.print_exc()
        self.send_busy.remove(node.id+str(c_type))
        with contextlib.suppress(KeyError):
            del data["buffer"]
        if self.save_messages:
            self.our_messages.append(data)
        return data

    def get_message(self, client, data, hash_of_data=""):
        self.logger.info(
            f"Starting to proccess the message ({hash_of_data}) of {client.id}:{client.host}:{client.port}"
        )
        if self.check_message(data):
            self.logger.debug(f"Message is valid")
            if self.save_messages:
                self.messages.append(data)
            self.direct_message(client, data, hash_of_data)
        else:
            self.logger.error(f"Message is not in a valid format")

    def check_message(self, data):
        if "id" not in data:
            self.logger.error("No id")
            return False
        if "signature" not in data:
            self.logger.error("No signature")
            return False
        if "timestamp" not in data:
            self.logger.error("No timestamp")
            return False
        # the_control = time.time() - float(data["timestamp"])
        # if the_control > self.time_control:
        #    logger.debug("Time control is not true")
        #    return False
        # remove sign from data
        sign = data["signature"]
        del data["signature"]
        message = str(data)
        data["signature"] = sign

        signature_verify = Ecdsa.verify(
            message,
            Signature.fromBase64(sign),
            PublicKey.fromPem(data["id"]),
        )

        if not signature_verify:
            self.logger.error("Signature not valid")
            return False

        return True


    def _connect(self, host, port, c_type=0):
            self.logger.info(
                "New connection request confirmed trying to connect")
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(10.0)
            addr = (host, port)
            try:
                conn.connect(addr)
                conn.send((self.id+"-"+str(c_type)).encode("utf-8"))                
                raw_id = conn.recv(1024).decode("utf-8")
                client_id = raw_id.split("-")[0]
                client_type = int(raw_id.split("-")[1])                
                if Unl.node_is_unl(client_id):
                    self.logger.info(
                        f"Succesfully connected to {client_id} on {host}:{port}"
                    )
                    self.clients.append(client(conn, addr, client_id, self, c_type=client_type))
                    self.save_connected_node(addr[0], addr[1], client_id)
                    return True
            except socket.timeout:
                self.logger.warning(f"Connection timeout")
                conn.close()
            except ConnectionRefusedError:
                self.logger.warning(f"Connection refused")
                conn.close()    

    def connect(self, host, port):
        self.logger.info(f"Asking for new node on {host}:{port}")
        connected = self.check_connected(host=host, port=port)
        if not connected:
            self._connect(host, port)
            time.sleep(1)
            self._connect(host, port, c_type=1)
            time.sleep(1)
            self._connect(host, port, c_type=2)
            time.sleep(1)
            self._connect(host, port, c_type=3)
        else:
            self.logger.warning("Already connected")

    @staticmethod
    def get_connected_nodes(custom_CONNECTED_NODES_PATH=None):
        """
        Returns the connected nodes.
        """

        the_pending_list = {}
        all_records = (connectednodes_db.get_all()
                       if custom_CONNECTED_NODES_PATH is None else KOT(
                           "connectednodes" + custom_CONNECTED_NODES_PATH,
                           folder=get_config()["main_folder"] + "/db",
                       ).get_all())
        for entry in all_records:
            loaded_json = all_records[entry]
            the_pending_list[loaded_json["host"] + str(loaded_json["port"]) +
                             loaded_json["id"]] = loaded_json

        return the_pending_list

    def save_connected_node(self, host, port, node_id):
        """
        Saves the connected nodes.
        """

        node_list = {}
        node_list["id"] = node_id
        node_list["host"] = host
        node_list["port"] = port

        node_id = sha256(
            (node_id + host + str(port)).encode("utf-8")).hexdigest()

        connectednodes_db.set(
            node_id, node_list) if self.CONNECTED_NODES_PATH is None else KOT(
                "connectednodes" + self.CONNECTED_NODES_PATH,
                folder=get_config()["main_folder"] + "/db",
            ).set(node_id, node_list)

    @staticmethod
    def connectionfrommixdb(custom_server=None,
                            custom_CONNECTED_NODES_PATH=None):
        """
        Connects to the mixdb.
        """
        the_server = server.Server if custom_server is None else custom_server
        the_CONNECTED_NODES_PATH = (the_server.CONNECTED_NODES_PATH
                                    if custom_CONNECTED_NODES_PATH is None else
                                    custom_CONNECTED_NODES_PATH)
        node_list = the_server.get_connected_nodes(
            custom_CONNECTED_NODES_PATH=the_CONNECTED_NODES_PATH)
        for element in node_list:
            with contextlib.suppress(Exception):
                the_server.connect(
                    node_list[element]["host"],
                    node_list[element]["port"],
                )

    def connected_node_delete(self, node):
        """
        Deletes a connected node.
        """

        node_id = sha256((node["id"] + node["host"] +
                          str(node["port"])).encode("utf-8")).hexdigest()
        connectednodes_db.delete(
            node_id) if self.CONNECTED_NODES_PATH is None else KOT(
                "connectednodes" + self.CONNECTED_NODES_PATH,
                folder=get_config()["main_folder"] + "/db",
            ).delete(node_id)

    def direct_message(self, node, data, hash_of_data):
        if "sendmefullblock" == data["action"]:
            self.send_block_to_other_nodes(node, hash_of_data=hash_of_data)

        if "fullblock" == data["action"]:
            self.get_full_chain(data, node, hash_of_data=hash_of_data)

        if "fullaccounts" == data["action"]:
            self.get_full_accounts(data, node, hash_of_data=hash_of_data)

        if "fullblockshash" == data["action"]:
            self.get_full_blockshash(data, node, hash_of_data=hash_of_data)

        if "fullblockshash_part" == data["action"]:
            self.get_full_blockshash_part(data,
                                          node,
                                          hash_of_data=hash_of_data)

        if "transactionrequest" == data["action"]:
            self.get_transaction(data, node, hash_of_data=hash_of_data)

        if "myblock" == data["action"]:
            self.get_candidate_block(data, node, hash_of_data=hash_of_data)

        if "myblockhash" == data["action"]:
            self.get_candidate_block_hash(data,
                                          node,
                                          hash_of_data=hash_of_data)

    def send_me_full_block(self, node=None):
        the_node = node
        choices = []
        if the_node is None:
            for i in self.clients:
                if i.c_type == 2:
                    choices.append(i)
            the_node = random.choice(choices)

        self.logger.info(
            f"Sending sendmefullblock to {the_node.id}:{the_node.host}:{the_node.port}"
        )
        self.send_client(the_node, {"action": "sendmefullblock"}, c_type=2)

    def send_my_block(self, block: Block):
        self.logger.info(f"Sending my block to all nodes")
        system = self_candidates(block)[0]

        

        new_list = []

        signature_list = []

        for element in system.validating_list:
            tx_json = element.dump_json()
            new_list.append(tx_json)
            signature_list.append(element.signature)

        first_element = [new_list[0]] if len(new_list) > 0 else []

        data = {
            "action": "myblock",
            "transaction": first_element,
            "total_length": len(new_list),
            "sequence_number":
            system.sequence_number+system.empty_block_number,
            "adding": False,
        }

        self.send(data)
        time.sleep(2)

        if len(new_list) > 1:
            for element in new_list[1:]:
                data = {
                    "action": "myblock",
                    "transaction": [element],
                    "total_length": len(new_list),
                    "sequence_number":
                    system.sequence_number+system.empty_block_number,
                    "adding": True,
                }

                self.send(data)


    def send_my_block_hash(self, block):
        self.logger.info(f"Sending my block hash to all nodes")
         
        system = self_candidates(block)[1]

        data = {
            "action": "myblockhash",
            "hash": system.hash,
            "previous_hash": system.previous_hash,
            "sequence_number":
            system.sequence_number+system.empty_block_number,
        }

        self.send(data, c_type=3)

    def get_candidate_block(self, data, node: client, hash_of_data=""):
        self.logger.info(f"Getting candidate block with {hash_of_data}")
        self.logger.debug(
            f"Getting candidate block from {node.id}:{node.host}:{node.port}")
        if node.candidate_block is None:
            node.candidate_block = data
            return
        if data["sequence_number"] > node.candidate_block["sequence_number"]:
            self.logger.debug("Candidate block is updated directly")
            if len(node.candidate_block_history) >= 5:
                node.candidate_block_history.pop(0)

            node.candidate_block_history.append(copy.copy(
                node.candidate_block))
            node.candidate_block = data
        else:
            self.logger.debug("Candidate block is not updated directly")
            if node.candidate_block["total_length"] <= data["total_length"]:
                if node.candidate_block["total_length"] == data[
                        "total_length"]:
                    if data["adding"]:
                        control = True
                        for i in node.candidate_block["transaction"]:
                            if i["signature"] == data["transaction"][0]["signature"]:
                                control = False
                        if control:
                            node.candidate_block["transaction"].append(data["transaction"][0])

                else:
                    node.candidate_block = data

    def get_candidate_block_hash(self, data, node: client, hash_of_data=""):
        self.logger.info(f"Getting candidate block hash with {hash_of_data}")
        if node.candidate_block_hash is None:
            node.candidate_block_hash = data
            return

        data["sender"] = node.id

        if data["sequence_number"] > node.candidate_block_hash[
                "sequence_number"]:
            if len(node.candidate_block_hash_history) >= 5:
                node.candidate_block_hash_history.pop(0)

            node.candidate_block_hash_history.append(
                copy.copy(node.candidate_block_hash))
            node.candidate_block_hash = data
        else:
            #if len(node.candidate_block_hash["hash"]) <= len(data["hash"]):
            node.candidate_block_hash = data

    def send_full_chain(self, node=None):
        log_text = ("Sending full chain" if node is None else
                    f"Sending full chain to {node.id}:{node.host}:{node.port}")
        self.logger.info(log_text)
        file = open(self.TEMP_BLOCK_PATH, "rb")
        SendData = file.read(1024)
        while SendData:
            data = {
                "action": "fullblock",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }
            if node is None:
                self.send(data, c_type=2)
            else:
                self.send_client(node, data, c_type=2)

            SendData = file.read(1024)

            if not SendData:
                data = {
                    "action": "fullblock",
                    "byte": "end",
                }
                if node is None:
                    self.send(data, c_type=2)
                else:
                    self.send_client(node, data, c_type=2)

    def send_full_accounts(self, node=None):
        the_TEMP_ACCOUNTS_PATH = self.TEMP_ACCOUNTS_PATH
        file = open(the_TEMP_ACCOUNTS_PATH, "rb")
        SendData = file.read(1024)
        while SendData:
            data = {
                "action": "fullaccounts",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }

            if node is None:
                self.send(data, c_type=2)
            else:
                self.send_client(node, data, c_type=2)

            SendData = file.read(1024)
            if not SendData:
                data = {"action": "fullaccounts", "byte": "end"}
                if node is None:
                    self.send(data, c_type=2)
                else:
                    self.send_client(node, data, c_type=2)

    def send_full_blockshash(self, node=None):
        the_TEMP_BLOCKSHASH_PATH = self.TEMP_BLOCKSHASH_PATH
        file = open(the_TEMP_BLOCKSHASH_PATH, "rb")
        SendData = file.read(1024)
        while SendData:
            data = {
                "action": "fullblockshash",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }
            if node is None:
                self.send(data, c_type=2)
            else:
                self.send_client(node, data, c_type=2)

            SendData = file.read(1024)

            if not SendData:
                data = {"action": "fullblockshash", "byte": "end"}
                if node is None:
                    self.send(data, c_type=2)
                else:
                    self.send_client(node, data, c_type=2)

    def send_full_blockshash_part(self, node=None):
        the_TEMP_BLOCKSHASH_PART_PATH = self.TEMP_BLOCKSHASH_PART_PATH
        file = open(the_TEMP_BLOCKSHASH_PART_PATH, "rb")
        SendData = file.read(1024)
        while SendData:
            data = {
                "action": "fullblockshash_part",
                "byte": (SendData.decode(encoding="iso-8859-1")),
            }
            if node is None:
                self.send(data, c_type=2)
            else:
                self.send_client(node, data, c_type=2)

            SendData = file.read(1024)

            if not SendData:
                data = {"action": "fullblockshash_part", "byte": "end"}
                if node is None:
                    self.send(data, c_type=2)
                else:
                    self.send_client(node, data, c_type=2)

    def get_full_chain(self, data, node, hash_of_data=""):
        self.logger.info(f"Getting full chain with {hash_of_data}")
        get_ok = False

        if not os.path.exists(self.TEMP_BLOCK_PATH):
            get_ok = True
        else:
            system = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH, reset=self.custom_variables)
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            if str(data["byte"]) == "end":
                move(self.LOADING_BLOCK_PATH, self.TEMP_BLOCK_PATH)

                from naruno.consensus.consensus_main import consensus_trigger
                from naruno.lib.perpetualtimer import perpetualTimer

                system = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH,
                                  get_normal_block=True, reset=self.custom_variables)

                ChangeTransactionFee(system)

                perpetualTimer(system.consensus_timer, consensus_trigger, the_consensus=True)
                SaveBlock(
                    system,
                    custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH,
                    custom_TEMP_ACCOUNTS_PATH=self.TEMP_ACCOUNTS_PATH,
                    custom_TEMP_BLOCKSHASH_PATH=self.TEMP_BLOCKSHASH_PATH,
                    custom_TEMP_BLOCKSHASH_PART_PATH=self.
                    TEMP_BLOCKSHASH_PART_PATH,
                )

            else:
                os.chdir(get_config()["main_folder"])
                file = open(self.LOADING_BLOCK_PATH, "ab")

                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    def get_full_blockshash(self, data, node, hash_of_data=""):
        self.logger.info(f"Getting full blockshash with {hash_of_data}")
        the_TEMP_BLOCKSHASH_PATH = self.TEMP_BLOCKSHASH_PATH
        get_ok = False

        if not os.path.exists(the_TEMP_BLOCKSHASH_PATH):
            get_ok = True
        else:
            system = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH, reset=self.custom_variables)
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            if str(data["byte"]) == "end":
                blockshash_db.set("blockshash", None)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(the_TEMP_BLOCKSHASH_PATH)
                move(self.LOADING_BLOCKSHASH_PATH, the_TEMP_BLOCKSHASH_PATH)
            else:
                os.chdir(get_config()["main_folder"])
                file = open(self.LOADING_BLOCKSHASH_PATH, "ab")
                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    def get_full_blockshash_part(self, data, node, hash_of_data=""):
        self.logger.info(f"Getting full blockshash part with {hash_of_data}")
        the_TEMP_BLOCKSHASH_PART_PATH = self.TEMP_BLOCKSHASH_PART_PATH
        get_ok = False

        if not os.path.exists(the_TEMP_BLOCKSHASH_PART_PATH):
            get_ok = True
        else:
            system = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH, reset=self.custom_variables)
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            if str(data["byte"]) == "end":
                blockshash_db.set("blockshash_part", None)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(the_TEMP_BLOCKSHASH_PART_PATH)
                move(self.LOADING_BLOCKSHASH_PART_PATH,
                     the_TEMP_BLOCKSHASH_PART_PATH)
            else:
                os.chdir(get_config()["main_folder"])
                file = open(self.LOADING_BLOCKSHASH_PART_PATH, "ab")
                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    def get_full_accounts(self, data, node, hash_of_data=""):
        self.logger.info(f"Getting full accounts with {hash_of_data}")
        the_TEMP_ACCOUNTS_PATH = self.TEMP_ACCOUNTS_PATH
        the_LOADING_ACCOUNTS_PATH = self.LOADING_ACCOUNTS_PATH
        get_ok = False

        if not os.path.exists(the_TEMP_ACCOUNTS_PATH):
            get_ok = True
        else:
            system = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH, reset=self.custom_variables)
            if node.id == system.dowload_true_block:
                get_ok = True

        if get_ok:
            if str(data["byte"]) == "end":
                accounts_db.set("accounts", None)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(the_TEMP_ACCOUNTS_PATH)
                move(the_LOADING_ACCOUNTS_PATH, the_TEMP_ACCOUNTS_PATH)
            else:
                os.chdir(get_config()["main_folder"])
                file = open(the_LOADING_ACCOUNTS_PATH, "ab")
                file.write((data["byte"].encode(encoding="iso-8859-1")))
                file.close()

    @staticmethod
    def send_transaction(
        tx,
        custom_current_time=None,
        custom_sequence_number=None,
        custom_balance=None,
        except_client=None,
        custom_server=None,
    ):
        """
        Sends the given transaction to UNL nodes.
        """
        if not tx.signature == "NARUNO":
            data = {
                "action": "transactionrequest",
                "sequence_number": tx.sequence_number,
                "txsignature": tx.signature,
                "fromUser": tx.fromUser,
                "to_user": tx.toUser,
                "data": tx.data,
                "amount": tx.amount,
                "transaction_fee": tx.transaction_fee,
                "transaction_time": tx.transaction_time,
                "custom_current_time": custom_current_time,
                "custom_sequence_number": custom_sequence_number,
                "custom_balance": custom_balance,
            }
            the_server = server.Server if custom_server is None else custom_server
            the_server.send(data, except_client=except_client, c_type=1)

    def get_transaction(self, data, node, hash_of_data=""):
        self.logger.info(f"Getting transaction with {hash_of_data}")
        if self not in naruno.node.server.server.tx_signature_list:
            naruno.node.server.server.tx_signature_list[self] = []

        if data["txsignature"] in naruno.node.server.server.tx_signature_list[self]:
            self.logger.debug("Transaction is already getted")
            return

        naruno.node.server.server.tx_signature_list[self].append(data["txsignature"])
        
        the_transaction = Transaction(
            data["sequence_number"],
            data["txsignature"],
            data["fromUser"],
            data["to_user"],
            data["data"],
            data["amount"],
            data["transaction_fee"],
            data["transaction_time"],
        )
        block = GetBlock(custom_TEMP_BLOCK_PATH=self.TEMP_BLOCK_PATH, reset=self.custom_variables)
        custom_current_time = None
        custom_sequence_number = None
        custom_balance = None
        if self.custom_variables:
            custom_current_time = data["custom_current_time"]
            custom_sequence_number = data["custom_sequence_number"]
            custom_balance = data["custom_balance"]

        GetTransaction(
                block,
                the_transaction,
                custom_current_time=custom_current_time,
                custom_sequence_number=custom_sequence_number,
                custom_balance=custom_balance,
                custom_PENDING_TRANSACTIONS_PATH=self.
                PENDING_TRANSACTIONS_PATH,
                except_client=node,
                custom_server=self)
        
    def send_block_to_other_nodes(self,
                                  node=None,
                                  sync=False,
                                  hash_of_data=""):
        """
        Sends the block to the other nodes.
        """
        self.logger.info(f"Sending block to other nodes with {hash_of_data}")
        if node is None or sync:
            self.logger.info("Sync process started")
            self.send_full_accounts(node=node)
            self.send_full_blockshash(node=node)
            self.send_full_blockshash_part(node=node)
            self.send_full_chain(node=node)
        else:
            self.logger.info("Node appended to sync_clients")
            self.sync_clients.append(node)

    def get_ip(self):
        """
        Returns the IP address of the socket in this class.
        """
        ip = self.sock.getsockname()[0]
        return ip
