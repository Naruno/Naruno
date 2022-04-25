#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from blockchain.block.get_block import GetBlock
from node.unl import Unl
from transactions.get_my_transaction import GetMyTransaction


def Status():
    """
    Returns the status of the network.
    """

    first_block = GetBlock()
    start_time = time.time()
    while True:
        time.sleep(5)
        new_time = time.time()
        new_block = GetBlock()
        difference = int(new_time - start_time)

        status_json = {
            "status":
            "",
            "first_block":
            str(first_block.__dict__),
            "new_block":
            str(new_block.__dict__),
            "last_transaction_of_block":
            str(new_block.validating_list[-1])
            if len(new_block.validating_list) > 0 else "",
            "last_transaction_of_us":
            str([i.__dict__ for i in GetMyTransaction()]),
            "connected_nodes": [
                str(the_connections) for the_connections in
                Unl.get_as_node_type(Unl.get_unl_nodes())
            ],
        }

        if not (first_block.sequance_number +
                first_block.empty_block_number) == (
                    new_block.sequance_number + new_block.empty_block_number):
            if difference <= 6:
                status_json["status"] = "Good"
            elif difference <= 10:
                status_json["status"] = "Not bad"
            elif difference <= 20:
                status_json["status"] = "Bad"
            elif difference >= 20:
                status_json["status"] = "Very bad"
        else:
            if difference >= 20:
                status_json["status"] = "Not work"

        return status_json
