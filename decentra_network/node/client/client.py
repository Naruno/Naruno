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

class client(Thread):
    def __init__(self, socket, address, node_id, server):
        Thread.__init__(self)
        self.server = server
        self.socket = socket
        self.host = address[0]
        self.port = address[1]
        self.id = node_id
        self.candidate_block = None
        self.candidate_block_hash = None

        self.running = True

        self.start()

    def run(self):
        self.socket.settimeout(10.0)        
        while self.running:
            with contextlib.suppress(socket.timeout):
                data = self.socket.recv(1024)
                data = json.loads(data.decode("utf-8"))
                if self.server.check_message(data):
                    self.server.messages.append(data)
                    self.server.get_message(self, data)
            time.sleep(0.01)
        self.socket.settimeout(None)
        self.socket.close()

    def stop(self):
        self.running = False
