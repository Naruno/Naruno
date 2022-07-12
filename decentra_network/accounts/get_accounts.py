#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.accounts.account import Account
from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.lib.config_system import get_config


def GetAccounts(custom_TEMP_ACCOUNTS_PATH=None):
    """
    Returns the accounts from TEMP_ACCOUNTS_PATH.
    """

    the_TEMP_ACCOUNTS_PATH = (
        TEMP_ACCOUNTS_PATH
        if custom_TEMP_ACCOUNTS_PATH is None
        else custom_TEMP_ACCOUNTS_PATH
    )

    os.chdir(get_config()["main_folder"])
    if not os.path.exists(the_TEMP_ACCOUNTS_PATH):
        return []
    with open(the_TEMP_ACCOUNTS_PATH, "r") as block_file:
        the_accounts_json = json.load(block_file)

    return [
        Account.load_json(the_accounts_json[account_json])
        for account_json in the_accounts_json
    ]
