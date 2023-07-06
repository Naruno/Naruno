#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os
import traceback
from urllib.request import urlopen

from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT
from naruno.lib.settings_system import the_settings
from naruno.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from naruno.transactions.transaction import Transaction

mytransactions_db = KOT("mytransactions", folder=get_config()["main_folder"] + "/db")


def check_from_network():
    """
    Checks if the transaction is in the network.
    """
    validated_transactions = []
    if the_settings()["baklava"]:
        try:
            # export validated transactions
            response = (
                urlopen("http://test_net.1.naruno.org:8000/transactions/received")
                .read()
                .decode("utf-8")
            )
            response = json.loads(response)
            for transaction in response:
                if response[transaction]["validated"]:
                    validated_transactions.append(transaction)
        except:
            traceback.print_exc()

    return validated_transactions


def GetMyTransaction(sended=None, validated=None, turn_json=False) -> list:
    """
    Returns the transaction db.
    """
    network_validated = check_from_network()

    the_transactions = []

    all_records = mytransactions_db.get_all()
    for entry in all_records:
        if not entry.endswith("validated") and not entry.endswith("sended"):
            try:
                the_transactions_json = all_records[entry]
                the_tx = Transaction.load_json(the_transactions_json)
                each_validated = (
                    False
                    if mytransactions_db.get(entry + "validated") == None
                    else True
                )
                if (
                    the_transactions_json["signature"] in network_validated
                    and not each_validated
                ):
                    each_validated = True
                    ValidateTransaction(the_tx)
                each_sended = (
                    False if mytransactions_db.get(entry + "sended") == None else True
                )
                the_transactions.append(
                    [
                        the_tx,
                        each_validated,
                        each_sended,
                    ]
                )
            except json.decoder.JSONDecodeError:
                mytransactions_db.delete(entry)
                mytransactions_db.delete(entry + "validated")
                mytransactions_db.delete(entry + "sended")

    if sended is not None:
        the_transactions = [tx for tx in the_transactions if tx[2] == sended]

    if validated is not None:
        the_transactions = [tx for tx in the_transactions if tx[1] == validated]

    # sort
    the_transactions.sort(key=lambda x: x[0].signature)

    if turn_json:
        the_transactions = {
            tx[0].signature: {
                "transaction": tx[0].dump_json(),
                "validated": tx[1],
                "sended": tx[2],
            }
            for tx in the_transactions
        }

    return the_transactions
