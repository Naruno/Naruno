#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.wallet.ellipticcurve.wallet_import import Address


def GetSequanceNumber(user, account_list=None):
    user = Address(user)
    sequence_number = 0
    the_account_list = GetAccounts() if account_list is None else account_list
    the_account_list.execute(
        f"SELECT * FROM account_list WHERE address = '{user}'")
    for Accounts in the_account_list.fetchall():
        sequence_number = Accounts[1]
        return sequence_number
    return sequence_number
