#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import os

from lib.config_system import get_config

from config import TEMP_BLOCK_PATH


def GetBlock():
    """
    Returns the block.
    """

    os.chdir(get_config()["main_folder"])
    with open(TEMP_BLOCK_PATH, 'rb') as block_file:
        return pickle.load(block_file)


def GetBlockFromOtherNode():
    """
    Receive the block from the other node.
    """

    from node.myownp2pn import mynode
    from node.unl import get_unl_nodes, get_as_node_type

    node = mynode.main_node
    unl_list = get_as_node_type(get_unl_nodes())
    node.send_data_to_node(unl_list[0], "sendmefullblock")
