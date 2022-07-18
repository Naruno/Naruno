#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import TEMP_BLOCKSHASH_PART_PATH
from decentra_network.config import TEMP_BLOCKSHASH_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("BLOCKCHAIN")


def SaveBlockshash(the_blockshash, custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Saves the blockshash to the TEMP_BLOCKSHASH_PATH.
    """

    os.chdir(get_config()["main_folder"])
    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)
    with open(the_TEMP_BLOCKSHASH_PATH, "w") as block_file:
        json.dump(the_blockshash, block_file)


def SaveBlockshash_part(the_blockshash, custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Saves the blockshash part to the TEMP_BLOCKSHASH_PART_PATH.
    """

    os.chdir(get_config()["main_folder"])
    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)
    logger.info(
        f"Saving blockshash part to disk ({the_TEMP_BLOCKSHASH_PART_PATH})")
    with open(the_TEMP_BLOCKSHASH_PART_PATH, "w") as block_file:
        json.dump(the_blockshash, block_file)


def GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Returns the blockshash.
    """
    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)
    os.chdir(get_config()["main_folder"])
    if not os.path.exists(the_TEMP_BLOCKSHASH_PATH):
        return []

    with open(the_TEMP_BLOCKSHASH_PATH, "r") as block_file:
        return json.load(block_file)


def GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Returns the blockshash part.
    """
    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)
    os.chdir(get_config()["main_folder"])
    if not os.path.exists(the_TEMP_BLOCKSHASH_PART_PATH):
        return []

    with open(the_TEMP_BLOCKSHASH_PART_PATH, "r") as block_file:
        return json.load(block_file)
