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


def GetAccounts():
    """
    Returns the accounts from TEMP_ACCOUNTS_PATH.
    """
    
    os.chdir(get_config()["main_folder"])
    if not os.path.exists(TEMP_ACCOUNTS_PATH):
        return []
    else:
        with open(TEMP_ACCOUNTS_PATH, "rb") as block_file:
            return pickle.load(block_file)
