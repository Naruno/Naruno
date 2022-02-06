#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from accounts.get_balance import GetBalance
from accounts.get_sequance_number import GetSequanceNumber
from lib.mixlib import dprint
from transactions.change_transaction_fee import ChangeTransactionFee
from transactions.propagating_the_tx import PropagatingtheTX
from transactions.transaction import Transaction
from transactions.tx_already_got import TXAlreadyGot
from wallet.wallet import Ecdsa
from wallet.wallet import PublicKey
from wallet.wallet import Signature


def CheckTransaction(block, transaction):
    """
    This function checks the transaction.
    """

    dprint("\nValidation")

    validation = True

    if not TXAlreadyGot(block, transaction):
        dprint("The transaction is not already in the block")
    else:
        validation = False

    if Ecdsa.verify(
        (str(transaction.sequance_number) + str(transaction.fromUser) +
         str(transaction.toUser) + str(transaction.data) +
         str(transaction.amount) + str(transaction.transaction_fee) +
         str(transaction.transaction_time)),
            Signature.fromBase64(transaction.signature),
            PublicKey.fromPem(transaction.fromUser),
    ):
        dprint("The signature is valid")
    else:
        validation = False

    if not transaction.amount < block.minumum_transfer_amount:
        dprint("Minimum transfer amount is reached")
    else:
        validation = False

    if not transaction.transaction_fee < block.transaction_fee:
        dprint("Transaction fee is reached")
    else:
        validation = False

    if not (int(time.time()) - transaction.transaction_time) > 60:
        dprint("Transaction time is valid")
    else:
        validation = False

    if transaction.sequance_number == (
            GetSequanceNumber(transaction.fromUser, block) + 1):
        dprint("Sequance number is valid")
    else:
        validation = False

    balance = GetBalance(block, transaction.fromUser)
    if balance >= (float(transaction.amount) +
                   float(transaction.transaction_fee)):
        dprint("Balance is valid")
    else:
        validation = False

    if (balance -
        (float(transaction.amount) + float(transaction.transaction_fee))) > 2:
        dprint("Balance is enough")
    else:
        validation = False

    dprint("Validation end")

    return validation
