#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from contextlib import suppress
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.lib.log import get_logger
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import

logger = get_logger("BLOCKCHAIN")


def CreateBlock(custom_TEMP_BLOCK_PATH=None):
    """
    If test mode is on, creates genesis block
    and send the connected nodes, if it is off,
    it calls get_block() function.
    """

    previous_hash = None

    with suppress(Exception):
        current_block = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
        if current_block.hash is not None:
            previous_hash = current_block.hash
        else:
            previous_hash = current_block.previous_hash

    logger.info("Creating the genesis block and sending it to the connected nodes")

    if previous_hash is None:
        return Block(wallet_import(-1, 3))
    else:
        return Block(wallet_import(-1, 3), previous_hash=previous_hash)
