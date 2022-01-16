#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from blockchain.block.get_block import GetBlock


def Status():
    """
    Returns the status of the network.
    """

    first_block = GetBlock()
    start_time = time.time()
    while True:
        time.sleep(5)
        new_time = time.time()
        new_block = GetBlock()
        difference = int(new_time - start_time) 
        if not (first_block.sequance_number + first_block.empty_block_number) == (new_block.sequance_number + new_block.empty_block_number):
            if difference <= 6:
                return "Good"
            elif difference <= 10:
                return "Not bad"
            elif difference <= 20:
                return "Bad"
            elif difference >= 20:
                return "Very bad"
        else:
            if difference >= 20:
                return "Not work"
