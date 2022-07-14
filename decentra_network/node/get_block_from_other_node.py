#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def GetBlockFromOtherNode():
    """
    Receive the block from the other node.
    """

    from decentra_network.node.server.server import server
    from decentra_network.node.unl import Unl

    node = server.Server
    unl_list = Unl.get_as_node_type(Unl.get_unl_nodes())
    node.send_node(unl_list[0], {"action":"sendmefullblock"})
