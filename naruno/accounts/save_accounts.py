#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sqlite3

from naruno.config import TEMP_ACCOUNTS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT

accounts_db = KOT("accounts_db", folder=get_config()["main_folder"] + "/db")

accounts_ram_db = {}


def get_ram_accounts(name: str, reset: bool = False):
    if not name in accounts_ram_db or reset:
        print("Not")
        record = accounts_db.get("accounts", custom_key_location=name)
        print(record)
        if record is None:
            accounts_ram_db[name] = {}
        else:
            accounts_ram_db[name] = record
    return name


def SaveAccounts(new_account, custom_TEMP_ACCOUNTS_PATH=None, reset: bool = False):
    """
    Saves the accounts to the TEMP_ACCOUNTS_PATH.
    """

    if type(new_account) != list:
        new_account = [new_account]
    for i in new_account:
        print("save", i.__dict__)
    print(custom_TEMP_ACCOUNTS_PATH)

    the_TEMP_ACCOUNTS_PATH = (
        TEMP_ACCOUNTS_PATH
        if custom_TEMP_ACCOUNTS_PATH is None
        else custom_TEMP_ACCOUNTS_PATH
    )

    the_TEMP_ACCOUNTS_PATH = os.path.join(
        get_config()["main_folder"], the_TEMP_ACCOUNTS_PATH
    )

    ram_db_record = get_ram_accounts(the_TEMP_ACCOUNTS_PATH)
    if reset:
        accounts_ram_db[ram_db_record] = {}
    for account in new_account:
        accounts_ram_db[ram_db_record][account.Address] = [
            account.sequence_number,
            account.balance,
        ]
    print(accounts_ram_db[ram_db_record])
    accounts_db.set(
        "accounts",
        accounts_ram_db[ram_db_record],
        custom_key_location=the_TEMP_ACCOUNTS_PATH,
    )
