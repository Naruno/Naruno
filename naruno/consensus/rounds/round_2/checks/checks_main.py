#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.rounds.round_2.checks.candidate_blocks_hashes.candidate_blocks_hashes_main import \
    candidate_blocks_hashes_check
from decentra_network.consensus.rounds.round_2.checks.time.time_difference.time_difference_main import \
    time_difference_check
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_SECOND_ROUND")


def round_check(block: Block, candidate_class: candidate_block,
                unl_nodes: dict) -> bool:
    logger.info("Round 2 checking is started")
    if not candidate_blocks_hashes_check(candidate_class, unl_nodes):
        return False
    if not time_difference_check(block=block):
        return False
    logger.info("Round 2 checking is True")
    return True
