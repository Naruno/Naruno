#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import hashlib


class Transaction:
    def __init__(self, sequance_number, signature, fromUser, toUser, data, amount, transaction_fee):
        self.sequance_number = sequance_number
        self.signature = signature
        self.fromUser = fromUser
        self.toUser = toUser
        self.data = data
        self.amount = amount
        self.transaction_fee = transaction_fee

    def dump_json(self):
        data = {
            "sequance_number": self.sequance_number,
            "signature": self.signature,
            "fromUser": self.fromUser,
            "toUser": self.toUser,
            "data": self.data,
            "amount": self.amount,
            "transaction_fee": self.transaction_fee
        }
        return data

    def get_hash(self, encoding="ascii"):
        transaction_data = json.dumps(self.dump_json()).encode(encoding)
        return hashlib.sha256(transaction_data).hexdigest()

    @staticmethod
    def load_json(data):
        return Transaction(data["sequance_number"],data["signature"],data["fromUser"],data["toUser"],data["data"],data["amount"],data["transaction_fee"])
