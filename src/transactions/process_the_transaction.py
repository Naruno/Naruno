#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from accounts.account import Account
from accounts.account import GetAccounts
from accounts.save_accounts import save_accounts
from wallet.wallet import Address


def ProccesstheTransaction(block):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    from_user_list = []
    temp_validating_list = block.validating_list

    temp_accounts = GetAccounts()
    new_added_accounts_list = []

    for trans in block.validating_list:
        touser_inlist = False
        address_of_fromUser = Address(trans.fromUser)

        for Accounts in temp_accounts:

            if Accounts.Address == address_of_fromUser:
                Accounts.balance -= float(trans.amount) + trans.transaction_fee
                Accounts.sequance_number += 1
                from_user_list.append(Accounts)
                block.edited_accounts.append(Accounts)

            elif Accounts.Address == trans.toUser:
                Accounts.balance += float(trans.amount)
                touser_inlist = True
                block.edited_accounts.append(Accounts)

        # If not included in the temp_accounts, add.
        if not touser_inlist:
            new_added_accounts_list.append(
                Account(trans.toUser, float(trans.amount)))

    # Syncs new sorted list to block.validating_list

    block.validating_list = sorted(temp_validating_list,
                                   key=lambda x: x.fromUser)

    new_accounts_list = temp_accounts + sorted(new_added_accounts_list,
                                               key=lambda x: x.Address)

    save_accounts(new_accounts_list)
