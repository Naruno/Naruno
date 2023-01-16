#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.accounts.get_sequence_number import GetSequanceNumber
from decentra_network.lib.log import get_logger
from decentra_network.transactions.pending.get_pending import GetPending

logger = get_logger("TRANSACTIONS")


def Check_Datas(
    block,
    transaction,
    custom_current_time=None,
    custom_balance=None,
    custom_sequence_number=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
    custom_account_list=None,
):
    """
    Check if the transaction datas are valid
    """

    pending_transactions = GetPending(
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)
    for already_tx in pending_transactions + block.validating_list:
        if already_tx.signature == transaction.signature:
            logger.error("Transaction is already in the pending list")
            return False

    for tx in pending_transactions + block.validating_list:
        if (tx.fromUser == transaction.fromUser
                and tx.signature != transaction.signature):
            logger.info("Multiple transaction in one account")
            return False

    balance = (GetBalance(
        transaction.fromUser,
        block=block,
    ) if custom_balance is None else custom_balance)
    if balance >= (float(transaction.amount) +
                   float(transaction.transaction_fee)):
        pass
    else:
        logger.error("Balance is not valid")
        return False

    if transaction.amount >= block.minumum_transfer_amount:
        pass
    else:
        if (GetBalance(
                transaction.toUser,
                account_list=custom_account_list,
                dont_convert=True,
                block=block,
        ) >= 0):
            pass
        else:
            logger.error("Minimum transfer amount is not reached")
            return False

    if transaction.transaction_fee >= block.transaction_fee:
        pass
    else:
        logger.error(
            f"Transaction fee is not reached {transaction.transaction_fee}-{block.transaction_fee}"
        )
        return False

    get_sequence_number = (GetSequanceNumber(transaction.fromUser)
                           if custom_sequence_number is None else
                           custom_sequence_number)
    if transaction.sequence_number == (get_sequence_number + 1):
        pass
    else:
        logger.error("Sequance number is not valid")
        return False

    current_time = (int(time.time())
                    if custom_current_time is None else custom_current_time)
    if (current_time -
            transaction.transaction_time) <= block.transaction_delay_time:
        pass
    else:
        logger.error("Transaction time is not valid")
        return False

    return True
