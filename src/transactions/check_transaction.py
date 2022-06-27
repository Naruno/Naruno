#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from accounts.get_balance import GetBalance
from accounts.get_sequance_number import GetSequanceNumber
from lib.log import get_logger
from transactions.change_transaction_fee import ChangeTransactionFee
from transactions.propagating_the_tx import PropagatingtheTX
from transactions.transaction import Transaction
from transactions.tx_already_got import TXAlreadyGot
from wallet.ellipticcurve.ecdsa import Ecdsa
from wallet.ellipticcurve.publicKey import PublicKey
from wallet.ellipticcurve.signature import Signature

logger = get_logger("TRANSACTIONS")


def CheckTransaction(block, transaction):
    """
    This function checks the transaction.
    """

    logger.info(
        f"Checking the transaction started {block.sequance_number}:{transaction.signature}"
    )

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

    if (1000000 / block.max_tx_number) >= len(transaction.data):
        logger.info("Data len is true")
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

    if len(transaction.fromUser) == 120:
        logger.info("The from user is correct")
    else:
        return False

    if len(transaction.toUser) <= 40:
        logger.info("The to user is correct")
    else:
        return False

    if not TXAlreadyGot(block, transaction):
        logger.warning("The transaction is already got")
    else:
        return False

    if Ecdsa.verify(
        (str(transaction.sequance_number) + str(transaction.fromUser) +
         str(transaction.toUser) + str(transaction.data) +
         str(transaction.amount) + str(transaction.transaction_fee) +
         str(transaction.transaction_time)),
            Signature.fromBase64(transaction.signature),
            PublicKey.fromPem(transaction.fromUser),
    ):
        logger.info("The signature is valid")
    else:
        return False

    decimal_amount = len(str(block.transaction_fee).split(".")[1])

    if not len(str(transaction.amount).split(".")[1]) > decimal_amount:
        logger.info(f"The decimal amount of transaction.amount is true.")
    else:
        return False

    if not transaction.amount < block.minumum_transfer_amount:
        logger.info("Minimum transfer amount is reached")
    else:
        return False

    if not len(str(
            transaction.transaction_fee).split(".")[1]) > decimal_amount:
        logger.info(
            f"The decimal amount of transaction.transaction_fee is true.")
    else:
        return False

    if not transaction.transaction_fee < block.transaction_fee:
        logger.info("Transaction fee is reached")
    else:
        return False

    if not (int(time.time()) - transaction.transaction_time) > 60:
        logger.info("Transaction time is valid")
    else:
        return False

    if transaction.sequance_number == (
            GetSequanceNumber(transaction.fromUser) + 1):
        logger.info("Sequance number is valid")
    else:
        return False

    balance = GetBalance(block, transaction.fromUser)
    if balance >= (float(transaction.amount) +
                   float(transaction.transaction_fee)):
        logger.info("Balance is valid")
    else:
        return False

    if (balance -
        (float(transaction.amount) + float(transaction.transaction_fee))) > 2:
        logger.info("Balance is enough")
    else:
        return False

    for tx in block.pendingTransaction + block.validating_list:
        if (tx.fromUser == transaction.fromUser
                and tx.signature != transaction.signature):
            logger.info("Multiple transaction in one account")
            return False

    logger.info(
        f"Checking the transaction finished {block.sequance_number}:{transaction.signature}"
    )
    return True
