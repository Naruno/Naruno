#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.rounds.round_1.checks.candidate_blocks.candidate_blocks_main import \
    candidate_blocks_check
from decentra_network.consensus.rounds.round_1.checks.time.time_difference.time_difference_main import \
    time_difference_check
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_FIRST_ROUND")


def round_check(
    block: Block, 
    candidate_class: candidate_block,
    unl_nodes: dict,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,    
    ) -> bool:
    logger.info("Round 1 checking is started")
    if not time_difference_check(
        block=block,
        custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,           
        ):
        return False    
    if not candidate_blocks_check(candidate_class, unl_nodes):
        return False
    logger.info("Round 1 checking is True")
    return True
