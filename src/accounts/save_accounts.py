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


def save_accounts(the_accounts):
    """
    Saves the accounts to the TEMP_ACCOUNTS_PATH.
    """

    os.chdir(get_config()["main_folder"])
    with open(TEMP_ACCOUNTS_PATH, "wb") as block_file:
        pickle.dump(the_accounts, block_file, protocol=2)