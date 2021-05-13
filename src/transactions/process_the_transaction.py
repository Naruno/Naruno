#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from accounts.account import Account


def ProccesstheTransaction(block):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    from_user_list = []
    temp_validating_list = block.validating_list

    for trans in block.validating_list:
        touser_inlist = False

        for Accounts in block.Accounts:

            if Accounts.PublicKey == trans.fromUser:
                Accounts.balance -= (float(trans.amount)+trans.transaction_fee)
                Accounts.sequance_number += 1
                from_user_list.append(Accounts)

            elif Accounts.PublicKey == trans.toUser:
                Accounts.balance += float(trans.amount)
                touser_inlist = True

        # If not included in the block.Accounts, add.
        if not touser_inlist:
            block.Accounts.append(Account(trans.toUser, float(trans.amount)))

    # Converts public keys to an Account class to use when ordering
    for tx_item in temp_validating_list[:]:
        for Account_item in from_user_list:

            if tx_item.fromUser == Account_item.PublicKey:
                tx_item.fromUser = Account_item

    # Orders the transactions by fromUser index of block.Accounts.
    temp_validating_list = sorted(temp_validating_list, key=lambda x: block.Accounts.index(x.fromUser))

    # Converts the Account class to Public key.
    for temp_validating_list_item in temp_validating_list[:]:
        temp_validating_list_item.fromUser = temp_validating_list_item.fromUser.PublicKey

    # Syncs new sorted list to block.validating_list
    block.validating_list = temp_validating_list
