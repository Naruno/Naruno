#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3

from decentra_network.accounts.account import Account
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.shares import shares
from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.wallet.ellipticcurve.wallet_import import Address


def ProccesstheTransaction(
    block,
    the_account_list,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_shares=None,
    custom_fee_address=None,
):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH
                              if custom_TEMP_ACCOUNTS_PATH is None else
                              custom_TEMP_ACCOUNTS_PATH)

    from_user_list = []
    to_user_list = []

    clean_list = []
    for unclear in block.validating_list:
        if not unclear.signature == "DN":
            clean_list.append(unclear)
    block.validating_list = clean_list

    the_shares = shares(block,
                        custom_shares=custom_shares,
                        custom_fee_address=custom_fee_address)
    block.validating_list = block.validating_list + the_shares
    temp_validating_list = block.validating_list

    new_added_accounts_list = []
    account_list = []

    for trans in block.validating_list:

        touser_inlist = True
        to_user_in_new_list = False

        address_of_fromUser = Address(trans.fromUser)
        the_account_list.execute(
            f"SELECT * FROM account_list WHERE address = '{address_of_fromUser}'"
        )
        first_list = the_account_list.fetchall()
        the_account_list.execute(
            f"SELECT * FROM account_list WHERE address = '{trans.toUser}'")
        second_list = the_account_list.fetchall()

        for the_pulled_account in first_list + second_list:
            account_list.append(
                Account(the_pulled_account[0], the_pulled_account[2],
                        the_pulled_account[1]))
        for Accounts in account_list:
            touser_inlist = False
            if Accounts.Address == address_of_fromUser:
                Accounts.balance -= float(trans.amount) + trans.transaction_fee
                Accounts.sequence_number += 1
                from_user_list.append(Accounts)

            elif Accounts.Address == trans.toUser:
                Accounts.balance += float(trans.amount)
                touser_inlist = True
                to_user_list.append(Accounts)
                break

        for i in new_added_accounts_list:
            if i.Address == trans.toUser:
                i.balance += float(trans.amount)
                to_user_in_new_list = True

            # If not included in the account_list, add.
        if not touser_inlist and not to_user_in_new_list:
            new_added_accounts_list.append(
                Account(trans.toUser, float(trans.amount)))

    # Syncs new sorted list to block.validating_list

    block.validating_list = sorted(temp_validating_list,
                                   key=lambda x: x.fromUser)

    new_added_accounts_list = sorted(new_added_accounts_list,
                                     key=lambda x: x.Address)

    conn = sqlite3.connect(the_TEMP_ACCOUNTS_PATH)
    c = conn.cursor()
    for changed_account in from_user_list + to_user_list:
        c.execute(
            f"UPDATE account_list SET balance = {changed_account.balance}, sequence_number = {changed_account.sequence_number} WHERE address = '{changed_account.Address}'"
        )
        conn.commit()
    conn.close()

    SaveAccounts(new_added_accounts_list, the_TEMP_ACCOUNTS_PATH)
