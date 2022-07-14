#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.wallet.ellipticcurve.wallet_import import Address


def ProccesstheTransaction(block, account_list):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    from_user_list = []
    temp_validating_list = block.validating_list

    new_added_accounts_list = []

    for trans in block.validating_list:
        touser_inlist = True
        to_user_in_new_list = False

        address_of_fromUser = Address(trans.fromUser)

        for Accounts in account_list:
            touser_inlist = False
            if Accounts.Address == address_of_fromUser:
                Accounts.balance -= float(trans.amount) + trans.transaction_fee

                Accounts.sequance_number += 1
                from_user_list.append(Accounts)
                block.edited_accounts.append(Accounts)

            elif Accounts.Address == trans.toUser:
                Accounts.balance += float(trans.amount)
                touser_inlist = True
                block.edited_accounts.append(Accounts)
                break

            for i in new_added_accounts_list:
                if i.Address == trans.toUser:
                    i.balance += float(trans.amount)
                    to_user_in_new_list = True

            # If not included in the account_list, add.
        if not touser_inlist and not to_user_in_new_list:
            new_added_accounts_list.append(Account(trans.toUser, float(trans.amount)))

    # Syncs new sorted list to block.validating_list

    block.validating_list = sorted(temp_validating_list, key=lambda x: x.fromUser)

    new_added_accounts_list = sorted(new_added_accounts_list, key=lambda x: x.Address)
    account_list.extend(new_added_accounts_list)
