#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from decentra_network.lib.config_system import get_config
from decentra_network.transactions.transaction import Transaction
from decentra_network.transactions.pending.delete_pending import DeletePending
from decentra_network.blockchain.block.block_main import Block
from decentra_network.transactions.send import send


def CleanUp_tests():
    os.chdir(get_config()["main_folder"])
    for the_file in os.listdir("db/"):
        if the_file.startswith("test_"):
            if os.path.isfile(f"db/{the_file}"):
                os.remove(f"db/{the_file}")
    for the_file in os.listdir(
            "db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB/"):
        if the_file.endswith(".json"):
            os.remove(
                f"db/test_SaveBlockstoBlockchainDB_GetBlockstoBlockchainDB/{the_file}"
            )

    for the_file in os.listdir("db/connected_nodes_test_0/"):
        if the_file.endswith(".json"):
            os.remove(f"db/connected_nodes_test_0/{the_file}")
    for the_file in os.listdir("db/connected_nodes_test_1/"):
        if the_file.endswith(".json"):
            os.remove(f"db/connected_nodes_test_1/{the_file}")
    for the_file in os.listdir("db/connected_nodes_test_2/"):
        if the_file.endswith(".json"):
            os.remove(f"db/connected_nodes_test_2/{the_file}")

    for the_file in os.listdir("db/pending_transactions_test_0/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_0/{the_file}")
    for the_file in os.listdir("db/pending_transactions_test_1/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_1/{the_file}")
    for the_file in os.listdir("db/pending_transactions_test_2/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_2/{the_file}")

    for the_file in os.listdir("db/pending_transactions_test_3/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_3/{the_file}")
    for the_file in os.listdir("db/pending_transactions_test_4/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_4/{the_file}")
    for the_file in os.listdir("db/pending_transactions_test_5/"):
        if the_file.endswith(".json"):
            os.remove(f"db/pending_transactions_test_5/{the_file}")

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
        DeletePending(the_transaction)

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
        the_transaction1 = Transaction.load_json(the_transaction_json)
        the_transaction1.signature = "11"
        DeletePending(the_transaction1)

        block = Block("onur")
        result = send(
            block,
            "123",
            "onur",
            5000,
            "77ulusoy",
            custom_current_time=(int(time.time()) + 5),
            custom_sequence_number=0,
            custom_balance=100000,
        )

        DeletePending(result)

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
        DeletePending(the_transaction)

        the_transaction_json = {
            "sequance_number": 1,
            "signature":
            "test_SavePending_GetPending",
            "fromUser":
            "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE0AYA7B+neqfUA17wKh3OxC67K8UlIskMm9T2qAR+pl+kKX1SleqqvLPM5bGykZ8tqq4RGtAcGtrtvEBrB9DTPg==",
            "toUser": "onur",
            "data": "blockchain-lab",
            "amount": 5000.0,
            "transaction_fee": 0,
            "transaction_time": 1656764224,
        }
        the_transaction = Transaction.load_json(the_transaction_json)
        DeletePending(the_transaction)
