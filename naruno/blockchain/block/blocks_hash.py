#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sqlite3

from naruno.config import TEMP_BLOCKSHASH_PART_PATH
from naruno.config import TEMP_BLOCKSHASH_PATH
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.lib.kot import KOT

blockshash_db = KOT("blockshash", folder=get_config()["main_folder"] + "/db")

logger = get_logger("BLOCKCHAIN")


def SaveBlockshash(the_blockshash, custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Saves the blockshash to the TEMP_BLOCKSHASH_PATH.
    """

    if not type(the_blockshash) == list:
        the_blockshash = [the_blockshash]

    blockshash_db.set("blockshash", the_blockshash) if custom_TEMP_BLOCKSHASH_PATH is None else KOT("blockshash"+custom_TEMP_BLOCKSHASH_PATH, folder=get_config()["main_folder"] + "/db").set("blockshash", the_blockshash)



def SaveBlockshash_part(the_blockshash, custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Saves the blockshash part to the TEMP_BLOCKSHASH_PART_PATH.
    """

    if not type(the_blockshash) == list:
        the_blockshash = [the_blockshash]
    blockshash_db.set("blockshash_part", the_blockshash) if custom_TEMP_BLOCKSHASH_PART_PATH is None else KOT("blockshash"+custom_TEMP_BLOCKSHASH_PART_PATH, folder=get_config()["main_folder"] + "/db").set("blockshash_part", the_blockshash)





def GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Returns the blockshash.
    """
    record = blockshash_db.get("blockshash") if custom_TEMP_BLOCKSHASH_PATH is None else KOT("blockshash"+custom_TEMP_BLOCKSHASH_PATH, folder=get_config()["main_folder"] + "/db").get("blockshash")
    return record if record is not None else []

def GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Returns the blockshash part.
    """
    record = blockshash_db.get("blockshash_part") if custom_TEMP_BLOCKSHASH_PART_PATH is None else KOT("blockshash"+custom_TEMP_BLOCKSHASH_PART_PATH, folder=get_config()["main_folder"] + "/db").get("blockshash_part")

    return record if record is not None else []
