#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import time

from lib.mixlib import dprint

from transactions.transaction import Transaction
from transactions.propagating_the_tx import PropagatingtheTX
from transactions.tx_already_got import TXAlreadyGot
from transactions.change_transaction_fee import ChangeTransactionFee
from transaction.check_transaction import CheckTransaction

from accounts.get_balance import GetBalance
from accounts.get_sequance_number import GetSequanceNumber

from wallet.wallet import (
    Ecdsa,
    PublicKey,
    Signature
    )


def SendTransactiontoTheBlock(block, sequance_number, signature, fromUser, toUser, transaction_fee, data, amount, transaction_time, transaction_sender=None):
    """
    This function creates a transaction and adds it 
    to the validating list and other direction.
    """

    # Some data
    signature_class = Signature.fromBase64(signature)
    temp_signature = signature_class.toBase64()


    # Local saving
    the_tx = Transaction(
      sequance_number= sequance_number,
      signature=temp_signature,
      fromUser= fromUser,
      toUser=toUser,
      data = data,
      amount = amount,
      transaction_fee= transaction_fee,
      time_of_transaction = transaction_time
    )
    print(the_tx.dump_json())


    if CheckTransaction(the_tx):
      block.pendingTransaction.append(the_tx)
      ChangeTransactionFee(block)
      block.save_block()

      PropagatingtheTX(the_tx)

      return the_tx
