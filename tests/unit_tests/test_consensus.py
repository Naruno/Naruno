#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import time
import unittest
import copy

from decentra_network.blockchain.block.block_main import Block
from decentra_network.consensus.time.true_time.true_time_main import true_time
from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction

from decentra_network.consensus.finished.transactions.transactions_main import \
    transactions_main
from decentra_network.transactions.transaction import Transaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


class Test_Consensus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    @classmethod
    def tearDownClass(cls):
        CleanUp_tests()

    def test_true_time_false(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 100
        self.assertFalse(true_time(block=block))

    def test_true_time(self):
        block = Block("Onur")

        block.genesis_time = int(time.time())
        block.block_time = 1
        block.sequance_number = 0
        block.empty_block_number = 0
        time.sleep(1)
        self.assertTrue(true_time(block=block))

    def test_transactions_main(self):
        backup = GetMyTransaction()
        block = Block("Onur")
        the_transaction_json = {
            "sequance_number": 1,
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
        block.validating_list.append(the_transaction)

        the_transaction_2 = copy.copy(the_transaction)
        the_transaction_2.signature = "ulusoy"
        the_transaction_2.fromUser = "onuratakan"
        the_transaction_2.toUser = wallet_import(-1, 3)

        block.validating_list.append(the_transaction_2)

        SavetoMyTransaction(the_transaction)

        transactions_main(block=block)

        result = GetMyTransaction()

        for each_result in result:
            result[result.index(each_result)][0] = result[result.index(
                each_result)][0].dump_json()
        SaveMyTransaction(backup)
        self.assertEqual(result, [[{'sequance_number': 1, 'signature': 'MEUCIHABt7ypkpvFlpqL4SuogwVuzMu2gGynVkrSw6ohZ/GyAiEAg2O3iOei1Ft/vQRpboX7Sm1OOey8a3a67wPJaH/FmVE=', 'fromUser': 'MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBiwdGJ8HYs6GzhdtI+LyPOQ1mOQSSTx7ZPOzEIPqz4DsngIwzE2K7Zslxo9AzqFnBZSM9/n5a9XTlCzD29/qwQ==', 'toUser': 'onur', 'data': 'blockchain-lab',
                         'amount': 5000.0, 'transaction_fee': 0.02, 'transaction_time': 1656764224}, True], [{'sequance_number': 1, 'signature': 'ulusoy', 'fromUser': 'onuratakan', 'toUser': '640c45eba93f854ad9c4447a4af2a0b24487d680', 'data': 'blockchain-lab', 'amount': 5000.0, 'transaction_fee': 0.02, 'transaction_time': 1656764224}, True]])


unittest.main(exit=False)
