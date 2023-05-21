#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import time
import unittest
import zipfile

from naruno.accounts.account import Account
from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.get_balance import GetBalance
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import (GetBlockshash,
                                                 GetBlockshash_part,
                                                 SaveBlockshash_part)
from naruno.blockchain.block.change_transaction_fee import ChangeTransactionFee
from naruno.blockchain.block.get_block_from_blockchain_db import \
    GetBlockstoBlockchainDB
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.consensus.finished.finished_main import finished_main
from naruno.lib.clean_up import CleanUp_tests
from naruno.lib.mix.merkle_root import MerkleTree
from naruno.lib.settings_system import save_settings, the_settings
from naruno.transactions.check.check_transaction import CheckTransaction
from naruno.transactions.check.datas.check_datas import Check_Datas
from naruno.transactions.check.len.check_len import Check_Len
from naruno.transactions.check.type.check_type import Check_Type
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.my_transactions.check_proof import CheckProof
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.get_proof import GetProof
from naruno.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from naruno.transactions.pending.delete_pending import DeletePending
from naruno.transactions.pending.get_pending import GetPending, GetPendingLen
from naruno.transactions.pending.save_pending import SavePending
from naruno.transactions.pending_to_validating import PendingtoValidating
from naruno.transactions.process_the_transaction import ProccesstheTransaction
from naruno.transactions.send import send
from naruno.transactions.transaction import Transaction
from naruno.wallet.wallet_import import Address, wallet_import


