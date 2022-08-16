#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_SECOND_ROUND")


def candidate_blocks_hashes_check(candidate_class: candidate_block,
                                  unl_nodes: dict) -> bool:
    if len(candidate_class.candidate_block_hashes) >= (
        (len(unl_nodes) * 80) / 100):
        return True
    else:
        return False
