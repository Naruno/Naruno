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

from accounts.get_balance import GetBalance
from accounts.get_sequance_number import GetSequanceNumber

from wallet.wallet import (
    Ecdsa,
    PublicKey,
    Signature
    )


def CreateTransaction(block, sequance_number, signature, fromUser, toUser, transaction_fee, data, amount, transaction_time, transaction_sender=None):
      """
      This function creates a transaction and adds it 
      to the validating list and other direction.
      """

      # Printing the info of tx
      dprint("\nCreating the transaction")
      dprint("***")
      dprint(sequance_number)
      dprint(signature)
      dprint(fromUser)
      dprint(toUser)
      dprint(data)
      dprint(amount)
      dprint("***\n")
      # End

      # Some data
      signature_class = Signature.fromBase64(signature)
      temp_signature = signature_class.toBase64()

      already_got = TXAlreadyGot(block, fromUser, sequance_number, temp_signature)
      # End

      # Validation
      dprint("\nValidation")
      if Ecdsa.verify((str(sequance_number)+str(fromUser)+str(toUser)+str(data)+str(amount)+str(transaction_fee)+str(transaction_time)), signature_class, PublicKey.fromPem(fromUser)) and not amount < block.minumum_transfer_amount and not transaction_fee < block.transaction_fee and not already_got and not (int(time.time()) - transaction_time) > 60:
        dprint("Signature is valid")

        dprint("Getsequancenumber: "+str(GetSequanceNumber(fromUser, block)+1))
        if sequance_number == (GetSequanceNumber(fromUser, block)+1):
          dprint("Sequance number is valid")

          balance = GetBalance(fromUser, block)

          if balance >= (float(amount)+float(transaction_fee)) and (balance - (float(amount)+float(transaction_fee))) > 2:
            dprint("Amount is valid")

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
            block.pendingTransaction.append(the_tx)
            ChangeTransactionFee(block)
            block.save_block()
            # End

            PropagatingtheTX(the_tx)

            return the_tx

      dprint(" Validation end")
      # End