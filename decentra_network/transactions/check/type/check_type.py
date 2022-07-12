#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.log import get_logger

logger = get_logger("TRANSACTIONS")


def Check_Type(transaction):
    """
    Check if the transaction type is valid
    """
    if isinstance(transaction.sequance_number, int):
        logger.info("sequance_number is int")
    else:
        return False

    if isinstance(transaction.signature, str):
        logger.info("signature is str")
    else:
        return False

    if isinstance(transaction.fromUser, str):
        logger.info("fromUser is str")
    else:
        return False

    if isinstance(transaction.toUser, str):
        logger.info("toUser is str")
    else:
        return False

    if isinstance(transaction.data, str):
        logger.info("data is str")
    else:
        return False

    if isinstance(transaction.amount, (int, float)):
        logger.info("amount is int&&float")
    else:
        return False

    if isinstance(transaction.transaction_fee, (int, float)):
        logger.info("transaction_fee is int&&float")
    else:
        return False

    if isinstance(transaction.transaction_time, (int)):
        logger.info("transaction_time is int")
    else:
        return False

    return True
