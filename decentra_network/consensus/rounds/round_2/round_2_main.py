#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from decentra_network.consensus.rounds.round_1.checks.checks_main import round_check
from decentra_network.consensus.rounds.round_2.checks.checks_main import round_check
from decentra_network.consensus.rounds.round_2.process.process_main import round_process
from decentra_network.lib.log import get_logger
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
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
    candidate_class = GetCandidateBlocks()

    if round_check(block, candidate_class, unl_nodes):
        round_process(block, candidate_class, unl_nodes)
        return True
    else:
        logger.info("Our block hash is sending to the unl nodes")
        server.Server.send_my_block_hash(block)
        return False

    logger.info("Second round is done")
