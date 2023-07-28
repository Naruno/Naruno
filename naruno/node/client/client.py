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
import traceback

from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger



class client(Thread):

    def __init__(self, socket, address, node_id, server, test=False,c_type=0):
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


        a_block = Block("onur")
        self.logger.debug(f"Block max_data_size: {a_block.max_data_size}")
        self.logger.debug(f"Block max_tx_number: {a_block.max_tx_number}")        
        buffer_size = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 1.5)
        buffer_size_2 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 1.5)
        buffer_size_3 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 5)  
        buffer_size_4 = 6525 + int(
            (a_block.max_data_size // a_block.max_tx_number) * 0.5)  

        self.c_type = c_type
        if self.c_type == 0:
            self.buffer_size = buffer_size
        elif self.c_type == 1:
            self.buffer_size = buffer_size_2          
        elif self.c_type == 2:
            self.buffer_size = buffer_size_3   
        elif self.c_type == 3:
            self.buffer_size = buffer_size_4


        self.logger.info(f"Connection established with {self.id}")



        self.logger.debug("Test mode: " + str(test))
        self.logger.debug("Buffer size: " + str(self.buffer_size))

        self.running = True
        if not test:
            self.start()


    def threaded_receive(self, data):
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
                    traceback.print_exc()
                    self.logger.error(f"Error while processing data: {e}")
                    self.logger.error(f"Data: {data}")

    def run(self):
        self.socket.settimeout(10.0)
        while self.running:
            with contextlib.suppress(socket.timeout):
                data = self.socket.recv(self.buffer_size)

                if not data:
                    break

                Thread(target=self.threaded_receive, args=(data,)).start()

            time.sleep(0.01)

    def stop(self):
        self.running = False
        self.socket.close()
