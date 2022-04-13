#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import pickle

from config import TEMP_BLOCK_PATH
from lib.config_system import get_config


def GetBlock():
    """
    Returns the block.
    """

    os.chdir(get_config()["main_folder"])
    with open(TEMP_BLOCK_PATH, "rb") as block_file:
        return pickle.load(block_file)


def GetBlockFromOtherNode():
    """
    Receive the block from the other node.
    """

    from node.node import Node
    from node.unl import Unl

    node = Node.main_node
    unl_list = Unl.get_as_node_type(Unl.get_unl_nodes())
    node.send_data_to_node(unl_list[0], "sendmefullblock")
