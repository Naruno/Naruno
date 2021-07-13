#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import json
import hashlib


class Transaction:
    """
    The transaction class.

    Transaction class consists of 8 elements:
      * sequance_number: A number from the account class that ensures that
      each transaction is valid once.
      * signature: A signature proving that the sender approved the transaction.
      * fromUser: Sender's public key.
      * toUser: Receiver's address.
      * data: A text that can be written into the transaction.
      * amount: A int or float amount to be sent.
      * transaction_fee: Fee for transaction.
      * time: Sending time.
    """

    def __init__(self, sequance_number, signature, fromUser, toUser, data, amount, transaction_fee, time_of_transaction):
        self.sequance_number = sequance_number
        self.signature = signature
        self.fromUser = fromUser
        self.toUser = toUser
        self.data = data
        self.amount = amount
        self.transaction_fee = transaction_fee
        self.time = time_of_transaction

    def dump_json(self):
        """
        Returns a json containing the account's data.
        """

        data = {
            "sequance_number": self.sequance_number,
            "signature": self.signature,
            "fromUser": self.fromUser,
            "toUser": self.toUser,
            "data": self.data,
            "amount": self.amount,
            "transaction_fee": self.transaction_fee,
            "transaction_time": self.time
        }
        return data

    def get_hash(self, encoding="ascii"):
        """
        Returns a sha256 created using the dump_json() function.
        """

        transaction_data = json.dumps(self.dump_json()).encode(encoding)
        return hashlib.sha256(transaction_data).hexdigest()

    @staticmethod
    def load_json(data):
        """
        Returns the json data received with dump_json() as an object again.
        """

        return Transaction(
            data['sequance_number'],
            data['signature'],
            data['fromUser'],
            data['toUser'],
            data['data'],
            data['amount'],
            data['transaction_fee'],
            data['transaction_time'],
            )
