#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.wallet.ellipticcurve.wallet_import import Address
from decentra_network.accounts.get_accounts import GetAccounts


def GetBalance(block, user, account_list=None):
    """
    Returns the users balance.
    """

    balance = -block.minumum_transfer_amount
    user = Address(user)
    the_account_list = GetAccounts() if account_list is None else account_list
    for Accounts in the_account_list:

        if Accounts.Address == user:
            balance += Accounts.balance

            break

    return balance
