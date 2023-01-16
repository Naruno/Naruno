#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.rounds.round_1.checks.checks_main import \
    round_check
from decentra_network.consensus.rounds.round_1.process.process_main import \
    round_process
from decentra_network.lib.log import get_logger
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.pending_to_validating import PendingtoValidating

logger = get_logger("CONSENSUS_FIRST_ROUND")


def consensus_round_1(
    block: Block,
    custom_candidate_class: candidate_block = None,
    custom_unl_nodes: dict = None,
    custom_UNL_NODES_PATH: str = None,
    custom_server: server = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
    custom_shares=None,
    custom_fee_address=None,
) -> bool:
    """
    At this stage of the consensus process,
    The transactions of our and the unl nodes
    are evaluated and transactions accepted by
    owned by more than 50 percent.
    Inputs:
      * block: The block (class) we want consensus
      round 1 to be done
    """

    logger.info(
        f"BLOCK#{block.sequence_number}:{block.empty_block_number} First round is starting"
    )

    unl_nodes = (Unl.get_unl_nodes(custom_UNL_NODES_PATH=custom_UNL_NODES_PATH)
                 if custom_unl_nodes is None else custom_unl_nodes)
    logger.debug(f"unl_nodes: {unl_nodes}")
    candidate_class = (
        GetCandidateBlocks(custom_nodes_list=Unl.get_as_node_type(unl_nodes), block=block)
        if custom_candidate_class is None else custom_candidate_class)
    logger.debug(f"candidate_class: {candidate_class.__dict__}")

    if round_check(
        block, 
        candidate_class, 
        unl_nodes,
        custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,        
        ):
        round_process(
            block,
            candidate_class,
            unl_nodes,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            custom_shares=custom_shares,
            custom_fee_address=custom_fee_address,
        )
        logger.info("Round 1 check is True")
        return True
    else:
       
        logger.warning("Round 1 check is False")
        return False
