#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from node.myownp2pn import mynode, connectionfrommixdb
from wallet.wallet import Wallet_Import

from config import *


def ndstart(ip, port):
    """
    Starts the node server.
    """

    node = mynode(ip, port)
    node.start()
    return node


def ndstop():
    """
    Stops the node server
    """

    mynode.main_node.stop()


def ndconnect(ip, port):
    """
    Connects to a node.
    """

    mynode.main_node.connect_to_node(ip, port)


def ndconnectmixdb():
    """
    Connects to nodes from mixdb.
    """

    connectionfrommixdb()


def ndid():
    """
    Returns the our node id.
    """

    return "".join(
        [
            l.strip()
            for l in Wallet_Import(0, 0).splitlines()
            if l and not l.startswith("-----")
        ]
    )
