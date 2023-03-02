#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import hashlib
import json


class Transaction:
    """
    The transaction class.

    Transaction class consists of 8 elements:
      * sequence_number: A number from the account class that ensures that
      each transaction is valid once.
      * signature: A signature proving that the sender approved the transaction.
      * fromUser: Sender's public key.
      * toUser: Receiver's address.
      * data: A text that can be written into the transaction.
      * amount: A int or float amount to be sent.
      * transaction_fee: Fee for transaction.
      * time: Sending time.
    """

    def __init__(
        self,
        sequence_number,
        signature,
        fromUser,
        toUser,
        data,
        amount,
        transaction_fee,
        time_of_transaction,
    ):
        self.sequence_number = int(sequence_number)
        self.signature = str(signature)
        self.fromUser = str(fromUser)
        self.toUser = str(toUser)
        self.data = str(data)
        self.amount = float(amount)
        self.transaction_fee = float(transaction_fee)
        self.transaction_time = int(time_of_transaction)

    def dump_json(self):
        """
        Returns a json containing the account's data.
        """
        return self.__dict__

    @staticmethod
    def load_json(data):
        """
        Returns the json data received with dump_json() as an object again.
        """

        the_transaction_json = json.loads(json.dumps(data))
        the_transaction = Transaction(1, 1, 1, 1, 1, 1, 1, 1)
        the_transaction.__dict__ = the_transaction_json
        return the_transaction
