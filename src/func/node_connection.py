#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from node.myownp2pn import mynode, connectionfrommixdb
from lib.settings_system import the_settings

from config import *

def ndstart(ip, port):
    node = mynode(ip, port)
    # node.debug = the_settings()["debug_mode"]
    node.start()
    return node


def ndstop():
    mynode.main_node.stop()


def ndconnect(ip, port):
    mynode.main_node.connect_to_node(ip, port)


def ndconnectmixdb():
    connectionfrommixdb()


def connect_to_main_network():
    import urllib.request
    urllib.request.urlretrieve('https://raw.githubusercontent.com/onuratakan/Decentra-Network/master/connected_node.decentra_network', CONNECTED_NODE_PATH)

    ndconnectmixdb()
