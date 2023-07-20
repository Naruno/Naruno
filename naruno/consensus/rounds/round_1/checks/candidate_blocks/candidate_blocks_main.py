#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.lib.log import get_logger
from naruno.blockchain.block.block_main import Block
logger = get_logger("CONSENSUS_FIRST_ROUND")


def candidate_blocks_check(candidate_class: candidate_block,
                           unl_nodes: dict, block=None) -> bool:
    logger.info("Candidate block control started for round 2")
    logger.debug(
        f"len(candidate_class.candidate_blocks): {len(candidate_class.candidate_blocks)}"
    )

    the_block = Block(creator="Naruno") if block is None else block

    logger.debug(f"len(unl_nodes): {len(unl_nodes)}")
    if len(candidate_class.candidate_blocks) > ((
        (len(unl_nodes) + 1) * the_block.candidate_blocks_check) / 100):
        logger.info("Candidate block number is True")
        return True
    else:
        logger.info("Candidate block number is not True")
        return False
