#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.wallet import Address

from accounts.account import Account,  GetAccounts
from accounts.save_accounts import save_accounts


def ProccesstheTransaction(block):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    from_user_list = []
    temp_validating_list = block.validating_list

    temp_accounts = GetAccounts()

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
            temp_accounts.append(Account(trans.toUser, float(trans.amount)))

    # Converts public keys to an Account class to use when ordering
    temp_pubkeys = []
    for tx_item in temp_validating_list[:]:
        for Account_item in from_user_list:
            if Address(str(tx_item.fromUser)) == Account_item.Address:
                temp_pubkeys.append(str(tx_item.fromUser))
                tx_item.fromUser = Account_item

    # Orders the transactions by Address index of temp_accounts.
    temp_validating_list = sorted(
        temp_validating_list, key=lambda x: temp_accounts.index(x.fromUser)
    )

    # Converts the Account class to Public key.
    for temp_validating_list_item in temp_validating_list[:]:
        for temp_pubkey in temp_pubkeys:
            if str(temp_validating_list_item.fromUser) == Address(temp_pubkey):
                temp_validating_list_item.fromUser = temp_pubkey

    # Syncs new sorted list to block.validating_list
    block.validating_list = temp_validating_list

    save_accounts(temp_accounts)
