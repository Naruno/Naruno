#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pickle

from accounts.get_accounts import GetAccounts
from blockchain.block.blocks_hash import GetBlockshash
from blockchain.block.blocks_hash import GetBlockshash_part
from config import BLOCKS_PATH
from wallet.wallet_import import wallet_import


def SaveBlockstoBlockchainDB(block,
                             custom_BLOCKS_PATH=None,
                             custom_TEMP_ACCOUNTS_PATH=None,
                             custom_TEMP_BLOCKSHASH_PATH=None,
                             custom_TEMP_BLOCKSHASH_PART_PATH=None
                             ):
    """
    Adds the block to the blockchain database
    at BLOCKS_PATH.
    """

    our_tx = False
    my_public_key = "".join([
        l.strip() for l in wallet_import(-1, 0).splitlines()
        if l and not l.startswith("-----")
    ])
    my_address = wallet_import(-1, 3)
    for validated_transaction in block.validating_list:
        if (validated_transaction.fromUser == my_public_key) or (validated_transaction.toUser == my_address):
            our_tx = True

    # If the block is our transaction, then add it to the blockchain database.
    if our_tx:
        the_BLOCKS_PATH = BLOCKS_PATH if custom_BLOCKS_PATH is None else custom_BLOCKS_PATH
        with open(the_BLOCKS_PATH + str(block.sequance_number) + ".block",
                  "wb") as block_file:
            pickle.dump(block, block_file, protocol=2)

        with open(the_BLOCKS_PATH + str(block.sequance_number) + ".accounts",
                  "wb") as block_file:
            pickle.dump(GetAccounts(
                custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH), block_file, protocol=2)

        with open(the_BLOCKS_PATH + str(block.sequance_number) + ".blockshash",
                  "wb") as block_file:
            pickle.dump(GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH), block_file, protocol=2)

        with open(the_BLOCKS_PATH + str(block.sequance_number) + ".blockshashpart",
                  "wb") as block_file:
            pickle.dump(GetBlockshash_part(
                custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH), block_file, protocol=2)
    else:
        False
