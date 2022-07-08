#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pickle


from accounts.account import Account
from accounts.get_accounts import GetAccounts
from accounts.save_accounts import SaveAccounts
from blockchain.block.blocks_hash import SaveBlockshash
from config import TEMP_BLOCK_PATH
from lib.config_system import get_config
from lib.log import get_logger

logger = get_logger("BLOCKCHAIN")

def SaveBlock(block):
    """
    Saves the current block to the TEMP_BLOCK_PATH.
    """
    if block.first_time:
        accounts_list = GetAccounts()
        if accounts_list == []:
            SaveAccounts([Account(block.creator, block.coin_amount)])
        blocks_hash = [block.previous_hash]
        SaveBlockshash(blocks_hash)
        block.first_time = False
    os.chdir(get_config()["main_folder"])
    with open(TEMP_BLOCK_PATH, "wb") as block_file:
        pickle.dump(block, block_file, protocol=2)
