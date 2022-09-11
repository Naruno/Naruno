#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.accounts.account import Account
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("BLOCKCHAIN")


def SaveBlock(
    block,
    custom_TEMP_BLOCK_PATH=None,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_TEMP_BLOCKSHASH_PATH=None,
    custom_TEMP_BLOCKSHASH_PART_PATH=None,
):
    """
    Saves the current block to the TEMP_BLOCK_PATH.
    """
    logger.info("Saving block to disk")
    if block.first_time:
        SaveAccounts(
            Account(block.creator, block.coin_amount),
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        )
        SaveBlockshash(
            block.previous_hash,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        )
        SaveBlockshash_part(
            [block.previous_hash],
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        block.first_time = False
    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)
    os.chdir(get_config()["main_folder"])
    with open(the_TEMP_BLOCK_PATH, "w") as block_file:
        json.dump(block.dump_json(), block_file)
