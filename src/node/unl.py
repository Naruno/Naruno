#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import time

from config import *
from lib.config_system import get_config


class Unl:

    @staticmethod
    def save_new_unl_node(id):
        """
        Saves the new unl.
        """

        nodes_list = Unl.get_unl_nodes()

        already_in_list = False

        for element in nodes_list:
            if element == id:
                already_in_list = True

        if not already_in_list:

            nodes_list[id] = {}
            nodes_list[id]["date"] = time.time()

            os.chdir(get_config()["main_folder"])
            with open(UNL_NODES_PATH, "w") as unl_nodes_file:
                json.dump(nodes_list, unl_nodes_file, indent=4)

    @staticmethod
    def get_unl_nodes():
        """
        Returns the UNL nodes list from UNL_NODES_PATH.
        """

        if not os.path.exists(UNL_NODES_PATH):
            return {}

        os.chdir(get_config()["main_folder"])
        with open(UNL_NODES_PATH, "rb") as unl_nodes_file:
            return json.load(unl_nodes_file)

    @staticmethod
    def get_as_node_type(id_list):
        """
        Converts the UNL node list to Node class.
        """

        from node.node import Node

        temp_list = []
        if Node.main_node is not None:
            for list_node in id_list:
                for each_node in (Node.main_node.nodes_inbound +
                                  Node.main_node.nodes_outbound):
                    if list_node == each_node.id:
                        temp_list.append(each_node)

        return temp_list

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
