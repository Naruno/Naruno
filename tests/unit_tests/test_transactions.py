#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..","..","src"))
from transactions.get_my_transaction import GetMyTransaction
from transactions.save_my_transaction import SaveMyTransaction
from transactions.save_to_my_transaction import SavetoMyTransaction
from transactions.validate_transaction import ValidateTransaction
from transactions.transaction import Transaction

class Test_Settings(unittest.TestCase):

    def test_1_get_my_transaction_non(self):
        backup = GetMyTransaction()
        SaveMyTransaction([])

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result, [])

    def test_2_get_my_transaction_not_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)
        
        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)

    def test_3_get_my_transaction_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=True)
        
        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)

    def test_4_validate_my_transaction(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)
        
        result = GetMyTransaction()

        ValidateTransaction(new_transaction)

        result_2 = GetMyTransaction()


        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)

        self.assertEqual(result_2[0][0].signature, new_transaction.signature)
        self.assertEqual(result_2[0][1], True)

    def test_5_dumb_transaction(self):

        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        
        dumped_transaction = new_transaction.dump_json()
        
        the_json = {
            "sequance_number": 1,
            "signature": "",
            "fromUser": "",
            "toUser": "",
            "data": "",
            "amount": 1,
            "transaction_fee": 1,
            "transaction_time": 1,
        }

        self.assertEqual(dumped_transaction, the_json)


    def test_5_load_transaction(self):

        the_json = {
            "sequance_number": 1,
            "signature": "",
            "fromUser": "",
            "toUser": "",
            "data": "",
            "amount": 1,
            "transaction_fee": 1,
            "transaction_time": 1,
        }

        loaded_transaction = Transaction.load_json(the_json)

        loaded_transaction_json = loaded_transaction.dump_json()


        self.assertEqual(loaded_transaction_json, the_json)




unittest.main(exit=False)
