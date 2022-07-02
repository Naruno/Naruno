#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from transactions.change_transaction_fee import ChangeTransactionFee
from transactions.check.check_transaction import CheckTransaction
from transactions.propagating_the_tx import PropagatingtheTX
from transactions.transaction import Transaction


def SendTransactiontoTheBlock(
    block,
    sequance_number,
    signature,
    fromUser,
    toUser,
    transaction_fee,
    data,
    amount,
    transaction_time,
    transaction_sender=None,
):
    """
    This function creates a transaction and adds it
    to the validating list and other direction.
    """

    the_tx = Transaction(
        sequance_number=int(sequance_number),
        signature=str(signature),
        fromUser=str(fromUser),
        toUser=str(toUser),
        data=str(data),
        amount=float(amount),
        transaction_fee=float(transaction_fee),
        time_of_transaction=int(transaction_time),
    )
    checking = CheckTransaction(block, the_tx)

    if checking:
        block.pendingTransaction.append(the_tx)
        ChangeTransactionFee(block)
        block.save_block()

        PropagatingtheTX(the_tx)

        return the_tx
    else:
        return False
