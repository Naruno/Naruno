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
        pubkey = "".join([
            l.strip() for l in Wallet_Import(0, 0).splitlines()
            if l and not l.startswith("-----")
        ])
        Block(0, pubkey)
        mynode.main_node.send_full_chain()
    else:
        dprint("Getting block from nodes")
        GetBlock()