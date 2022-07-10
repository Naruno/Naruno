#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import sys
import time
import unittest

from accounts.account import Account
from blockchain.block.block_main import Block
from blockchain.block.change_transaction_fee import ChangeTransactionFee
from transactions.check.check_transaction import CheckTransaction
from transactions.check.datas.check_datas import Check_Datas
from transactions.check.len.check_len import Check_Len
from transactions.check.type.check_type import Check_Type
from transactions.get_transaction import GetTransaction
from transactions.my_transactions.get_my_transaction import GetMyTransaction
from transactions.my_transactions.save_my_transaction import SaveMyTransaction
from transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from transactions.pending_to_validating import PendingtoValidating
from transactions.process_the_transaction import ProccesstheTransaction
from transactions.send import send
from transactions.transaction import Transaction

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))


class Test_Transactions(unittest.TestCase):
    def test_get_my_transaction_non(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

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

        block = Block("")
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)

        PendingtoValidating(block)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(len(block.pendingTransaction), 1)

    def test_pending_to_validating_round_1_started(self):

        block = Block("")
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

        block = Block("")
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        block.pendingTransaction.append(temp_transaction)
        block.pendingTransaction.append(temp_transaction)

        PendingtoValidating(block)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(len(block.pendingTransaction), 0)

    def test_change_transaction_fee_increasing(self):

        block = Block("")
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

        block = Block("")
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

    def test_check_transaction_true(self):

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
        block = Block(the_transaction.fromUser)
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

    def test_check_transaction_false_seuance_number(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

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

    def test_check_transaction_false_signature(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

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

    def test_check_transaction_false_fromUser(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

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

    def test_check_transaction_false_toUser(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

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

    def test_check_transaction_already_got(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000
        block.pendingTransaction.append(the_transaction)
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_bad_type_fromUser(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

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

    def test_check_transaction_true_len_data(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_string = ""
        for i in range(int((block.max_data_size / block.max_tx_number))):
            the_string += "a"
        the_transaction.data = the_string
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, True)

    def test_check_transaction_false_len_data(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_string = "a"
        for i in range(int((block.max_data_size / block.max_tx_number))):
            the_string += "a"
        the_transaction.data = the_string
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_balance(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=10,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_false_amount(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = 10
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_false_transaction_fee(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = 0.001
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_multiple_transaction_from_one_user(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000
        the_transaction1 = Transaction.load_json(the_transaction_json)
        the_transaction1.signature = "a"
        block.pendingTransaction.append(the_transaction1)
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_wrong_time(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        result = Check_Datas(
            block, the_transaction, custom_balance=100000, custom_sequence_number=0
        )
        self.assertEqual(result, False)

    def test_check_transaction_false_amount_decimal(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = 0.001
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_transaction_fee_decimal(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = 0.001
        result = Check_Len(block, the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_sequance_number_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.sequance_number = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_signature_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.signature = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_fromUser_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_toUser_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.toUser = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_data_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.data = 1
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_amount_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.amount = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_transaction_fee_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_fee = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_transaction_time_type(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.transaction_time = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_send_false_amount_type(self):
        block = Block("onur")
        result = send(block, "123", "onur", "atakan", "ulusoy")
        self.assertEqual(result, False)

    def test_send_false_amount_type_negative(self):
        block = Block("onur")
        result = send(block, "123", "onur", -500, "ulusoy")
        self.assertEqual(result, False)

    def test_send_false_big_data(self):
        block = Block("onur")
        data = "a"
        for i in range(int((block.max_data_size / block.max_tx_number))):
            data += "a"
        result = send(block, "123", "onur", 500, data)
        self.assertEqual(result, False)

    def test_send_false_decimal_amount(self):
        block = Block("onur")
        result = send(block, "123", "onur", 500.001, "ulusoy")
        self.assertEqual(result, False)

    def test_send_false_amount_lower_than_minumum(self):
        block = Block("onur")
        result = send(block, "123", "onur", 500, "ulusoy")
        self.assertEqual(result, False)

    def test_send_false_pass(self):
        block = Block("onur")
        result = send(block, "1235", "onur", 5000, "ulusoy")
        self.assertEqual(result, False)

    def test_send_false_check(self):
        block = Block("onur")
        result = send(block, "123", "onur", 5000, "ulusoy", custom_balance=5)
        self.assertEqual(result, False)

    def test_send_true(self):
        block = Block("onur")
        result = send(
            block,
            "123",
            "onur",
            5000,
            "ulusoy",
            custom_current_time=(int(time.time()) + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertNotEqual(result, False)

    def test_get_transaction_false(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        result = GetTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=1,
        )
        self.assertEqual(result, False)

    def test_get_transaction_true(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        result = GetTransaction(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )
        self.assertEqual(result, True)

    def test_ProccesstheTransaction_validating_list(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000
        the_transaction_2 = Transaction.load_json(the_transaction_json)
        the_transaction_2.fromUser = "A"
        block.validating_list = [the_transaction, the_transaction_2]
        account_list = [Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000)]
        result = ProccesstheTransaction(block, account_list)
        self.assertEqual(block.validating_list, [the_transaction_2, the_transaction])

    def test_ProccesstheTransaction_account_list(self):

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
        block = Block(the_transaction.fromUser)
        block.max_tx_number = 2
        block.transaction_delay_time = 60
        block.minumum_transfer_amount = 1000

        the_transaction_2 = Transaction.load_json(the_transaction_json)
        the_transaction_2.fromUser = "B"
        the_transaction_2.toUser = "d10d419bae75549222c5ffead625a9e0246ad3e6"

        the_transaction_3 = Transaction.load_json(the_transaction_json)
        the_transaction_3.fromUser = "C"

        the_transaction_4 = Transaction.load_json(the_transaction_json)
        the_transaction_4.fromUser = "A"

        the_transaction_5 = Transaction.load_json(the_transaction_json)
        the_transaction_5.fromUser = "Atakan"
        the_transaction_5.toUser = "teaaast"

        block.validating_list = [
            the_transaction,
            the_transaction_2,
            the_transaction_3,
            the_transaction_4,
            the_transaction_5,
        ]
        account_list = [
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000),
            Account("73cd109827c0de9fa211c0d062eab13584ea6bb8", 100000),
            Account("08fe9bfc6521565c601a3785c5f5fb0a406279e6", 100000),
            Account("6a4236cba1002b2919651677c7c520b67627aa2a", 100000),
            Account("d10d419bae75549222c5ffead625a9e0246ad3e6", 100000),
        ]
        result = ProccesstheTransaction(block, account_list)
        self.assertEqual(len(account_list), 7)
        true_list = [
            the_transaction_4,
            the_transaction_5,
            the_transaction_2,
            the_transaction_3,
            the_transaction,
        ]
        self.assertEqual(block.validating_list, true_list)
        self.assertEqual(account_list[0].balance, 100000 - 5000 - 0.02)
        self.assertEqual(
            account_list[0].Address, "2ffd1f6bed8614f4cd01fc7159ac950604272773"
        )
        self.assertEqual(account_list[0].sequance_number, 1)

        self.assertEqual(account_list[1].balance, 94999.98)
        self.assertEqual(
            account_list[1].Address, "73cd109827c0de9fa211c0d062eab13584ea6bb8"
        )
        self.assertEqual(account_list[1].sequance_number, 1)

        self.assertEqual(account_list[2].balance, 94999.98)
        self.assertEqual(
            account_list[2].Address, "08fe9bfc6521565c601a3785c5f5fb0a406279e6"
        )
        self.assertEqual(account_list[2].sequance_number, 1)

        self.assertEqual(account_list[3].balance, 94999.98)
        self.assertEqual(
            account_list[3].Address, "6a4236cba1002b2919651677c7c520b67627aa2a"
        )
        self.assertEqual(account_list[3].sequance_number, 1)

        self.assertEqual(account_list[4].balance, 99999.98)
        self.assertEqual(
            account_list[4].Address, "d10d419bae75549222c5ffead625a9e0246ad3e6"
        )
        self.assertEqual(account_list[4].sequance_number, 1)

        self.assertEqual(account_list[5].balance, 55000)
        self.assertEqual(account_list[5].Address, "onur")
        self.assertEqual(account_list[5].sequance_number, 0)

        self.assertEqual(account_list[6].balance, 5000)
        self.assertEqual(account_list[6].Address, "teaaast")
        self.assertEqual(account_list[6].sequance_number, 0)


unittest.main(exit=False)
