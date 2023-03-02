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
from decentra_network.lib.config_system import get_config


def GetAccounts(custom_TEMP_ACCOUNTS_PATH=None):
    """
    Returns the accounts from TEMP_ACCOUNTS_PATH.
    """

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH
                              if custom_TEMP_ACCOUNTS_PATH is None else
                              custom_TEMP_ACCOUNTS_PATH)

    os.chdir(get_config()["main_folder"])
    conn = sqlite3.connect(the_TEMP_ACCOUNTS_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS account_list (address text, sequence_number integer, balance integer)"""
    )

    return c
