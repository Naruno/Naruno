#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.lib.log import get_logger
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl

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
        f"BLOCK#{block.sequance_number}:{block.empty_block_number} Second round is starting"
    )

    unl_nodes = Unl.get_unl_nodes()
    logger.info("Our block hash is sending to the unl nodes")
    server.Server.send_my_block_hash(block)

    candidate_class = GetCandidateBlocks()

    time_difference = int(time.time()) - block.raund_2_starting_time

    if len(candidate_class.candidate_block_hashes) > ((len(unl_nodes) * 80) / 100):
        logger.info("Enough candidate block hashes received")

        if time_difference > block.raund_2_time:
            logger.info("True time")

            for candidate_block in candidate_class.candidate_block_hashes[:]:
                logger.debug(f"Candidate block hash {candidate_block}")

                tx_valid = 0

                if block.hash == candidate_block["hash"]:
                    tx_valid += 1

                for other_block in candidate_class.candidate_block_hashes[:]:

                    if (
                        candidate_block != other_block
                        and candidate_block["hash"] == other_block["hash"]
                    ):
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
                            f"Our block is not valid, the system will try to get true block from decentra_network.node {sender}"
                        )
                        node = server.Server
                        unl_list = Unl.get_as_node_type([sender])
                        node.send_client(unl_list[0],  {"action":"sendmefullblock"})
                        block.dowload_true_block = sender
                    SaveBlock(block)

    logger.info("Second round is done")
