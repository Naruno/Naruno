#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from threading import Thread
import socket
import time
import json
import contextlib
from decentra_network.lib.log import get_logger

logger = get_logger("NODE")

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

        self.running = True
        if not test:
            self.start()

    def run(self):
        self.socket.settimeout(10.0)        
        while self.running:
            with contextlib.suppress(socket.timeout):
                data = self.socket.recv(1024)
                logger.info("Received data from %s:%s: %s" % (self.host, self.port, data))
                data = data.decode("utf-8")
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    logger.error("Error decoding JSON data: %s" % data)
                if self.server.check_message(data):
                    self.server.messages.append(data)
                    self.server.get_message(self, data)
            time.sleep(0.01)
        self.socket.settimeout(None)
        self.socket.close()

    def stop(self):
        self.running = False
