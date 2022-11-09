#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.wallet.ellipticcurve.wallet_import import Address


def GetBalance(block, user, account_list=None, dont_convert=False):
    """
    Returns the users balance.
    """

    balance = -block.minumum_transfer_amount
    address = Address(user) if not dont_convert else user

    the_account_list = GetAccounts() if account_list is None else account_list
    the_account_list.execute(
        f"SELECT * FROM account_list WHERE address = '{address}'")
    for row in the_account_list.fetchall():
        balance += row[2]
    return balance
