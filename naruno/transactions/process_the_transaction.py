#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3

from naruno.accounts.account import Account
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.shares import shares
from naruno.config import TEMP_ACCOUNTS_PATH
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import \
    Remove_Duplicates
from naruno.lib.log import get_logger
from naruno.wallet.wallet_import import Address

logger = get_logger("TRANSACTIONS")


def ProccesstheTransaction(
    block,
    the_account_list,
    custom_TEMP_ACCOUNTS_PATH=None,
    custom_shares=None,
    custom_fee_address=None,
    dont_clean=False,
):
    """
    It performs the transactions in the block.vali list and
    puts the transactions in order.

    Queuing is required so that all nodes have the same transaction hash.
    """

    logger.info("Transaction processing started.")

    if not dont_clean:
        block = Remove_Duplicates(block)

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH
                              if custom_TEMP_ACCOUNTS_PATH is None else
                              custom_TEMP_ACCOUNTS_PATH)

    edited_accounts = []

    clean_list = []
    for unclear in block.validating_list:
        if not "NARUNO" in unclear.signature:
            clean_list.append(unclear)
    block.validating_list = clean_list

    the_shares = shares(
        block,
        custom_shares=custom_shares,
        custom_fee_address=custom_fee_address,
        dont_clean=dont_clean,
    )
    block.validating_list = block.validating_list + the_shares

    new_added_accounts_list = []
    account_list = []

    block.validating_list = sorted(block.validating_list,
                                   key=lambda x: x.fromUser)

    temp_validating_list = block.validating_list

    actions = []

    for trans in block.validating_list:
        logger.info(f"Transaction: {trans.__dict__}")

        touser_inlist = True
        to_user_in_new_list = False

        address_of_fromUser = Address(trans.fromUser)
        logger.debug(f"FromUser address: {address_of_fromUser}")
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
                logger.debug(f"FromUser found: {Accounts.Address}")
                actions.append([
                    Accounts.Address,
                    "balance",
                    -(float(trans.amount) + trans.transaction_fee),
                ])
                actions.append([Accounts.Address, "sequence_number", 1])

            if Accounts.Address == trans.toUser:
                logger.debug(f"ToUser found: {Accounts.Address}")
                actions.append(
                    [Accounts.Address, "balance",
                     float(trans.amount)])
                touser_inlist = True

        for i in new_added_accounts_list:
            if i.Address == trans.toUser:
                i.balance += float(trans.amount)
                to_user_in_new_list = True

        # If not included in the account_list, add.
        if not touser_inlist and not to_user_in_new_list:
            new_added_accounts_list.append(
                Account(trans.toUser, float(trans.amount)))

    for action in actions:
        for account in account_list:
            if action[0] == account.Address:
                if action[1] == "balance":
                    account.balance += action[2]
                elif action[1] == "sequence_number":
                    account.sequence_number += action[2]
                edited_accounts.append(account)

    # Syncs new sorted list to block.validating_list

    block.validating_list = sorted(temp_validating_list,
                                   key=lambda x: x.signature)

    new_added_accounts_list = sorted(new_added_accounts_list,
                                     key=lambda x: x.Address)

    conn = sqlite3.connect(the_TEMP_ACCOUNTS_PATH)
    c = conn.cursor()
    for changed_account in edited_accounts:
        c.execute(
            f"UPDATE account_list SET balance = {changed_account.balance}, sequence_number = {changed_account.sequence_number} WHERE address = '{changed_account.Address}'"
        )
        conn.commit()
    conn.close()

    SaveAccounts(new_added_accounts_list, the_TEMP_ACCOUNTS_PATH)

    return block
