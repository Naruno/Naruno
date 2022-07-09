#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from blockchain.block.block_main import Block
from blockchain.block.get_block import GetBlock
from lib.log import get_logger
from wallet.wallet_import import wallet_import

logger = get_logger("BLOCKCHAIN")


def CreateBlock(custom_TEMP_BLOCK_PATH=None):
    """
    If test mode is on, creates genesis block
    and send the connected nodes, if it is off,
    it calls get_block() function.
    """

    previous_hash = None

    try:
        current_block = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        if not current_block.hash is None:
            previous_hash = current_block.hash
        else:
            previous_hash = current_block.previous_hash
    except:
            pass

    logger.info(
            "Creating the genesis block and sending it to the connected nodes")
    the_block = None
    if previous_hash is None:
            the_block = Block(wallet_import(-1, 3))
    else:
            the_block = Block(wallet_import(-1, 3),
                              previous_hash=previous_hash)
    return the_block



