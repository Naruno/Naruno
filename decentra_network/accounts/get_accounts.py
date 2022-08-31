#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sqlite3

from decentra_network.accounts.account import Account
from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.lib.cache import Cache
from decentra_network.lib.config_system import get_config


def GetAccounts(custom_TEMP_ACCOUNTS_PATH=None):
    """
    Returns the accounts from TEMP_ACCOUNTS_PATH.
    """

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH
                              if custom_TEMP_ACCOUNTS_PATH is None else
                              custom_TEMP_ACCOUNTS_PATH)

    the_cache = Cache.get(the_TEMP_ACCOUNTS_PATH)
    the_cache_2 = Cache.get(f"{the_TEMP_ACCOUNTS_PATH}_conn")
    if the_cache is None or the_cache_2 is None:
        os.chdir(get_config()["main_folder"])
        conn = sqlite3.connect(the_TEMP_ACCOUNTS_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS account_list (address text, sequance_number integer, balance integer)"""
        )
        conn.commit()

        Cache.save(the_TEMP_ACCOUNTS_PATH, c)
        Cache.save(f"{the_TEMP_ACCOUNTS_PATH}_conn", conn)
        return c
    else:
        return the_cache
