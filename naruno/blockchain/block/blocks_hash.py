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
from naruno.lib.kot import KOT
from naruno.lib.log import get_logger

blockshash_db = KOT("blockshash", folder=get_config()["main_folder"] + "/db")

logger = get_logger("BLOCKCHAIN")


def SaveBlockshash(the_blockshash, custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Saves the blockshash to the TEMP_BLOCKSHASH_PATH.
    """
    os.chdir(get_config()["main_folder"])

    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)

    the_TEMP_BLOCKSHASH_PATH = os.path.join(get_config()["main_folder"],
                                            the_TEMP_BLOCKSHASH_PATH)

    if type(the_blockshash) != list:
        the_blockshash = [the_blockshash]

    the_blockshash = (GetBlockshash(
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH) +
                      the_blockshash)

    blockshash_db.set("blockshash",
                      the_blockshash,
                      custom_key_location=the_TEMP_BLOCKSHASH_PATH)


def SaveBlockshash_part(the_blockshash, custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Saves the blockshash part to the TEMP_BLOCKSHASH_PART_PATH.
    """
    os.chdir(get_config()["main_folder"])

    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)

    the_TEMP_BLOCKSHASH_PART_PATH = os.path.join(
        get_config()["main_folder"], the_TEMP_BLOCKSHASH_PART_PATH)

    if type(the_blockshash) != list:
        the_blockshash = [the_blockshash]

    the_blockshash = (GetBlockshash_part(
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH) +
                      the_blockshash)

    blockshash_db.set(
        "blockshash_part",
        the_blockshash,
        custom_key_location=the_TEMP_BLOCKSHASH_PART_PATH,
    )


def GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Returns the blockshash.
    """
    os.chdir(get_config()["main_folder"])

    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)

    the_TEMP_BLOCKSHASH_PATH = os.path.join(get_config()["main_folder"],
                                            the_TEMP_BLOCKSHASH_PATH)

    record = blockshash_db.get("blockshash",
                               custom_key_location=the_TEMP_BLOCKSHASH_PATH)

    return record if record is not None else []


def GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Returns the blockshash part.
    """
    os.chdir(get_config()["main_folder"])

    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)

    the_TEMP_BLOCKSHASH_PART_PATH = os.path.join(
        get_config()["main_folder"], the_TEMP_BLOCKSHASH_PART_PATH)

    record = blockshash_db.get(
        "blockshash_part", custom_key_location=the_TEMP_BLOCKSHASH_PART_PATH)

    return record if record is not None else []