class Test_Transactions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    def test_get_my_transaction_non(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        result = GetMyTransaction()

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result, [])

    def test_get_my_transaction_not_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)

        result = GetMyTransaction()

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)

    def test_get_my_transaction_validated(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=True)

        result = GetMyTransaction()

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)

    def test_get_my_transaction_not_sended(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction)

        result = GetMyTransaction()

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_sended(self):
        backup = GetMyTransaction()
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        result = GetMyTransaction()

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_sended(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "af", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False)

        new_transaction = Transaction(1, "a", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        result = GetMyTransaction(sended=True)

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "bf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=False)

        new_transaction = Transaction(1, "b", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, validated=True)

        result = GetMyTransaction(validated=True)

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)

    def test_get_my_transaction_just_sended_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "cf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "cff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "c", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        result = GetMyTransaction(sended=True, validated=True)

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_sended_no_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "df", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "dff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "d", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        result = GetMyTransaction(sended=True, validated=False)

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)
        self.assertEqual(result[0][2], True)

    def test_get_my_transaction_just_received(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "ef", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True)

        new_transaction = Transaction(1, "e", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False)

        result = GetMyTransaction(sended=False)

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_just_received_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "ff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=True)

        new_transaction = Transaction(1, "fff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        new_transaction = Transaction(1, "f", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        result = GetMyTransaction(sended=False, validated=True)

        SaveMyTransaction(backup, clear=True)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], True)
        self.assertEqual(result[0][2], False)

    def test_get_my_transaction_just_received_no_validated(self):
        backup = GetMyTransaction()
        SaveMyTransaction([], clear=True)

        new_transaction = Transaction(1, "gf", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=True, validated=False)

        new_transaction = Transaction(1, "gff", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=True)

        new_transaction = Transaction(1, "g", "", "", "", 1, 1, 1)
        SavetoMyTransaction(new_transaction, sended=False, validated=False)

        result = GetMyTransaction(sended=False, validated=False)

        SaveMyTransaction(backup, clear=True)
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

        SaveMyTransaction(backup, clear=True)
        self.assertEqual(result[0][0].signature, new_transaction.signature)
        self.assertEqual(result[0][1], False)

        self.assertEqual(result_2[0][0].signature, new_transaction.signature)
        self.assertEqual(result_2[0][1], True)

    def test_dumb_transaction(self):
        new_transaction = Transaction(1, "", "", "", "", 1, 1, 1)

        dumped_transaction = new_transaction.dump_json()

        the_json = {
            "sequence_number": 1,
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
            "sequence_number": 1,
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

        temp_transaction = Transaction(1, "1", "", "", "", 1, 15, 1)
        temp_transaction_2 = Transaction(1, "2", "", "", "", 1, 10, 1)
        temp_transaction_3 = Transaction(1, "3", "", "", "", 1, 5, 1)

        SavePending(temp_transaction)
        SavePending(temp_transaction_2)
        SavePending(temp_transaction_3)

        PendingtoValidating(block)

        pending_transactions = GetPending()

        transaction_1_true = any(
            element.signature == temp_transaction.signature
            for element in pending_transactions)
        transaction_2_true = any(
            element.signature == temp_transaction_2.signature
            for element in pending_transactions)
        transaction_3_true = any(
            element.signature == temp_transaction_3.signature
            for element in pending_transactions)

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
            for element in pending_transactions)
        transaction_2_true = any(
            element.signature == temp_transaction_2.signature
            for element in pending_transactions)

        DeletePending(temp_transaction)
        DeletePending(temp_transaction_2)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(transaction_1_true, False)
        self.assertEqual(transaction_2_true, False)

    def test_pending_to_validating_full_list(self):
        block = Block("")
        block.validating_list = [
            Transaction(1, "717", "", "", "", 1, 1, 1),
            Transaction(1, "7b7", "", "", "", 1, 1, 1),
        ]
        block.max_tx_number = 2

        temp_transaction = Transaction(1, "77", "", "", "", 1, 1, 1)
        temp_transaction_2 = Transaction(1, "88", "", "", "", 1, 1, 1)

        SavePending(temp_transaction)
        SavePending(temp_transaction_2)

        PendingtoValidating(block)

        pending_transactions = GetPending()

        transaction_1_true = any(
            element.signature == temp_transaction.signature
            for element in pending_transactions)
        transaction_2_true = any(
            element.signature == temp_transaction_2.signature
            for element in pending_transactions)

        DeletePending(temp_transaction)
        DeletePending(temp_transaction_2)

        self.assertEqual(len(block.validating_list), 2)
        self.assertEqual(transaction_1_true, True)
        self.assertEqual(transaction_2_true, True)

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

        ChangeTransactionFee(block,
                             custom_pending_transaction_len=len(
                                 [temp_transaction]))

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

        ChangeTransactionFee(block,
                             custom_pending_transaction_len=len(
                                 [temp_transaction]))

        new_transaction_fee = block.transaction_fee

        self.assertEqual(first_transaction_fee, 0.02)
        self.assertEqual(new_transaction_fee, 0.02)

    def test_check_transaction_true(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        the_transaction.sequence_number = 2
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        the_transaction.amount = 0
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
        )
        self.assertEqual(result, False)

    def test_check_transaction_false_amount_high_account(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        a_account = Account(the_transaction.toUser, 1000)
        SaveAccounts([a_account],
                     "db/test_check_transaction_false_amount_high_account.db")
        the_accounts = GetAccounts(
            "db/test_check_transaction_false_amount_high_account.db")
        result = Check_Datas(
            block,
            the_transaction,
            custom_current_time=(the_transaction.transaction_time + 5),
            custom_balance=100000,
            custom_sequence_number=0,
            custom_account_list=the_accounts,
        )
        self.assertEqual(result, True)

    def test_check_transaction_false_transaction_fee(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        result = Check_Datas(block,
                             the_transaction,
                             custom_balance=100000,
                             custom_sequence_number=0)
        self.assertEqual(result, False)

    def test_check_transaction_false_amount_decimal(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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

    def test_check_transaction_false_transaction_fee_bigger_than_coin_amount(
            self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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

    def test_check_transaction_false_sequence_number_type(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        the_transaction.sequence_number = "1"
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_signature_type(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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

    def test_check_transaction_false_amount_type_str(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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

    def test_check_transaction_false_amount_type_negative(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        the_transaction.amount = -15.0
        result = Check_Type(the_transaction)
        self.assertEqual(result, False)

    def test_check_transaction_false_transaction_fee_type(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
        result = send("123",
                      "onur",
                      amount="atakan",
                      data="1ulusoy",
                      block=block)
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
        result = send("123",
                      "onur",
                      amount=500.001,
                      data="3ulusoy",
                      block=block)
        self.assertEqual(result, False)

    def test_send_false_pass(self):
        block = Block("onur")
        result = send("1235", "onur", amount=5000, data="5ulusoy", block=block)
        self.assertEqual(result, False)

    def test_send_false_check(self):
        block = Block("onur")
        result = send("123",
                      "onur",
                      amount=5000,
                      data="6ulusoy",
                      custom_balance=5,
                      block=block)
        self.assertEqual(result, False)

    def test_send_true_just_data(self):
        block = Block("onur")
        a_account = Account("onur", 1000)
        SaveAccounts([a_account],
                     "db/test_check_transaction_false_amount_high_account.db")
        the_accounts = GetAccounts(
            "db/test_check_transaction_false_amount_high_account.db")
        result = send(
            "123",
            "onur",
            data="77ulusoy",
            custom_current_time=(int(time.time()) + 5),
            custom_sequence_number=0,
            custom_balance=100000,
            block=block,
            custom_account_list=the_accounts,
        )

        self.assertNotEqual(result, False)
        self.assertEqual(result.amount, 0)
        DeletePending(result)

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
        self.assertEqual(result.amount, 5000)
        DeletePending(result)

    def test_get_transaction_false(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000),
            temp_path)
        account_list = GetAccounts(temp_path)
        result = ProccesstheTransaction(block,
                                        account_list,
                                        custom_TEMP_ACCOUNTS_PATH=temp_path,
                                        dont_clean=True)
        self.assertEqual(len(block.validating_list), 3)
        self.assertEqual(block.validating_list[0], the_transaction_2)
        self.assertEqual(block.validating_list[2].toUser, block.fee_address)
        self.assertEqual(block.validating_list[2].amount, 0.04)
        self.assertEqual(block.validating_list[1], the_transaction)

    def test_ProccesstheTransaction_account_list(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000),
            temp_path)
        SaveAccounts(
            Account("73cd109827c0de9fa211c0d062eab13584ea6bb8", 100000),
            temp_path)
        SaveAccounts(
            Account("08fe9bfc6521565c601a3785c5f5fb0a406279e6", 100000),
            temp_path)
        SaveAccounts(
            Account("6a4236cba1002b2919651677c7c520b67627aa2a", 100000),
            temp_path)
        SaveAccounts(
            Account("d10d419bae75549222c5ffead625a9e0246ad3e6", 100000),
            temp_path)

        account_list = GetAccounts(temp_path)

        custom_fee_address = "onurtheprofessional"

        result = ProccesstheTransaction(
            block,
            account_list,
            custom_TEMP_ACCOUNTS_PATH=temp_path,
            custom_fee_address=custom_fee_address,
            dont_clean=True,
        )
        account_list = GetAccounts(temp_path)
        account_list.execute(f"SELECT * FROM account_list")
        account_list = account_list.fetchall()
        self.assertEqual(len(account_list), 8)
        true_list = [
            the_transaction_4,
            the_transaction_5,
            the_transaction_2,
            the_transaction_3,
            the_transaction,
        ]
        self.assertEqual(block.validating_list[0], the_transaction_4)
        self.assertEqual(block.validating_list[1], the_transaction_5)
        self.assertEqual(block.validating_list[2], the_transaction_2)
        self.assertEqual(block.validating_list[3], the_transaction_3)
        self.assertEqual(block.validating_list[5].toUser,
                         "onurtheprofessional")
        self.assertEqual(block.validating_list[5].amount, 0.1)
        self.assertEqual(block.validating_list[4], the_transaction)
        self.assertEqual(account_list[0][2], 100000 - 5000 - 0.02)
        self.assertEqual(account_list[0][0],
                         "2ffd1f6bed8614f4cd01fc7159ac950604272773")
        self.assertEqual(account_list[0][1], 1)

        self.assertEqual(account_list[1][2], 94999.98)
        self.assertEqual(account_list[1][0],
                         "73cd109827c0de9fa211c0d062eab13584ea6bb8")
        self.assertEqual(account_list[1][1], 1)

        self.assertEqual(account_list[2][2], 94999.98)
        self.assertEqual(account_list[2][0],
                         "08fe9bfc6521565c601a3785c5f5fb0a406279e6")
        self.assertEqual(account_list[2][1], 1)

        self.assertEqual(account_list[3][2], 94999.98)
        self.assertEqual(account_list[3][0],
                         "6a4236cba1002b2919651677c7c520b67627aa2a")
        self.assertEqual(account_list[3][1], 1)

        self.assertEqual(account_list[4][2], 104999.98)
        self.assertEqual(account_list[4][0],
                         "d10d419bae75549222c5ffead625a9e0246ad3e6")
        self.assertEqual(account_list[4][1], 1)

        self.assertEqual(account_list[5][2], 15000)
        self.assertEqual(account_list[5][0], "onur")
        self.assertEqual(account_list[5][1], 0)

        self.assertEqual(account_list[6][2], 0.1)
        self.assertEqual(account_list[6][0], "onurtheprofessional")
        self.assertEqual(account_list[6][1], 0)

        self.assertEqual(account_list[7][2], 5000)
        self.assertEqual(account_list[7][0], "teaaast")
        self.assertEqual(account_list[7][1], 0)

    def test_ProccesstheTransaction_account_list_with_shares(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        block = Block(the_transaction.fromUser)
        block.sequence_number = 10
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

        temp_path = "db/test_ProccesstheTransaction_account_list_with_shares.db"

        SaveAccounts(
            Account("2ffd1f6bed8614f4cd01fc7159ac950604272773", 100000),
            temp_path)
        SaveAccounts(
            Account("73cd109827c0de9fa211c0d062eab13584ea6bb8", 100000),
            temp_path)
        SaveAccounts(
            Account("08fe9bfc6521565c601a3785c5f5fb0a406279e6", 100000),
            temp_path  # B
        )
        SaveAccounts(
            Account("6a4236cba1002b2919651677c7c520b67627aa2a", 100000),
            temp_path  # C
        )
        SaveAccounts(
            Account("d10d419bae75549222c5ffead625a9e0246ad3e6", 100000),
            temp_path)

        account_list = GetAccounts(temp_path)

        custom_shares = [["abc", 10, 10, 40], ["bca", 15, 10, 40]]
        custom_fee_address = "onuratakanulusoy"

        result = ProccesstheTransaction(
            block,
            account_list,
            custom_TEMP_ACCOUNTS_PATH=temp_path,
            custom_shares=custom_shares,
            custom_fee_address=custom_fee_address,
            dont_clean=True,
        )
        account_list = GetAccounts(temp_path)
        account_list.execute(f"SELECT * FROM account_list")
        account_list = account_list.fetchall()
        self.assertEqual(len(account_list), 10)
        true_list = [
            the_transaction_4,
            the_transaction_5,
            the_transaction_2,
            the_transaction_3,
            the_transaction,
        ]

        self.assertEqual(block.validating_list[0], the_transaction_4)
        self.assertEqual(block.validating_list[1], the_transaction_5)
        self.assertEqual(block.validating_list[2], the_transaction_2)
        self.assertEqual(block.validating_list[3], the_transaction_3)
        self.assertEqual(block.validating_list[5].toUser, "onuratakanulusoy")
        self.assertEqual(block.validating_list[5].amount, 0.1)
        self.assertEqual(block.validating_list[6].toUser, "abc")
        self.assertEqual(block.validating_list[6].amount, 10)
        self.assertEqual(block.validating_list[7].toUser, "bca")
        self.assertEqual(block.validating_list[7].amount, 15)
        self.assertEqual(block.validating_list[4], the_transaction)
        self.assertEqual(account_list[0][2], 100000 - 5000 - 0.02)
        self.assertEqual(account_list[0][0],
                         "2ffd1f6bed8614f4cd01fc7159ac950604272773")
        self.assertEqual(account_list[0][1], 1)

        self.assertEqual(account_list[1][2], 94999.98)
        self.assertEqual(account_list[1][0],
                         "73cd109827c0de9fa211c0d062eab13584ea6bb8")
        self.assertEqual(account_list[1][1], 1)

        self.assertEqual(account_list[2][2], 94999.98)
        self.assertEqual(account_list[2][0],
                         "08fe9bfc6521565c601a3785c5f5fb0a406279e6")  # B
        self.assertEqual(account_list[2][1], 1)

        self.assertEqual(account_list[3][2], 94999.98)
        self.assertEqual(account_list[3][0],
                         "6a4236cba1002b2919651677c7c520b67627aa2a")
        self.assertEqual(account_list[3][1], 1)

        self.assertEqual(account_list[4][2], 104999.98)
        self.assertEqual(account_list[4][0],
                         "d10d419bae75549222c5ffead625a9e0246ad3e6")
        self.assertEqual(account_list[4][1], 1)

        self.assertEqual(account_list[5][2], 10)
        self.assertEqual(account_list[5][0], "abc")
        self.assertEqual(account_list[5][1], 0)

        self.assertEqual(account_list[6][2], 15)
        self.assertEqual(account_list[6][0], "bca")
        self.assertEqual(account_list[6][1], 0)

        self.assertEqual(account_list[9][2], 5000)
        self.assertEqual(account_list[9][0], "teaaast")
        self.assertEqual(account_list[9][1], 0)

        self.assertEqual(account_list[8][2], 0.1)
        self.assertEqual(account_list[8][0], "onuratakanulusoy")
        self.assertEqual(account_list[8][1], 0)

        self.assertEqual(account_list[7][2], 15000)
        self.assertEqual(account_list[7][0], "onur")
        self.assertEqual(account_list[7][1], 0)

    def test_SavePending_GetPending_DeletePending(self):
        the_transaction_json = {
            "sequence_number": 1,
            "signature": "test_SavePending_GetPending",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
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

    def test_GetProof_no_transaction(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main_3/"
        custom_TEMP_ACCOUNTS_PATH = (
            "db/test_GetProof_no_transaction_TEMP_ACCOUNTS_PATH.json")
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_GetProof_no_transaction_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_GetProof_no_transaction_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_a = copy.copy(the_transaction)
        the_transaction_a.signature = "aa"
        block.validating_list = [the_transaction, the_transaction_a]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=
                               custom_TEMP_BLOCKSHASH_PART_PATH),
            GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash,
             hash_1]).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_1])

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

        the_transaction_2 = Transaction.load_json(the_transaction_json)
        the_transaction_2.signature = "a"

        result = GetProof(
            the_transaction_2.signature,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
        )

        self.assertIsNone(result)
        SaveMyTransaction(backup, clear=True)

    def test_GetProof_CheckProof(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_TEMP_BLOCKSHASH_PATH.json"
        custom_TEMP_BLOCKSHASH_PART_PATH = "db/test_finished_main_save_from_part_no_save_blockshash_TEMP_BLOCKSHASH_PART_PATH.json"

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_a = copy.copy(the_transaction)
        the_transaction_a.signature = "aa"
        block.validating_list = [the_transaction, the_transaction_a]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=
                               custom_TEMP_BLOCKSHASH_PART_PATH),
            GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash,
             hash_1]).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_1])

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

        result = GetProof(
            the_transaction.signature,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
        )

        self.assertIsNotNone(result)

        # Open result zip file
        zip_file = zipfile.ZipFile(result, "r")
        # Extract all files
        zip_file.extractall("db/test_proof_extracted/")
        # Close the zip file
        zip_file.close()

        list_of_files = []
        custom_BLOCKS_PATH_from_proof = None
        for file in os.listdir("db/test_proof_extracted/db/"):
            if os.path.isdir("db/test_proof_extracted/db/" + file):
                custom_BLOCKS_PATH_from_proof = (
                    "db/test_proof_extracted/db/" + file + "/")
                for file_2 in os.listdir("db/test_proof_extracted/db/" + file):
                    list_of_files.append(file_2)

        self.assertIn("0.block.json", list_of_files)
        self.assertIn("0.blockshashpart.json", list_of_files)
        self.assertIn("0.accounts.db", list_of_files)
        self.assertIn("0.blockshash.json", list_of_files)
        self.assertIn("1.blockshash_full.json", list_of_files)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH_from_proof,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH_from_proof +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(len(result_2[0].validating_list), 2)
        self.assertEqual(result_2[0].validating_list[0].dump_json(),
                         the_transaction.dump_json())
        self.assertEqual(result_2[0].validating_list[1].dump_json(),
                         the_transaction_a.dump_json())

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_2])
        self.assertEqual(hash_2, hash_1)
        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_2]).getRootHash()

        # Check the_hash_part is in the the_blockshash_part
        is_in = False
        for i in the_blockshash_part:
            if i == the_hash_part:
                is_in = True
        self.assertTrue(is_in)

        self.assertEqual(
            CheckProof(
                result,
                custom_TEMP_BLOCKSHASH_PART_PATH=
                custom_TEMP_BLOCKSHASH_PART_PATH,
            ),
            True,
        )

        SaveMyTransaction(backup, clear=True)

    def test_GetProof_CheckProof_false(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_GetProof_CheckProof_false_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_GetProof_CheckProof_false_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_a = copy.copy(the_transaction)
        the_transaction_a.signature = "aa"
        block.validating_list = [the_transaction, the_transaction_a]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=
                               custom_TEMP_BLOCKSHASH_PART_PATH),
            GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash,
             hash_1]).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_1])

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

        result = GetProof(
            the_transaction.signature,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
        )

        self.assertIsNotNone(result)

        # Open result zip file
        zip_file = zipfile.ZipFile(result, "r")
        # Extract all files
        zip_file.extractall("db/test_proof_extracted/")
        # Close the zip file
        zip_file.close()

        list_of_files = []
        custom_BLOCKS_PATH_from_proof = None
        for file in os.listdir("db/test_proof_extracted/db/"):
            if os.path.isdir("db/test_proof_extracted/db/" + file):
                custom_BLOCKS_PATH_from_proof = (
                    "db/test_proof_extracted/db/" + file + "/")
                for file_2 in os.listdir("db/test_proof_extracted/db/" + file):
                    list_of_files.append(file_2)

        self.assertIn("0.block.json", list_of_files)
        self.assertIn("0.blockshashpart.json", list_of_files)
        self.assertIn("0.accounts.db", list_of_files)
        self.assertIn("0.blockshash.json", list_of_files)
        self.assertIn("1.blockshash_full.json", list_of_files)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH_from_proof,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH_from_proof +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(len(result_2[0].validating_list), 2)
        self.assertEqual(result_2[0].validating_list[0].dump_json(),
                         the_transaction.dump_json())
        self.assertEqual(result_2[0].validating_list[1].dump_json(),
                         the_transaction_a.dump_json())

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_2])
        self.assertEqual(hash_2, hash_1)
        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_2]).getRootHash()

        # Check the_hash_part is in the the_blockshash_part
        is_in = False
        for i in the_blockshash_part:
            if i == the_hash_part:
                is_in = True
        self.assertTrue(is_in)

        false_part = custom_TEMP_BLOCKSHASH_PART_PATH.replace(
            "TEMP_BLOCKSHASH_PART_PATH", "TEMP_BLOCKSHASH_PART_PATH_2")
        SaveBlockshash_part(["abc", "abc"],
                            custom_TEMP_BLOCKSHASH_PART_PATH=false_part)

        self.assertEqual(
            CheckProof(
                result,
                custom_TEMP_BLOCKSHASH_PART_PATH=
                custom_TEMP_BLOCKSHASH_PART_PATH,
            ),
            True,
        )
        self.assertEqual(
            CheckProof(result, custom_TEMP_BLOCKSHASH_PART_PATH=false_part),
            False)

        SaveMyTransaction(backup, clear=True)

    def test_GetProof_CheckProof_none(self):
        backup_the_settings = the_settings()
        settings = copy.copy(backup_the_settings)
        settings["save_blockshash"] = True
        save_settings(settings)

        backup = GetMyTransaction()
        custom_TEMP_BLOCK_PATH = "db/test_finished_main.json"
        custom_BLOCKS_PATH = "db/test_finished_main/"
        custom_TEMP_ACCOUNTS_PATH = "db/test_finished_main_TEMP_ACCOUNTS_PATH.json"
        custom_TEMP_BLOCKSHASH_PATH = (
            "db/test_GetProof_CheckProof_none_TEMP_BLOCKSHASH_PATH.json")
        custom_TEMP_BLOCKSHASH_PART_PATH = (
            "db/test_GetProof_CheckProof_none_TEMP_BLOCKSHASH_PART_PATH.json")

        block = Block("Onurdsadsaas")
        block.hash = "new_hash"

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequence_number = 0
        block.empty_block_number = 0
        block.max_tx_number = 3
        block.part_amount = 2
        the_transaction_json = {
            "sequence_number": 1,
            "signature":
            "MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0.02,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        the_transaction.fromUser = wallet_import(-1, 0)
        the_transaction_a = copy.copy(the_transaction)
        the_transaction_a.signature = "aa"
        block.validating_list = [the_transaction, the_transaction_a]
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        hash_1 = CalculateHash(
            block,
            GetBlockshash_part(custom_TEMP_BLOCKSHASH_PART_PATH=
                               custom_TEMP_BLOCKSHASH_PART_PATH),
            GetBlockshash(
                custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH),
            GetAccounts(custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH),
        )
        block.hash = hash_1

        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )

        time.sleep(1)

        result = finished_main(
            block=block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            pass_sync=True,
            dont_clean=True,
        )
        self.assertTrue(result)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        the_blockshash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
        the_blockshash_part = GetBlockshash_part(
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
        expected_hash = MerkleTree(
            [Block("Onurdsadasdsaddsaas").previous_hash,
             hash_1]).getRootHash()
        self.assertEqual(the_blockshash, [])
        self.assertEqual(
            the_blockshash_part,
            [Block("Onurdsadasdsaddsaas").previous_hash, expected_hash],
        )

        settings = the_settings()
        self.assertEqual(settings["save_blockshash"], True)

        save_settings(backup_the_settings)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_1])

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(hash_2, hash_1)

        self.assertEqual(Saved_blocks_hash[1], hash_1)

        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_1]).getRootHash()
        self.assertEqual(the_blockshash_part[1], the_hash_part)

        result = GetProof(
            the_transaction.signature,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH,
        )

        self.assertIsNotNone(result)

        # Open result zip file
        zip_file = zipfile.ZipFile(result, "r")
        # Extract all files
        zip_file.extractall("db/test_proof_extracted/")
        # Close the zip file
        zip_file.close()

        list_of_files = []
        custom_BLOCKS_PATH_from_proof = None
        for file in os.listdir("db/test_proof_extracted/db/"):
            if os.path.isdir("db/test_proof_extracted/db/" + file):
                custom_BLOCKS_PATH_from_proof = (
                    "db/test_proof_extracted/db/" + file + "/")
                for file_2 in os.listdir("db/test_proof_extracted/db/" + file):
                    list_of_files.append(file_2)

        self.assertIn("0.block.json", list_of_files)
        self.assertIn("0.blockshashpart.json", list_of_files)
        self.assertIn("0.accounts.db", list_of_files)
        self.assertIn("0.blockshash.json", list_of_files)
        self.assertIn("1.blockshash_full.json", list_of_files)

        result_2 = GetBlockstoBlockchainDB(
            sequence_number=0,
            custom_BLOCKS_PATH=custom_BLOCKS_PATH_from_proof,
            dont_clean=True,
        )
        self.assertIsNot(result_2, False)

        Saved_blocks_hash = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=(custom_BLOCKS_PATH_from_proof +
                                         str(block.sequence_number) +
                                         ".blockshash_full.json"))

        hash_2 = CalculateHash(
            result_2[0],
            result_2[3],
            result_2[2],
            result_2[1],
        )

        self.assertEqual(len(result_2[0].validating_list), 2)
        self.assertEqual(result_2[0].validating_list[0].dump_json(),
                         the_transaction.dump_json())
        self.assertEqual(result_2[0].validating_list[1].dump_json(),
                         the_transaction_a.dump_json())

        self.assertEqual(Saved_blocks_hash,
                         [Block("Onurdsadasdsaddsaas").previous_hash, hash_2])
        self.assertEqual(hash_2, hash_1)
        the_hash_part = MerkleTree([Saved_blocks_hash[0],
                                    hash_2]).getRootHash()

        # Check the_hash_part is in the the_blockshash_part
        is_in = False
        for i in the_blockshash_part:
            if i == the_hash_part:
                is_in = True
        self.assertTrue(is_in)

        false_part = custom_TEMP_BLOCKSHASH_PART_PATH.replace(
            "TEMP_BLOCKSHASH_PART_PATH", "TEMP_BLOCKSHASH_PART_PATH_2")
        SaveBlockshash_part(["abc", "abc"],
                            custom_TEMP_BLOCKSHASH_PART_PATH=false_part)

        self.assertEqual(
            CheckProof(
                result + "onur",
                custom_TEMP_BLOCKSHASH_PART_PATH=
                custom_TEMP_BLOCKSHASH_PART_PATH,
            ),
            None,
        )
        self.assertEqual(
            CheckProof(result, custom_TEMP_BLOCKSHASH_PART_PATH=false_part),
            False)

        SaveMyTransaction(backup, clear=True)

    def test_cleaner_validating_list(self):
        block = Block("")
        block.max_tx_number = 2

        transaction_frem_a_0_j_3 = Transaction(0, "j", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)
        transaction_frem_a_0_a_4 = Transaction(0, "a", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 4)
        transaction_frem_a_1_q_3 = Transaction(1, "q", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)

        block.validating_list = [
            transaction_frem_a_0_j_3,
            transaction_frem_a_0_a_4,
            transaction_frem_a_1_q_3,
        ]
        pending_list_txs = GetPending()

        first_validating_list = copy.copy(block.validating_list)

        cleaned_lists = Cleaner(
            block=block,
            pending_list_txs=pending_list_txs,
            custom_balance=10000000000000,
            custom_sequence_number=-1,
        )
        block.validating_list = cleaned_lists[0]

        self.assertNotEqual(len(first_validating_list),
                            len(block.validating_list))

        find_difference = list(
            set(first_validating_list) - set(block.validating_list))
        find_difference_dict = [tx.__dict__ for tx in find_difference]
        print(find_difference_dict)
        self.assertTrue(
            transaction_frem_a_0_a_4.__dict__ in find_difference_dict)
        self.assertTrue(
            transaction_frem_a_1_q_3.__dict__ in find_difference_dict)
        self.assertEqual(len(find_difference_dict), 2)

        DeletePending(transaction_frem_a_0_j_3)
        DeletePending(transaction_frem_a_0_a_4)
        DeletePending(transaction_frem_a_1_q_3)

    def test_cleaner_validating_list_one(self):
        block = Block("")
        block.max_tx_number = 2

        transaction_frem_a_0_j_3 = Transaction(0, "j", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)
        transaction_frem_a_0_a_4 = Transaction(0, "a", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 4)
        transaction_frem_a_1_q_3 = Transaction(1, "q", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)

        block.validating_list = [
            transaction_frem_a_0_j_3,
        ]
        pending_list_txs = GetPending()

        first_validating_list = copy.copy(block.validating_list)

        cleaned_lists = Cleaner(
            block=block,
            pending_list_txs=pending_list_txs,
            custom_balance=10000000000000,
            custom_sequence_number=-1,
        )
        block.validating_list = cleaned_lists[0]

        self.assertEqual(len(first_validating_list),
                         len(block.validating_list))

        find_difference = list(
            set(first_validating_list) - set(block.validating_list))
        find_difference_dict = [tx.__dict__ for tx in find_difference]

        self.assertEqual(len(find_difference_dict), 0)

        DeletePending(transaction_frem_a_0_j_3)
        DeletePending(transaction_frem_a_0_a_4)
        DeletePending(transaction_frem_a_1_q_3)

    def test_cleaner_pending(self):
        block = Block("")
        block.max_tx_number = 2

        transaction_frem_a_0_j_3 = Transaction(0, "j", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)
        transaction_frem_a_0_a_4 = Transaction(0, "a", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 4)
        transaction_frem_a_1_q_3 = Transaction(1, "q", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)

        SavePending(transaction_frem_a_0_j_3)
        SavePending(transaction_frem_a_0_a_4)
        SavePending(transaction_frem_a_1_q_3)

        pending_list_txs = GetPending()

        first_pending_list_txs = copy.copy(pending_list_txs)

        cleaned_lists = Cleaner(
            block=block,
            pending_list_txs=pending_list_txs,
            custom_balance=10000000000000,
            custom_sequence_number=-1,
        )
        block.validating_list = cleaned_lists[0]
        pending_list_txs = cleaned_lists[1]
        self.assertNotEqual(len(first_pending_list_txs), len(pending_list_txs))
        first_pending_list_txs = [tx.__dict__ for tx in first_pending_list_txs]
        pending_list_txs = [tx.__dict__ for tx in pending_list_txs]
        # Get the difference of two dict lists
        # TypeError: unhashable type: 'dict'

        find_difference_dict = [
            x for x in first_pending_list_txs if x not in pending_list_txs
        ]

        self.assertTrue(
            transaction_frem_a_0_a_4.__dict__ in find_difference_dict)
        self.assertTrue(
            transaction_frem_a_1_q_3.__dict__ in find_difference_dict)
        self.assertEqual(len(find_difference_dict), 2)

        self.assertEqual([tx for tx in pending_list_txs],
                         [tx.__dict__ for tx in GetPending()])

        DeletePending(transaction_frem_a_0_j_3)
        DeletePending(transaction_frem_a_0_a_4)
        DeletePending(transaction_frem_a_1_q_3)

    def test_cleaner_pending_one(self):
        block = Block("")
        block.max_tx_number = 2

        transaction_frem_a_0_j_3 = Transaction(0, "j", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)
        transaction_frem_a_0_a_4 = Transaction(0, "a", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 4)
        transaction_frem_a_1_q_3 = Transaction(1, "q", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)

        SavePending(transaction_frem_a_0_j_3)

        pending_list_txs = GetPending()

        first_pending_list_txs = copy.copy(pending_list_txs)

        cleaned_lists = Cleaner(
            block=block,
            pending_list_txs=pending_list_txs,
            custom_balance=10000000000000,
            custom_sequence_number=-1,
        )
        block.validating_list = cleaned_lists[0]
        pending_list_txs = cleaned_lists[1]
        self.assertEqual(len(first_pending_list_txs), len(pending_list_txs))
        first_pending_list_txs = [tx.__dict__ for tx in first_pending_list_txs]
        pending_list_txs = [tx.__dict__ for tx in pending_list_txs]

        find_difference_dict = [
            x for x in first_pending_list_txs if x not in pending_list_txs
        ]

        self.assertEqual([tx for tx in pending_list_txs],
                         [tx.__dict__ for tx in GetPending()])

        DeletePending(transaction_frem_a_0_j_3)
        DeletePending(transaction_frem_a_0_a_4)
        DeletePending(transaction_frem_a_1_q_3)

    def test_cleaner_pending_one_delete(self):
        block = Block("")
        block.max_tx_number = 2

        transaction_frem_a_0_j_3 = Transaction(0, "j", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)
        transaction_frem_a_0_a_4 = Transaction(0, "a", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 4)
        transaction_frem_a_1_q_3 = Transaction(1, "q", "a", "", "", 100000,
                                               150,
                                               int(time.time()) + 3)

        SavePending(transaction_frem_a_0_j_3)
        SavePending(transaction_frem_a_0_a_4)
        SavePending(transaction_frem_a_1_q_3)

        pending_list_txs = GetPending()

        first_pending_list_txs = copy.copy(pending_list_txs)

        cleaned_lists = Cleaner(block=block, pending_list_txs=pending_list_txs)
        block.validating_list = cleaned_lists[0]
        pending_list_txs = cleaned_lists[1]
        self.assertNotEqual(len(first_pending_list_txs), len(pending_list_txs))
        first_pending_list_txs = [tx.__dict__ for tx in first_pending_list_txs]
        pending_list_txs = [tx.__dict__ for tx in pending_list_txs]

        find_difference_dict = [
            x for x in first_pending_list_txs if x not in pending_list_txs
        ]

        self.assertEqual([tx for tx in pending_list_txs],
                         [tx.__dict__ for tx in GetPending()])

        DeletePending(transaction_frem_a_0_j_3)
        DeletePending(transaction_frem_a_0_a_4)
        DeletePending(transaction_frem_a_1_q_3)


backup = sys.argv
sys.argv = [sys.argv[0]]
unittest.main(exit=False)
sys.argv = backup
