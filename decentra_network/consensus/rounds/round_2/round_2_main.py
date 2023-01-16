#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.rounds.round_1.checks.checks_main import \
    round_check
from decentra_network.consensus.rounds.round_2.checks.checks_main import \
    round_check
from decentra_network.consensus.rounds.round_2.process.process_main import \
    round_process
from decentra_network.lib.log import get_logger
from decentra_network.node.client.client import client
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl

logger = get_logger("CONSENSUS_SECOND_ROUND")


def consensus_round_2(
    block: Block,
    candidate_class: candidate_block = None,
    unl_nodes: dict = None,
    custom_server: server = None,
    custom_unl: client = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
) -> bool:
    """
    At this stage of the consensus process,
    The blocks (block hashes) of our and the
    unl nodes are compared and the block accepted
    by majority approving.

    Inputs:
      * block: The block (class) we want consensus
      round 2 to be done
    """

    logger.info(
        f"BLOCK#{block.sequence_number}:{block.empty_block_number} second round is starting"
    )

    unl_nodes = Unl.get_unl_nodes() if unl_nodes is None else unl_nodes
    candidate_class = (GetCandidateBlocks(block=block)
                       if candidate_class is None else candidate_class)
    logger.debug(f"unl_nodes: {unl_nodes}")
    logger.debug(f"candidate_class: {candidate_class.__dict__}")

    if round_check(block, candidate_class, unl_nodes):
        round_process(
            block,
            candidate_class,
            unl_nodes,
            custom_server=custom_server,
            custom_unl=custom_unl,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        
        logger.info("Round 2 check is True")
        return True
    else:
        logger.warning("Round 2 check is False")
        return False

