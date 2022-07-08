#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import os

from lib.config_system import get_config

from config import TEMP_ACCOUNTS_PATH


def SaveAccounts(the_accounts, custom_TEMP_ACCOUNTS_PATH=None):
    """
    Saves the accounts to the TEMP_ACCOUNTS_PATH.
    """

    the_TEMP_ACCOUNTS_PATH = (
        TEMP_ACCOUNTS_PATH
        if custom_TEMP_ACCOUNTS_PATH is None
        else custom_TEMP_ACCOUNTS_PATH
    )
    os.chdir(get_config()["main_folder"])
    with open(the_TEMP_ACCOUNTS_PATH, "wb") as block_file:
        pickle.dump(the_accounts, block_file, protocol=2)
