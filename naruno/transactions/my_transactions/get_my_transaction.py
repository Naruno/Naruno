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


def GetMyTransaction(sended=None, validated=None, turn_json=False) -> list:
    """
    Returns the transaction db.
    """

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(MY_TRANSACTION_PATH):
        return []

    the_transactions = []

    # find the my transaction folder with os scandir
    for entry in os.scandir(MY_TRANSACTION_PATH):
        if (entry.name != "README.md"
                and not entry.name.startswith("validated")
                and not entry.name.startswith("sended")):
            try:
                the_transactions_json = json.load(open(entry.path, "r"))
                # Find "validatedentry.name" and "sendedentry.name" files
                each_validated = False
                each_sended = False
                if os.path.exists(
                        os.path.join(MY_TRANSACTION_PATH,
                                    "validated" + entry.name)):
                    each_validated = True
                if os.path.exists(
                        os.path.join(MY_TRANSACTION_PATH, "sended" + entry.name)):
                    each_sended = True
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

    #sort
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
