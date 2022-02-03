#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from lib.mixlib import dprint

from node.unl import get_as_node_type, get_unl_nodes
from node.myownp2pn import mynode

from blockchain.candidate_block.get_candidate_blocks import GetCandidateBlocks


def consensus_round_2(block):
    """
    At this stage of the consensus process,
    The blocks (block hashes) of our and the
    unl nodes are compared and the block accepted
    by 80 percent is approved.

    Inputs:
      * block: The block (class) we want consensus
      round 2 to be done
    """

    unl_nodes = get_unl_nodes()
    if not block.raund_2_node:
        dprint("Raund 2: in get candidate block hashes\n")

        mynode.main_node.send_my_block_hash(get_as_node_type(unl_nodes))
        block.raund_2_node = True
        block.save_block()

    candidate_class = GetCandidateBlocks()
    dprint("Raund 2 Conditions")
    dprint(len(candidate_class.candidate_block_hashes) > ((len(unl_nodes) * 80) / 100))
    dprint((int(time.time()) - block.raund_2_starting_time) < block.raund_2_time)

    if len(candidate_class.candidate_block_hashes) > ((len(unl_nodes) * 80) / 100):

        if not (int(time.time()) - block.raund_2_starting_time) < block.raund_2_time:
            dprint("Raund 2: first ok")
            for candidate_block in candidate_class.candidate_block_hashes[:]:
                tx_valid = 0

                if block.hash == candidate_block["hash"]:
                    tx_valid += 1

                for other_block in candidate_class.candidate_block_hashes[:]:

                    if candidate_block != other_block:
                        if candidate_block["hash"] == other_block["hash"]:
                            tx_valid += 1

                if tx_valid > ((len(unl_nodes) * 80) / 100):

                    dprint("Raund 2: second ok")
                    if block.hash == candidate_block["hash"]:
                        block.validated = True
                        block.validated_time = int(time.time())
                        block.raund_2 = True

                    else:
                        print("Raund 2: my block is not valid")
                        node = mynode.main_node
                        unl_list = get_as_node_type([candidate_block["sender"]])
                        node.send_data_to_node(unl_list[0], "sendmefullblock")
                        block.dowload_true_block = candidate_block["sender"]
                    block.save_block()

        else:
            if not block.decrease_the_time_2 == 3:
                block.decrease_the_time_2 += 1
                block.increase_the_time_2 = 0
                block.save_block()

    else:
        if not (int(time.time()) - block.raund_2_starting_time) < block.raund_2_time:
            if not block.increase_the_time_2 == 3:
                block.increase_the_time_2 += 1
                block.decrease_the_time_2 = 0
                block.save_block()
