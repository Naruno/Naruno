#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger

logger = get_logger("CONSENSUS_SECOND_ROUND")


def candidate_blocks_hashes_check(candidate_class: candidate_block,
                                  unl_nodes: dict, block=None) -> bool:
    logger.info("Candidate block hash control started for round 2")
    logger.debug(
        f"len(candidate_class.candidate_block_hashes): {len(candidate_class.candidate_block_hashes)}"
    )
    logger.debug(f"len(unl_nodes): {len(unl_nodes)}")

    the_block = Block(creator="Naruno") if block is None else block
    if len(candidate_class.candidate_block_hashes) > ((
        (len(unl_nodes) + 1) * the_block.candidate_blocks_hashes_check) / 100):
        logger.info("Candidate block hash number is True")
        return True
    else:
        logger.info("Candidate block hash number is not True")
        return False
