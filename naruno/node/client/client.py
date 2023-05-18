#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import socket
import time
from hashlib import md5
from threading import Thread

from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger

a_block = Block("onur")
buffer_size = 6525 + int(
    (a_block.max_data_size // a_block.max_tx_number) * 1.5)


class client(Thread):

    def __init__(self, socket, address, node_id, server, test=False):
        Thread.__init__(self)
        self.server = server
        self.socket = socket
        self.host = address[0]
        self.port = address[1]
        self.id = node_id
        self.candidate_block = None
        self.candidate_block_hash = None
        self.candidate_block_history = []
        self.candidate_block_hash_history = []

        self.logger = get_logger(
            f"NODE_{self.server.host}_{self.server.port}_SOCK_{self.host}_{self.port}"
        )

        self.logger.info(f"Connection established with {self.id}")

        self.logger.debug("Test mode: " + str(test))
        self.logger.debug("Buffer size: " + str(buffer_size))

        self.running = True
        if not test:
            self.start()

    def run(self):
        self.socket.settimeout(10.0)
        while self.running:
            with contextlib.suppress(socket.timeout):
                data = self.socket.recv(buffer_size)

                if not data:
                    break

                data = data.decode("utf-8")
                with contextlib.suppress(json.decoder.JSONDecodeError):
                    data = json.loads(data)
                with contextlib.suppress(Exception):
                    del data["buffer"]
                try:
                    hash_of_data = md5(str(data).encode()).hexdigest()[:6]
                    self.logger.debug(
                        f"Received data ({hash_of_data}): {data}")
                    self.server.get_message(self, data, hash_of_data)
                except Exception as e:
                    self.logger.error(f"Error while processing data: {e}")
                    self.logger.error(f"Data: {data}")

            time.sleep(0.01)

    def stop(self):
        self.running = False
        self.socket.close()
