#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import sys
from ast import Delete

from requests import delete

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import time
import unittest

from decentra_network.accounts.account import Account
from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.change_transaction_fee import \
    ChangeTransactionFee
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.transactions.check.check_transaction import \
    CheckTransaction
from decentra_network.transactions.check.datas.check_datas import Check_Datas
from decentra_network.transactions.check.len.check_len import Check_Len
from decentra_network.transactions.check.type.check_type import Check_Type
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.transactions.pending.delete_pending import DeletePending
from decentra_network.transactions.pending.get_pending import (GetPending,
                                                               GetPendingLen)
from decentra_network.transactions.pending.save_pending import SavePending
from decentra_network.transactions.pending_to_validating import \
    PendingtoValidating
from decentra_network.transactions.process_the_transaction import \
    ProccesstheTransaction
from decentra_network.transactions.send import send
from decentra_network.transactions.transaction import Transaction


class Test_Transactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

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

    def test_get_my_transaction_not_sended(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_sended(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        result = GetMyTransaction()

        SaveMyTransaction(backup)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_sended(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "af", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False)

        new_transaction = Transaction(1, "a", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        result = GetMyTransaction(sended=True)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "bf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=False)

        new_transaction = Transaction(1, "b", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=True)

        result = GetMyTransaction(validated=True)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)

    def test_get_my_transaction_just_sended_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "cf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "cff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "c", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        result = GetMyTransaction(sended=True, validated=True)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_sended_no_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "df", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "dff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "d", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        result = GetMyTransaction(sended=True, validated=False)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_received(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "ef", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        new_transaction = Transaction(1, "e", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False)

        result = GetMyTransaction(sended=False)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_just_received_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "ff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "fff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "f", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        result = GetMyTransaction(sended=False, validated=True)

        SaveMyTransaction(backup)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_just_received_no_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction({})

        new_transaction = Transaction(1, "gf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "gff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "g", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        result = GetMyTransaction(sended=False, validated=False)

        SaveMyTransaction(backup)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)
        self.assertEqual(result[0][2], False)

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

        temp_transaction = Transaction(1, "1", "", "", "", 1, 1, 1)
        temp_transaction_2 = Transaction(1, "2", "", "", "", 1, 1, 1)
        temp_transaction_3 = Transaction(1, "3", "", "", "", 1, 1, 1)

        SavePending(temp_transaction)
        SavePending(temp_transaction_2)
        SavePending(temp_transaction_3)

        PendingtoValidating(block)

        pending_transactions = GetPending()

        transaction_1_true = any(
            element.signature == temp_transaction.signature
            for element in pending_transactions
        )
        transaction_2_true = any(
            element.signature == temp_transaction_2.signature
            for element in pending_transactions
        )
        transaction_3_true = any(
            element.signature == temp_transaction_3.signature
            for element in pending_transactions
        )

        DeletePending(temp_transaction)
        DeletePending(temp_transaction_2)
        DeletePending(temp_transaction_3)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(transaction_1_true, False)
        self.assertEqual(transaction_2_true, False)
        self.assertEqual(transaction_3_true, True)

    def test_pending_to_validating(self):

        block = Block("")
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "77", "", "", "", 1, 1, 1)
        temp_transaction_2 = Transaction(1, "88", "", "", "", 1, 1, 1)

        SavePending(temp_transaction)
        SavePending(temp_transaction_2)

        PendingtoValidating(block)

        pending_transactions = GetPending()

        transaction_1_true = any(
            element.signature == temp_transaction.signature
            for element in pending_transactions
        )
        transaction_2_true = any(
            element.signature == temp_transaction_2.signature
            for element in pending_transactions
        )

        DeletePending(temp_transaction)
        DeletePending(temp_transaction_2)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(transaction_1_true, False)
        self.assertEqual(transaction_2_true, False)

    def test_change_transaction_fee_increasing(self):

        block = Block("")
        first_transaction_fee = block.transaction_fee
        block.max_tx_number = 3
        block.default_optimum_transaction_number = 1
        block.default_increase_of_fee = 0.01
        block.default_transaction_fee = 0.02

        temp_transaction = Transaction(1, "9", "", "", "", 1, 1, 1)

        block.validating_list.append(temp_transaction)
        block.validating_list.append(temp_transaction)

        ChangeTransactionFee(
            block, custom_pending_transaction_len=len([temp_transaction])
        )

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

        temp_transaction = Transaction(1, "10", "", "", "", 1, 1, 1)

        block.validating_list.append(temp_transaction)

        ChangeTransactionFee(
            block, custom_pending_transaction_len=len([temp_transaction])
        )

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
        SavePending(the_transaction)
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        DeletePending(the_transaction)
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
        the_transaction1.signature = "11"
        SavePending(the_transaction1)
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        DeletePending(the_transaction1)
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

    def test_check_transaction_false_amount_bigger_than_coin_amount(self):

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
        the_transaction.amount = block.coin_amount + 1
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

    def test_check_transaction_false_transaction_fee_bigger_than_coin_amount(self):

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
        the_transaction.transaction_fee = block.coin_amount + 1
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
        result = send("123", "onur", amount="atakan", data="1ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_amount_type_negative(self):
        block = Block("onur")
        result = send("123", "onur", amount=-500, data="2ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_big_data(self):
        block = Block("onur")
        data = "a"
        for i in range(int((block.max_data_size / block.max_tx_number))):
            data += "a"
        result = send("123", "onur", amount=500, data=data, block=block)
        self.assertEqual(result, False)

    def test_send_false_decimal_amount(self):
        block = Block("onur")
        result = send("123", "onur", amount=500.001, data="3ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_amount_lower_than_minumum(self):
        block = Block("onur")
        result = send("123", "onur", amount=500, data="4ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_pass(self):
        block = Block("onur")
        result = send("1235", "onur", amount=5000, data="5ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_check(self):
        block = Block("onur")
        result = send(
            "123", "onur", amount=5000, data="6ulusoy", custom_balance=5, block=block
        )
        self.assertEqual(result, False)

    def test_send_true(self):
        block = Block("onur")
        result = send(
            "123",
            "onur",
            amount=5000,
            data="77ulusoy",
            custom_current_time=(int(time.time()) + 5),
            custom_sequence_number=0,
            custom_balance=100000,
            block=block,
        )

        self.assertNotEqual(result, False)
        DeletePending(result)

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
        DeletePending(the_transaction)
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
        temp_path = "db/test_ProccesstheTransaction_validating_list.db"

        SaveAccounts(
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000), temp_path
        )
        account_list = GetAccounts(temp_path)
        result = ProccesstheTransaction(
            block, account_list, custom_TEMP_ACCOUNTS_PATH=temp_path
        )
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

        temp_path = "db/test_ProccesstheTransaction_account_list.db"

        SaveAccounts(
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000), temp_path
        )
        SaveAccounts(
            Account("73cd109827c0de9fa211c0d062eab13584ea6bb8", 100000), temp_path
        )
        SaveAccounts(
            Account("08fe9bfc6521565c601a3785c5f5fb0a406279e6", 100000), temp_path
        )
        SaveAccounts(
            Account("6a4236cba1002b2919651677c7c520b67627aa2a", 100000), temp_path
        )
        SaveAccounts(
            Account("d10d419bae75549222c5ffead625a9e0246ad3e6", 100000), temp_path
        )

        account_list = GetAccounts(temp_path)

        result = ProccesstheTransaction(
            block, account_list, custom_TEMP_ACCOUNTS_PATH=temp_path
        )
        account_list = GetAccounts(temp_path)
        account_list.execute(f"SELECT * FROM account_list")
        account_list = account_list.fetchall()
        self.assertEqual(len(account_list), 7)
        true_list = [
            the_transaction_4,
            the_transaction_5,
            the_transaction_2,
            the_transaction_3,
            the_transaction,
        ]
        self.assertEqual(block.validating_list, true_list)
        self.assertEqual(account_list[0][2], 100000 - 5000 - 0.02)
        self.assertEqual(account_list[0][0], "2ffd1f6bed8614f4cd01fc7159ac950604272773")
        self.assertEqual(account_list[0][1], 1)

        self.assertEqual(account_list[1][2], 94999.98)
        self.assertEqual(account_list[1][0], "73cd109827c0de9fa211c0d062eab13584ea6bb8")
        self.assertEqual(account_list[1][1], 1)

        self.assertEqual(account_list[2][2], 94999.98)
        self.assertEqual(account_list[2][0], "08fe9bfc6521565c601a3785c5f5fb0a406279e6")
        self.assertEqual(account_list[2][1], 1)

        self.assertEqual(account_list[3][2], 94999.98)
        self.assertEqual(account_list[3][0], "6a4236cba1002b2919651677c7c520b67627aa2a")
        self.assertEqual(account_list[3][1], 1)

        self.assertEqual(account_list[4][2], 99999.98)
        self.assertEqual(account_list[4][0], "d10d419bae75549222c5ffead625a9e0246ad3e6")
        self.assertEqual(account_list[4][1], 1)

        self.assertEqual(account_list[5][2], 15000)
        self.assertEqual(account_list[5][0], "onur")
        self.assertEqual(account_list[5][1], 0)

        self.assertEqual(account_list[6][2], 5000)
        self.assertEqual(account_list[6][0], "teaaast")
        self.assertEqual(account_list[6][1], 0)

    def test_SavePending_GetPending_DeletePending(self):
        the_transaction_json = {
            "sequance_number": 1,
            "signature": "test_SavePending_GetPending",
            "fromUser": "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)

        SavePending(the_transaction)
        pending_list = GetPending()
        result = False
        for pending in pending_list:
            if pending.signature == the_transaction.signature:
                result = True

        DeletePending(the_transaction)
        self.assertEqual(result, True)


unittest.main(exit=False)
