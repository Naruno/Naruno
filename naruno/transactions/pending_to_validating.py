#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import copy
import threading


from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger
from naruno.node.server.server import server
from naruno.transactions.pending.delete_pending import DeletePending
from naruno.transactions.pending.get_pending import GetPending
from naruno.transactions.pending.save_pending import SavePending

logger = get_logger("TRANSACTIONS")




def PendingtoValidating(block: Block):
    """
    Adds transactions to the verification list
    if there are suitable conditions.
    """
    logger.info("Pending to validating transfer process is started")
    first_validating_list_len = len(block.validating_list)
    first_max_tx_number = block.max_tx_number
    logger.debug(f"Currently tx amount: {first_validating_list_len}")
    logger.debug(f"Validating list capacity: {first_max_tx_number}")

    pending_list_txs = GetPending()
    logger.debug(f"Pending list is got: {pending_list_txs}")




    first_situation = copy.copy(block.validating_list)
    the_list_of_tx = pending_list_txs + first_situation
    
    block.validating_list = []

    logger.debug(f"Pending list is sent to server")
    if len(block.validating_list) < block.max_tx_number:
        logger.debug("List is not full")
        for tx in OrderbyFee(the_list_of_tx):
            logger.debug(f"TX {tx.signature} is checking")
            if len(block.validating_list) < block.max_tx_number:
                logger.info(f"tx {tx.signature} is moved to validating list")

                block.validating_list.append(tx)
                the_list_of_tx.remove(tx)
                if not tx in first_situation:
                    DeletePending(tx)

            else:
                logger.info(
                    f"TX {tx.signature} is can not moved to validating list")
    else:
        logger.info("List is full")
    
    for i in the_list_of_tx:
        if i in first_situation:
            SavePending(i)
        

    


def OrderbyFee(transactions: list):
    """
    Sorts transactions by fee.
    """

    the_transactions = copy.copy(transactions)
    the_transactions.sort(key=lambda x: x.signature, reverse=True)
    the_transactions.sort(key=lambda x: x.transaction_fee, reverse=True)
    return the_transactions
