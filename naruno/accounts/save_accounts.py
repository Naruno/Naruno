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
from naruno.lib.log import get_logger
import hashlib

accounts_db = KOT("accounts_db", folder=get_config()["main_folder"] + "/db")

accounts_ram_db = {}


operations_hashes = []
logger = get_logger("ACCOUNTS")

def get_ram_accounts(name: str, reset: bool = False):
    if not name in accounts_ram_db or reset:
        record = accounts_db.get("accounts", custom_key_location=name)

        if record is None:
            accounts_ram_db[name] = {}
        else:
            accounts_ram_db[name] = record
    return name


def SaveAccounts(new_account,
                 custom_TEMP_ACCOUNTS_PATH=None,
                 reset: bool = False,sequence=None):
    """
    Saves the accounts to the TEMP_ACCOUNTS_PATH.
    """

    os.chdir(get_config()["main_folder"])

    if type(new_account) != list:
        new_account = [new_account]

    if sequence is not None:
        logger.info("Sequence is not node")
        the_string=str(sequence)+str(custom_TEMP_ACCOUNTS_PATH)
        logger.debug(f"String: {the_string}")
        the_hash = hashlib.sha256(the_string.encode()).hexdigest()
        logger.debug(f"Hash: {the_hash}")
        if the_hash in operations_hashes:
            logger.warning("Two times try")
            return
        else:
            logger.info("Passed")
            operations_hashes.append(the_hash)



    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH if custom_TEMP_ACCOUNTS_PATH
                              is None else custom_TEMP_ACCOUNTS_PATH)

    the_TEMP_ACCOUNTS_PATH = os.path.join(get_config()["main_folder"],
                                          the_TEMP_ACCOUNTS_PATH)

    ram_db_record = get_ram_accounts(the_TEMP_ACCOUNTS_PATH)
    if reset:
        accounts_ram_db[ram_db_record] = {}
    for account in new_account:
        accounts_ram_db[ram_db_record][account.Address] = [
            account.sequence_number,
            account.balance,
        ]

    accounts_db.set(
        "accounts",
        accounts_ram_db[ram_db_record],
        custom_key_location=the_TEMP_ACCOUNTS_PATH,
    )


    return accounts_ram_db[ram_db_record]