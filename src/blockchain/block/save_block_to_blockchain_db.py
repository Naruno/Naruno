#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle

from config import BLOCKS_PATH

from accounts.account import GetAccounts, GetAccounts_part

from blockchain.block.blocks_hash import GetBlockshash, GetBlockshash_part

from wallet.wallet import Wallet_Import


def saveBlockstoBlockchainDB(block):
    """
    Adds the block to the blockchain database
    at BLOCKS_PATH.
    """

    our_tx = False
    my_public_key = "".join(
        [
            l.strip()
            for l in Wallet_Import(-1, 0).splitlines()
            if l and not l.startswith("-----")
        ]
    )
    my_address = Wallet_Import(-1, 3)
    for validated_transaction in block.validating_list:
        if validated_transaction.fromUser == my_public_key or validated_transaction.toUser == my_address:
            our_tx = True

    # If the block is our transaction, then add it to the blockchain database.
    if our_tx:
        #
        with open(BLOCKS_PATH + str(block.sequance_number) + ".block", "wb") as block_file:
            pickle.dump(block, block_file, protocol=2)

        with open(
            BLOCKS_PATH + str(block.sequance_number) + ".accounts", "wb"
        ) as block_file:
            pickle.dump(GetAccounts(), block_file, protocol=2)

        with open(
            BLOCKS_PATH + str(block.sequance_number) + ".accountspart", "wb"
        ) as block_file:
            pickle.dump(GetAccounts_part(), block_file, protocol=2)

        with open(
            BLOCKS_PATH + str(block.sequance_number) + ".blockshash", "wb"
        ) as block_file:
            pickle.dump(GetBlockshash(), block_file, protocol=2)

        with open(
            BLOCKS_PATH + str(block.sequance_number) + ".blockshashpart", "wb"
        ) as block_file:
            pickle.dump(GetBlockshash_part(), block_file, protocol=2)
