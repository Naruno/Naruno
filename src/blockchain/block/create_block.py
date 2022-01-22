#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from lib.settings_system import the_settings
from lib.mixlib import dprint

from node.myownp2pn import mynode

from blockchain.block.block_main import Block
from blockchain.block.get_block import GetBlock

from wallet.wallet import Wallet_Import


def CreateBlock():
    """
    If test mode is on, creates genesis block
    and send the connected nodes, if it is off,
    it calls get_block() function.
    """

    if the_settings()["test_mode"]:
        dprint("Creating the genesis block")
        previous_hash = "0"

        try:
            current_block = GetBlock() 
            if not current_block.hash is None:
                previous_hash = current_block.hash       
            else:
                previous_hash = current_block.previous_hash
        except:
            pass

        Block(Wallet_Import(-1, 3), previous_hash)
        mynode.main_node.send_full_accounts()
        mynode.main_node.send_full_chain()
        mynode.main_node.send_full_blockshash()
    else:
        dprint("Getting block from nodes")
        GetBlock()
