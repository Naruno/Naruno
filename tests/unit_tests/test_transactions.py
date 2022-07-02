#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from transactions.validate_transaction import ValidateTransaction
from transactions.tx_already_got import TXAlreadyGot
from transactions.transaction import Transaction
from transactions.save_to_my_transaction import SavetoMyTransaction
from transactions.save_my_transaction import SaveMyTransaction
from transactions.pending_to_validating import PendingtoValidating
from transactions.get_my_transaction import GetMyTransaction
from transactions.check.type.check_type import Check_Type
from transactions.check.len.check_len import Check_Len
from transactions.check.datas.check_datas import Check_Datas
from transactions.check.check_transaction import CheckTransaction
from transactions.change_transaction_fee import ChangeTransactionFee
from blockchain.block.block_main import Block
import unittest
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class Test_Transactions(unittest.TestCase):
    def test_get_my_transaction_non(self):
        backup = GetMyTransaction()
        SaveMyTransaction([])

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result, [])

    def test_get_my_transaction_not_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)

    def test_get_my_transaction_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=True)

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)

    def test_validate_my_transaction(self):
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

    def test_dumb_transaction(self):

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

    def test_load_transaction(self):

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

    def test_pending_to_validating_many_transaction(self):

        block = Block("", start_the_system=False)
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)

        PendingtoValidating(block)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(len(block.pendingTransaction), 1)

    def test_pending_to_validating_round_1_started(self):

        block = Block("", start_the_system=False)
        block.max_tx_number = 2
        block.raund_1_starting_time = 1

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)

        PendingtoValidating(block)

        self.assertEqual(len(block.validating_list), 0)
        self.assertEqual(len(block.pendingTransaction), 3)

    def test_pending_to_validating(self):

        block = Block("", start_the_system=False)
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)

        PendingtoValidating(block)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(len(block.pendingTransaction), 0)

    def test_tx_already_got_pending(self):

        block = Block("", start_the_system=False)

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)

        self.assertEqual(TXAlreadyGot(block, temp_transaction), True)

    def test_tx_already_got_validating(self):

        block = Block("", start_the_system=False)

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.validating_list.append(temp_transaction)

        result = TXAlreadyGot(block, temp_transaction)

        self.assertEqual(result, True)

    def test_tx_already_got_different(self):

        block = Block("", start_the_system=False)

        temp_transaction = Transaction(1, "1", "", "", "", 1, 1, 1)
        temp_transaction_2 = Transaction(2, "2", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)

        self.assertEqual(TXAlreadyGot(block, temp_transaction_2), False)

    def test_tx_already_got(self):

        block = Block("", start_the_system=False)

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        if not TXAlreadyGot(block, temp_transaction):
            block.pendingTransaction.append(temp_transaction)

        self.assertEqual(len(block.pendingTransaction), 1)

    def test_change_transaction_fee_increasing(self):

        block = Block("", start_the_system=False)
        first_transaction_fee = block.transaction_fee
        block.max_tx_number = 3
        block.default_optimum_transaction_number = 1
        block.default_increase_of_fee = 0.01
        block.default_transaction_fee = 0.02

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.validating_list.append(temp_transaction)
        block.validating_list.append(temp_transaction)

        ChangeTransactionFee(block)

        new_transaction_fee = block.transaction_fee

        self.assertEqual(first_transaction_fee, 0.02)
        self.assertEqual(new_transaction_fee, 0.05)

    def test_change_transaction_fee(self):

        block = Block("", start_the_system=False)
        first_transaction_fee = block.transaction_fee
        block.max_tx_number = 3
        block.default_optimum_transaction_number = 3
        block.default_increase_of_fee = 0.01
        block.default_transaction_fee = 0.02

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.validating_list.append(temp_transaction)

        ChangeTransactionFee(block)

        new_transaction_fee = block.transaction_fee

        self.assertEqual(first_transaction_fee, 0.02)
        self.assertEqual(new_transaction_fee, 0.02)

    def test_check_transaction(self):

        the_transaction_json = {
            "sequance_number": 1,
            "signature": "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        block = Block(the_transaction.fromUser, start_the_system=False)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, True)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.sequance_number = 2
        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.data = "test"
        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = "OMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg=="
        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.toUser = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg=="
        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        block2 = Block(the_transaction.fromUser, start_the_system=False)
        block2.max_tx_number = 2
        block2.transaction_delay_time = 60
        block2.minumum_transfer_amount = 1000
        block2.pendingTransaction.append(the_transaction)
        result = CheckTransaction(
            block2,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.toUser = 1
        result = CheckTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_string = ""
        for i in range(int((block.max_data_size / block.max_tx_number))):
            the_string += "a"
        the_transaction.data = the_string
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, True)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_string = "a"
        for i in range(int((block.max_data_size / block.max_tx_number))):
            the_string += "a"
        the_transaction.data = the_string
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        result = Check_Datas(
            block, the_transaction, custom_balance=10, custom_sequence_number=0
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = 10
        result = Check_Datas(
            block, the_transaction, custom_balance=100000, custom_sequence_number=0
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = 0.001
        result = Check_Datas(
            block, the_transaction, custom_balance=100000, custom_sequence_number=0
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        block3 = Block(the_transaction.fromUser, start_the_system=False)
        block3.max_tx_number = 2
        block3.transaction_delay_time = 60
        block3.minumum_transfer_amount = 1000
        the_transaction1 = Transaction.load_json(the_transaction_json)
        the_transaction1.signature = "a"
        block3.pendingTransaction.append(the_transaction1)
        result = Check_Datas(
            block3, the_transaction, custom_balance=100000, custom_sequence_number=0
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        result = Check_Datas(
            block, the_transaction, custom_balance=100000, custom_sequence_number=0
        )
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = 0.0001
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = 0.0001
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.sequance_number = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.signature = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.toUser = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.data = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_time = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)


unittest.main(exit=False)
