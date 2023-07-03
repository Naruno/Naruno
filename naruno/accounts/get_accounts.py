#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sqlite3

import naruno
from naruno.accounts.save_accounts import get_ram_accounts
from naruno.config import TEMP_ACCOUNTS_PATH
from naruno.lib.config_system import get_config


def GetAccounts(custom_TEMP_ACCOUNTS_PATH=None, reset: bool = False):
    """
    Returns the accounts from TEMP_ACCOUNTS_PATH.
    """
    os.chdir(get_config()["main_folder"])

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH if custom_TEMP_ACCOUNTS_PATH
                              is None else custom_TEMP_ACCOUNTS_PATH)
    the_TEMP_ACCOUNTS_PATH = os.path.join(get_config()["main_folder"],
                                          the_TEMP_ACCOUNTS_PATH)
    return naruno.accounts.save_accounts.accounts_ram_db[get_ram_accounts(
        the_TEMP_ACCOUNTS_PATH, reset=reset)]
