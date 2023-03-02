#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sqlite3

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

    conn = sqlite3.connect(the_TEMP_BLOCKSHASH_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS blockshash_list (hash text)""")
    if type(the_blockshash) == list:
        for i in the_blockshash:
            c.execute("""INSERT INTO blockshash_list VALUES (?)""", (i, ))
    else:
        c.execute(
            """INSERT INTO blockshash_list VALUES (?)""",
            (the_blockshash, ),
        )
    conn.commit()
    conn.close()


def SaveBlockshash_part(the_blockshash, custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Saves the blockshash part to the TEMP_BLOCKSHASH_PART_PATH.
    """

    os.chdir(get_config()["main_folder"])
    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)
    conn = sqlite3.connect(the_TEMP_BLOCKSHASH_PART_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS blockshash_part_list (hash text)""")
    if type(the_blockshash) == list:
        for i in the_blockshash:
            c.execute("""INSERT INTO blockshash_part_list VALUES (?)""", (i, ))
    else:
        c.execute(
            """INSERT INTO blockshash_part_list VALUES (?)""",
            (the_blockshash, ),
        )
    conn.commit()
    conn.close()


def GetBlockshash(custom_TEMP_BLOCKSHASH_PATH=None):
    """
    Returns the blockshash.
    """
    the_TEMP_BLOCKSHASH_PATH = (TEMP_BLOCKSHASH_PATH
                                if custom_TEMP_BLOCKSHASH_PATH is None else
                                custom_TEMP_BLOCKSHASH_PATH)

    os.chdir(get_config()["main_folder"])

    conn = sqlite3.connect(the_TEMP_BLOCKSHASH_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS blockshash_list (hash text)""")
    c.execute("""SELECT * FROM blockshash_list""")
    result = c.fetchall()

    result = [i[0] for i in result]
    conn.close()

    return result


def GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=None):
    """
    Returns the blockshash part.
    """
    the_TEMP_BLOCKSHASH_PART_PATH = (TEMP_BLOCKSHASH_PART_PATH if
                                     custom_TEMP_BLOCKSHASH_PART_PATH is None
                                     else custom_TEMP_BLOCKSHASH_PART_PATH)

    os.chdir(get_config()["main_folder"])

    conn = sqlite3.connect(the_TEMP_BLOCKSHASH_PART_PATH,
                           check_same_thread=False)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS blockshash_part_list (hash text)""")
    c.execute("""SELECT * FROM blockshash_part_list""")
    result = c.fetchall()

    result = [i[0] for i in result]
    conn.close()

    return result
