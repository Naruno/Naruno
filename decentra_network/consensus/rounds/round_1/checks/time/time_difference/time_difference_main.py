#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS_FIRST_ROUND")


def time_difference_check(block: Block) -> bool:

    time_difference = int(time.time()) - block.start_time
    logger.debug(f"Time difference is {time_difference}")
    if time_difference > block.round_1_time:
        return True
    else:
        return False
