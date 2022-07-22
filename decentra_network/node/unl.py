#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import itertools
import json
import os
import time

from decentra_network.config import *
from decentra_network.lib.config_system import get_config


class Unl:

    @staticmethod
    def save_new_unl_node(node_id):
        """
        Saves the new unl.
        """

        nodes_list = Unl.get_unl_nodes()

        already_in_list = any(element == node_id for element in nodes_list)
        if not already_in_list:

            nodes_list[node_id] = {}
            nodes_list[node_id]["date"] = time.time()

            os.chdir(get_config()["main_folder"])
            with open(UNL_NODES_PATH, "w") as unl_nodes_file:
                json.dump(nodes_list, unl_nodes_file, indent=4)

    @staticmethod
    def get_unl_nodes(custom_UNL_NODES_PATH=None):
        """
        Returns the UNL nodes list from UNL_NODES_PATH.
        """

        the_UNL_NODES_PATH = (UNL_NODES_PATH if custom_UNL_NODES_PATH is None
                              else custom_UNL_NODES_PATH)

        if not os.path.exists(the_UNL_NODES_PATH):
            return {}

        os.chdir(get_config()["main_folder"])
        with open(the_UNL_NODES_PATH, "r") as unl_nodes_file:
            return json.load(unl_nodes_file)

    @staticmethod
    def get_as_node_type(id_list):
        """
        Converts the UNL node list to Node class.
        """

        from decentra_network.node.server.server import server

        nodes = [] if server.Server is None else server.Server.clients
        return nodes

    @staticmethod
    def node_is_unl(node_id):
        """
        Returns the this node is unl or not.
        """

        for unl in Unl.get_unl_nodes():
            temp_unl = unl
            if node_id == temp_unl:
                return True
        return False

    @staticmethod
    def unl_node_delete(node_id):
        """
        Deletes the UNL node
        """

        saved_nodes = Unl.get_unl_nodes()
        if node_id in saved_nodes:
            del saved_nodes[node_id]

            os.chdir(get_config()["main_folder"])
            with open(UNL_NODES_PATH, "w") as connected_node_file:
                json.dump(saved_nodes, connected_node_file, indent=4)
