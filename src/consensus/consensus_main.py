#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from lib.mixlib import dprint

from consensus.consensus_first_round import consensus_round_1
from consensus.consensus_second_round import consensus_round_2

from blockchain.block.get_block import GetBlock


def consensus_trigger():
    """
    Gets the temporary block and starts the Block.consensus().
    """
    dprint("Consensus Trigger")
    block = GetBlock()

    if block.validated:
        if not int(time.time()) < (block.start_time + (block.sequance_number * block.block_time)):
           block.reset_the_block()  
    elif not (int(time.time()) - block.validating_list_starting_time) < block.validating_list_time:
        #or len(block.validating_list) == block.max_tx_number
        if block.raund_1_starting_time is None:
            block.raund_1_starting_time = int(time.time())
        if not block.raund_1:

            consensus_round_1(block)
        elif not block.raund_2:
            consensus_round_2(block)