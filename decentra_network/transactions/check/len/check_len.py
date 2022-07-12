#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.log import get_logger

logger = get_logger("TRANSACTIONS")


def Check_Len(block, transaction):
    """
    Check if the transaction lenght is valid
    """

    if (block.max_data_size / block.max_tx_number) >= len(transaction.data):
        logger.info("Data len is true")
    else:
        return False

    if len(transaction.fromUser) == 120:
        logger.info("The from user is correct")
    else:
        return False

    if len(transaction.toUser) <= 40:
        logger.info("The to user is correct")
    else:
        return False

    decimal_amount = len(str(block.transaction_fee).split(".")[1])

    if len(str(transaction.amount).split(".")[1]) <= decimal_amount:
        logger.info("The decimal amount of transaction.amount is true.")
    else:
        return False

    if len(str(transaction.transaction_fee).split(".")[1]) <= decimal_amount:
        logger.info("The decimal amount of transaction.transaction_fee is true.")
    else:
        return False

    return True
