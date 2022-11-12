#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.log import get_logger
from decentra_network.transactions.pending.delete_pending import DeletePending
from decentra_network.transactions.pending.get_pending import GetPending

logger = get_logger("TRANSACTIONS")


def PendingtoValidating(block):
    """
    Adds transactions to the verification list
    if there are suitable conditions.
    """
    logger.info("Pending to validating transfer process is started")
    first_validating_list_len = len(block.validating_list)
    first_max_tx_number = block.max_tx_number
    logger.debug(f"Currently tx amount: {first_validating_list_len}")
    logger.debug(f"Validating list capacity: {first_max_tx_number}")
    if len(block.validating_list) < block.max_tx_number:
        for tx in OrderbyFee(GetPending()):
            if len(block.validating_list) < block.max_tx_number:
                logger.info(f"tx {tx.signature} is moved to validating list")

                block.validating_list.append(tx)
                DeletePending(tx)
            else:
                logger.info(
                    f"TX {tx.signature} is can not moved to validating list")
    else:
        logger.info("List is full")


def OrderbyFee(transactions: list):
    """
    Sorts transactions by fee.
    """

    transactions.sort(key=lambda x: x.transaction_fee, reverse=True)
    return transactions
