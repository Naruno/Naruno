#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from accounts.get_accounts import GetAccounts
from wallet.wallet import Address


def GetBalance(block, user):
    """
    Returns the users balance.
    """

    balance = -block.minumum_transfer_amount
    user = Address(user)
    for Accounts in GetAccounts():

        if Accounts.Address == user:
            balance += Accounts.balance
            break

    return balance
