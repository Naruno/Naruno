#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import json

from blockchain.block.block_main import Block
from config import TEMP_BLOCK_PATH
from lib.config_system import get_config


def GetBlock(custom_TEMP_BLOCK_PATH=None):
    """
    Returns the block.
    """
    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)
    os.chdir(get_config()["main_folder"])
    with open(the_TEMP_BLOCK_PATH, "r") as block_file:
        the_block_json = json.load(block_file)
    the_block = Block.load_json(the_block_json)
    return the_block
