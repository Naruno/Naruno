#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.blockchain.block.block_main import Block
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.lib.cache import Cache
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("BLOCKCHAIN")


def GetBlock(custom_TEMP_BLOCK_PATH=None, no_cache=False):
    """
    Returns the block.
    """
    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)
    the_cache = Cache.get(the_TEMP_BLOCK_PATH)

    if the_cache is None or no_cache:
        os.chdir(get_config()["main_folder"])
        with open(the_TEMP_BLOCK_PATH, "r") as block_file:
            the_block_json = json.load(block_file)
        result = Block.load_json(the_block_json)
        Cache.save(the_TEMP_BLOCK_PATH, result) if not no_cache else None
        return result
    else:
        return the_cache
