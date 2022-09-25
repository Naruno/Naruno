#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger

logger = get_logger("CONSENSUS")


def true_time(block: Block, return_result=False) -> bool:
    the_time = (block.genesis_time + block.block_time + (
        (block.sequance_number + block.empty_block_number) * block.block_time))
    if int(time.time()) >= the_time:
        return True
    else:
        return False if return_result is False else the_time
