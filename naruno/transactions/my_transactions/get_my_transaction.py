#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os

from naruno.config import MY_TRANSACTION_PATH
from naruno.lib.config_system import get_config
from naruno.transactions.transaction import Transaction
from naruno.lib.kot import KOT

mytransactions_db = KOT("mytransactions", folder=get_config()[
                        "main_folder"] + "/db")


def GetMyTransaction(sended=None, validated=None, turn_json=False) -> list:
    """
    Returns the transaction db.
    """

    the_transactions = []

    all_records = mytransactions_db.get_all()
    for entry in all_records:
        if (not entry.endswith("validated") and not entry.endswith("sended")):
            try:
                the_transactions_json = all_records[entry]
                each_validated = False if mytransactions_db.get(
                    entry + "validated") == None else True
                each_sended = False if mytransactions_db.get(
                    entry + "sended") == None else True
                the_transactions.append([
                    Transaction.load_json(the_transactions_json),
                    each_validated,
                    each_sended,
                ])
            except json.decoder.JSONDecodeError:
                with contextlib.suppress(Exception):
                    os.remove(entry.path)

    if sended is not None:
        the_transactions = [tx for tx in the_transactions if tx[2] == sended]

    if validated is not None:
        the_transactions = [
            tx for tx in the_transactions if tx[1] == validated
        ]

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
