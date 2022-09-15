#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.transaction import Transaction


def GetMyTransaction(sended=None, validated=None, turn_json=False) -> list:
    """
    Returns the transaction db.
    """

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(MY_TRANSACTION_PATH):
        return []

    the_transactions = []

    with open(MY_TRANSACTION_PATH, "r") as my_transaction_file:
        the_transactions_json = json.load(my_transaction_file)
        for transaction in list(the_transactions_json.values()):
            the_transactions.append([
                Transaction.load_json(transaction["tx"]),
                transaction["validated"],
                transaction["sended"],
            ])

    if sended is not None:
        the_transactions = [tx for tx in the_transactions if tx[2] == sended]

    if validated is not None:
        the_transactions = [
            tx for tx in the_transactions if tx[1] == validated
        ]

    if turn_json:
        the_transactions = {
            the_transactions.index(tx): {
                "transaction": tx[0].dump_json(),
                "validated": tx[1],
                "sended": tx[2],
            }
            for tx in the_transactions
        }

    return the_transactions
