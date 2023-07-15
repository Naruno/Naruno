#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3
from decimal import Decimal
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

    the_TEMP_ACCOUNTS_PATH = (TEMP_ACCOUNTS_PATH if custom_TEMP_ACCOUNTS_PATH
                              is None else custom_TEMP_ACCOUNTS_PATH)

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
        the_record_account_list = []

        the_record_account_list.append([
            address_of_fromUser,
            the_account_list[address_of_fromUser][0],
            the_account_list[address_of_fromUser][1],
        ]) if address_of_fromUser in the_account_list else None
        the_record_account_list.append([
            trans.toUser,
            the_account_list[trans.toUser][0],
            the_account_list[trans.toUser][1],
        ]) if trans.toUser in the_account_list else None

        for the_pulled_account in the_record_account_list:
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
    logger.info(f"Actions: {actions}")
    for action in actions:
        for account in account_list:
            if action[0] == account.Address:
                alread_in = True if account in edited_accounts else False
                the_account = edited_accounts[edited_accounts.index(account)] if account in edited_accounts else account                
                if the_account.Address == block.fee_address:
                    logger.info(f"Fee Address Input: {the_account.dump_json()}")
                if action[1] == "balance":
                    balance_decimal = Decimal(str(the_account.balance)) + Decimal(str(action[2]))
                    the_account.balance = float(balance_decimal)
                elif action[1] == "sequence_number":
                    the_account.sequence_number += action[2]

                if the_account.Address == block.fee_address:
                    logger.info(f"Fee Address Output: {the_account.dump_json()}")
                if not alread_in:
                    edited_accounts.append(the_account)

    # Syncs new sorted list to block.validating_list

    block.validating_list = sorted(temp_validating_list,
                                   key=lambda x: x.signature)

    new_added_accounts_list = sorted(new_added_accounts_list,
                                     key=lambda x: x.Address)


    logger.debug(f"SaveAccounts list: {new_added_accounts_list + edited_accounts}")
    logger.debug(f"SaveAccounts path: {the_TEMP_ACCOUNTS_PATH}")
    the_account_list_result = SaveAccounts(new_added_accounts_list + edited_accounts,
                 the_TEMP_ACCOUNTS_PATH, sequence=block.sequence_number+block.empty_block_number)

    return [block, the_account_list_result]
