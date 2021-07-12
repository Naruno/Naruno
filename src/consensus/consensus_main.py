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
    Consensus process consists of 2 stages. This function makes
    the necessary redirects according to the situation and works
    to shorten the block time.
    """

    dprint("Consensus Trigger")
    block = GetBlock()

    if block.validated:
        true_time = (
            block.block_time_change_time
            + block.block_time
            + (
                (block.block_time_change_block - block.sequance_number)
                * block.block_time
            )
        )
        if block.newly:
            true_time -= 1
        if not int(time.time()) < true_time:
            block.newly = False
            block.reset_the_block()
    else:
        if block.raund_1_starting_time is None:
            block.raund_1_starting_time = int(time.time())
        if not block.raund_1:

            consensus_round_1(block)
        elif not block.raund_2:
            consensus_round_2(block)
