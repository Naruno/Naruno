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
        pass
    else:
        logger.debug("sequance_number is not int")
        return False

    if isinstance(transaction.signature, str):
        pass
    else:
        logger.debug("signature is not str")
        return False

    if isinstance(transaction.fromUser, str):
        pass
    else:
        logger.debug("fromUser is not str")
        return False

    if isinstance(transaction.toUser, str):
        pass
    else:
        logger.debug("toUser is not str")
        return False

    if isinstance(transaction.data, str):
        pass
    else:
        logger.debug("data is not str")
        return False

    if isinstance(transaction.amount, (int, float)):
        pass
    else:
        logger.debug("amount is not int&&float")
        return False

    if transaction.amount >= 0:
        pass
    else:
        logger.debug("amount is negative")
        return False

    if isinstance(transaction.transaction_fee, (int, float)):
        pass
    else:
        logger.debug("transaction_fee is not int&&float")
        return False

    if isinstance(transaction.transaction_time, (int)):
        pass
    else:
        logger.debug("transaction_time is not int")
        return False

    return True
