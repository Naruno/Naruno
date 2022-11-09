#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger
from decentra_network.transactions.transaction import Transaction

logger = get_logger("TRANSACTIONS")


def Check_Len(block: Block, transaction: Transaction):
    """
    Check if the transaction lenght is valid
    """

    if (block.max_data_size / block.max_tx_number) >= len(transaction.data):
        pass
    else:
        logger.debug("Transaction data len is not correct")
        return False

    if len(transaction.fromUser) == 120:
        pass
    else:
        logger.debug("The from user is not correct")
        return False

    if len(transaction.toUser) <= 40:
        pass
    else:
        logger.debug("The to user is not correct")
        return False

    decimal_amount = len(str(block.transaction_fee).split(".")[1])

    if type(transaction.amount) == float:
        if len(str(transaction.amount).split(".")[1]) <= decimal_amount:
            pass
        else:
            logger.debug(
                "The decimal amount of transaction.amount is not true.")
            return False

    if type(transaction.transaction_fee) == float:
        if len(str(
                transaction.transaction_fee).split(".")[1]) <= decimal_amount:
            pass
        else:
            logger.debug(
                "The decimal amount of transaction.transaction_fee is not true."
            )
            return False

    if transaction.amount <= block.coin_amount:
        pass
    else:
        logger.debug("The amount is not true")
        return False

    if transaction.transaction_fee <= block.coin_amount:
        pass
    else:
        logger.debug("The transaction fee is not true")
        return False

    return True
