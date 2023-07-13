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

from naruno.config import UNL_NODES_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT

unl_db = KOT("unl", folder=get_config()["main_folder"] + "/db")


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

            unl_db.set("unl", nodes_list)

    @staticmethod
    def get_unl_nodes(custom_UNL_NODES_PATH=None):
        """
        Returns the UNL nodes list from UNL_NODES_PATH.
        """

        record = (unl_db.get("unl") if custom_UNL_NODES_PATH is None else KOT(
            "unl" + custom_UNL_NODES_PATH,
            folder=get_config()["main_folder"] + "/db",
        ).get("unl"))
        return record if record is not None else {}

    @staticmethod
    def get_as_node_type(id_list, c_type=0):
        """
        Converts the UNL node list to Node class.
        """

        from naruno.node.server.server import server
        nodes = []
        if server.Server is not None:
         for i in server.Server.clients:
            if i.c_type == c_type:
                nodes.append(i)
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

            unl_db.set("unl", saved_nodes)
