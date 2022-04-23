#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from blockchain.block.block_main import Block
from blockchain.block.get_block import GetBlock
from lib.log import get_logger
from lib.settings_system import the_settings
from node.node import Node
from wallet.wallet import Wallet_Import

logger = get_logger("BLOCKCHAIN")


def CreateBlock():
    """
    If test mode is on, creates genesis block
    and send the connected nodes, if it is off,
    it calls get_block() function.
    """

    if the_settings()["test_mode"]:
        previous_hash = "0"

        try:
            current_block = GetBlock()
            if not current_block.hash is None:
                previous_hash = current_block.hash
            else:
                previous_hash = current_block.previous_hash
        except:
            pass

        logger.info(
            "Creating the genesis block and sending it to the connected nodes")
        Block(Wallet_Import(-1, 3), previous_hash)
        Node.main_node.send_full_accounts()
        Node.main_node.send_full_chain()
        Node.main_node.send_full_blockshash()
    else:
        logger.info("Getting the last block from the connected nodes")
        GetBlock()
