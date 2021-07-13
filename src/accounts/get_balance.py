#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.wallet import Address

from blockchain.block.get_block import GetBlock

from accounts.account import GetAccounts


def GetBalance(user, block):
    """
    Returns the users balance.
    """

    balance = -GetBlock().minumum_transfer_amount
    user = "".join(
        [l.strip() for l in user.splitlines() if l and not l.startswith("-----")]
    )
    user = Address(user)
    for Accounts in GetAccounts():

        if Accounts.Address == user:
            balance += Accounts.balance
            break

    for trans in block.pendingTransaction + block.validating_list:
        if user == trans.fromUser:
            balance -= trans.amount + trans.transaction_fee
    return balance
