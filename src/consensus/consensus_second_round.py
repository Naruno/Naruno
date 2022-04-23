#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from blockchain.candidate_block.get_candidate_blocks import GetCandidateBlocks
from lib.log import get_logger
from node.node import Node
from node.unl import Unl

logger = get_logger("CONSENSUS_SECOND_ROUND")


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

    logger.info(
        "BLOCK#{block.sequance_number}:{block.empty_block_number} Second round is starting"
    )

    unl_nodes = Unl.get_unl_nodes()
    if not block.raund_2_node:

        Node.main_node.send_my_block_hash(Unl.get_as_node_type(unl_nodes))
        block.raund_2_node = True
        block.save_block()

    candidate_class = GetCandidateBlocks()

    if len(candidate_class.candidate_block_hashes) > (
        (len(unl_nodes) * 80) / 100):
        logger.info("Enough candidate block hashes received")

        if not (int(time.time()) -
                block.raund_2_starting_time) < block.raund_2_time:
            logger.info("True time")

            for candidate_block in candidate_class.candidate_block_hashes[:]:
                logger.debug(f"Candidate block hash {candidate_block}")

                tx_valid = 0

                if block.hash == candidate_block["hash"]:
                    tx_valid += 1

                for other_block in candidate_class.candidate_block_hashes[:]:

                    if candidate_block != other_block:
                        if candidate_block["hash"] == other_block["hash"]:
                            tx_valid += 1

                logger.debug(f"Hash valid of  {candidate_block} : {tx_valid}")
                if tx_valid > ((len(unl_nodes) * 80) / 100):

                    if block.hash == candidate_block["hash"]:
                        logger.info("Block approved")
                        block.validated = True
                        block.validated_time = int(time.time())
                        block.raund_2 = True

                    else:
                        sender = candidate_block["sender"]
                        logger.warning(
                            f"Our block is not valid, the system will try to get true block from node {sender}"
                        )
                        node = Node.main_node
                        unl_list = Unl.get_as_node_type([sender])
                        node.send_data_to_node(unl_list[0], "sendmefullblock")
                        block.dowload_true_block = sender
                    block.save_block()

        else:
            if not block.decrease_the_time_2 == 3:
                logger.info("Decrease the time")
                block.decrease_the_time_2 += 1
                block.increase_the_time_2 = 0
                block.save_block()

    else:
        if not (int(time.time()) -
                block.raund_2_starting_time) < block.raund_2_time:
            if not block.increase_the_time_2 == 3:
                logger.info("Increase the time")
                block.increase_the_time_2 += 1
                block.decrease_the_time_2 = 0
                block.save_block()

    logger.info("Second round is done")
