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

from config import *
from lib.log import get_logger
from node.unl import Unl

logger = get_logger("NODE")


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

        self.EOT_CHAR = 0x04.to_bytes(1, "big")

        from node.node import Node

        Node.save_connected_node(host, port, id)

    def send(self, data, encoding_type="utf-8"):

        if isinstance(data, str):
            self.sock.sendall(data.encode(encoding_type) + self.EOT_CHAR)

        elif isinstance(data, dict):
            try:
                json_data = json.dumps(data)
                json_data = json_data.encode(encoding_type) + self.EOT_CHAR
                self.sock.sendall(json_data)

            except TypeError as type_error:
                logger.exception(type_error)

            except Exception as e:
                logger.exception(e)

        elif isinstance(data, bytes):
            bin_data = data + self.EOT_CHAR
            self.sock.sendall(bin_data)

        else:
            logger.warning(
                "Node System: Node System: Datatype used is not valid please use str, dict (will be send as json) or bytes"
            )

    def stop(self):
        self.terminate_flag.set()

    def parse_packet(self, packet):
        try:
            packet_decoded = packet.decode("utf-8")

            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                return packet_decoded

        except UnicodeDecodeError:
            return packet

    def run(self):
        self.sock.settimeout(10.0)
        buffer = b""

        while not self.terminate_flag.is_set():
            chunk = b""

            try:
                chunk = self.sock.recv(4096)

            except socket.timeout:
                logger.exception("Node System: Node_Connection: timeout")

            except Exception as e:
                self.terminate_flag.set()
                logger.exception(e)

            # BUG: possible buffer overflow when no EOT_CHAR is found => Fix by max buffer count or so?
            if chunk != b"":
                buffer += chunk
                eot_pos = buffer.find(self.EOT_CHAR)

                while eot_pos > 0:
                    packet = buffer[:eot_pos]
                    buffer = buffer[eot_pos + 1:]

                    self.main_node.message_from_node(self,
                                                     self.parse_packet(packet))

                    eot_pos = buffer.find(self.EOT_CHAR)

            time.sleep(0.01)

        # IDEA: Invoke (event) a method in main_node so the user is able to send a bye message to the node before it is closed?

        self.sock.settimeout(None)
        self.sock.close()
        logger.info("Node System: Node_Connection: Stopped")

    @staticmethod
    def connect(ip, port):
        """
        Connects to a node.
        """
        from node.node import Node

        Node.main_node.connect_to_node(ip, port)

    @staticmethod
    def connectmixdb():
        """
        Connects to nodes from mixdb.
        """
        from node.node import Node

        Node.connectionfrommixdb()

    def __str__(self):
        return f"Node Connection: {self.host}:{self.port} ({self.id})"
