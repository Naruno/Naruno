#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import threading

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.wallet.ellipticcurve.wallet_import import Address


lock = threading.Lock()

def GetSequanceNumber(user, account_list=None):
    user = Address(user)
    sequance_number = 0
    the_account_list = GetAccounts() if account_list is None else account_list
    try:
        lock.acquire(True)
        the_account_list.execute(
            f"SELECT * FROM account_list WHERE address = '{user}'")
        for Accounts in the_account_list.fetchall():
            sequance_number = Accounts[1]
    finally:
        lock.release()
    return sequance_number
