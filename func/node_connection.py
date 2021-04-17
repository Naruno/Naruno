#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
