#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.consensus.rounds.round_1.round_1_main import \
    consensus_round_1
from decentra_network.consensus.rounds.round_2.round_2_main import \
    consensus_round_2
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS")


def ongoing_main(block: Block) -> None:

    if not block.round_1:
        logger.info("First round is starting")
        consensus_round_1(block)
        logger.info("First round is done")
    elif not block.round_2:
        logger.info("Second round is starting")
        consensus_round_2(block)
        logger.info("Second round is done")
