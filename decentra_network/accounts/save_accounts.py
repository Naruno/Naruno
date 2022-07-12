#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.lib.config_system import get_config


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
    # turn account list to a json array (use dump_json for objects)
    the_accounts_json = {
        account.Address: account.dump_json() for account in the_accounts
    }

    with open(the_TEMP_ACCOUNTS_PATH, "w") as block_file:
        json.dump(the_accounts_json, block_file)
