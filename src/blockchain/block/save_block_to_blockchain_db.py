#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os
import pickle

from lib.config_system import get_config

from config import BLOCKS_PATH

from accounts.account import GetAccounts


def saveBlockstoBlockchainDB(block):
    """
    Adds the block to the blockchain database
    at BLOCKS_PATH.
    """

    os.chdir(get_config()["main_folder"])
    with open(BLOCKS_PATH+str(block.sequance_number)+".block", 'wb') as block_file:
        pickle.dump(block, block_file, protocol=2)

    with open(BLOCKS_PATH+str(block.sequance_number)+".accounts", 'wb') as block_file:
        pickle.dump(GetAccounts(), block_file, protocol=2)
