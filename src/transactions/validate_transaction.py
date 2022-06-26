#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from distutils.log import info
import pickle
import os

from lib.config_system import get_config
from config import MY_TRANSACTION_PATH

from transactions.get_my_transaction import GetMyTransaction
from transactions.save_my_transaction import SaveMyTransaction

from lib.log import get_logger

logger = get_logger("TRANSACTIONS")

def ValidateTransaction(tx):
    """
    Validates the transaction.
    """

    logger.info("Validating transaction: {}".format(tx))
    
    tx_list = GetMyTransaction()
    logger.info("My transactions: {}".format(tx_list))
    for i in tx_list:
        logger.info("myTransactionsig: {}".format(i[0].signature))
        logger.info("Transactionsig: {}".format(tx.signature))
        if i[0].signature == tx.signature:
            i[1] = True
    logger.info("My transactions2: {}".format(tx_list))
    SaveMyTransaction(tx_list)
