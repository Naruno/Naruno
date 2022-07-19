#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import re
import socket
import time
from posixpath import split
from threading import Thread

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
                data = self.socket.recv(4096)
                logger.info(
                    f"NODE:{self.server.host}:{self.server.port} SOCK:{self.host}:{self.port} Received data {data}"
                )
                data = data.decode("utf-8")
                try:
                    data = json.loads(data.replace("\'", "\""))
                    self.server.get_message(self, data)
                except json.JSONDecodeError:
                    splited_data = re.split(r"(?<=})\B(?={)", data)
                    for i in splited_data:
                        self.server.get_message(self, json.loads(i.replace("\'", "\"")))

            time.sleep(0.01)

    def stop(self):
        self.running = False
        self.socket.close()
