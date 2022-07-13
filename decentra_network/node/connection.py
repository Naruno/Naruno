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


from decentra_network.config import *
from decentra_network.lib.log import get_logger
from decentra_network.node.unl import Unl

logger = get_logger("NODE")


class Connection(threading.Thread):
    def __init__(self, main_node, sock, node_id, host, port, save_messages=False):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.status = True

        self.id = node_id

        self.candidate_block = None
        self.candidate_block_hash = None

        self.save_messages = save_messages
        self.messages = []

        self.EOT_CHAR = 0x04.to_bytes(1, "big")

    def send(self, data, encoding_type="utf-8"):
        json_data = json.dumps(data)
        json_data = json_data.encode(encoding_type) + self.EOT_CHAR
        self.sock.sendall(json_data)


    def stop(self):
        self.status = False

    def run(self):
        self.sock.settimeout(10.0)
        buffer = b""

        while self.status:
            chunk = b""

            try:
                chunk = self.sock.recv(4096)

            except socket.timeout:
                logger.exception("Node System: Connection: timeout")

            if chunk != b"":
                buffer += chunk
                eot_pos = buffer.find(self.EOT_CHAR)

                while eot_pos > 0:
                    packet = buffer[:eot_pos]
                    buffer = buffer[eot_pos + 1 :]
                    message = json.loads(packet)
                    if self.save_messages:
                        self.messages.append(message)
                    self.main_node.message_from_node(self, message)

                    eot_pos = buffer.find(self.EOT_CHAR)

            time.sleep(0.01)

        self.sock.settimeout(None)
        self.sock.close()
        self.main_node.delete_closed_connections()
        logger.info("Node System: Connection: Stopped")
