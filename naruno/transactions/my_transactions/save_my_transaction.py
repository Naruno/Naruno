#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import json
import os
import time
from hashlib import sha256

from naruno.config import MY_TRANSACTION_PATH
from naruno.lib.config_system import get_config
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction


def SaveMyTransaction(transaction_list, clear=False):
    """
    Saves the transaction_list to the transaction db.
    """

    os.chdir(get_config()["main_folder"])

    if type(transaction_list) is list:
        entry_name_list = []
        for tx in transaction_list:
            name = copy.copy(tx[0].signature.encode("utf-8"))
            if tx[0].signature == b"":
                name = "empty".encode("utf-8")

            entry_name_list.append(
                os.path.join(MY_TRANSACTION_PATH,
                             sha256(name).hexdigest()))

        new_dict = {
            tx[0].signature: {
                "tx": tx[0].dump_json(),
                "validated": tx[1],
                "sended": tx[2],
            }
            for tx in transaction_list
        }

        if clear:
            for entry in os.scandir(MY_TRANSACTION_PATH):
                if (entry.name != "README.md"
                        and not entry.name.startswith("validated")
                        and not entry.name.startswith("sended")):
                    if entry.name not in str(entry_name_list):
                        os.remove(entry.path)
                        if os.path.exists(
                                os.path.join(MY_TRANSACTION_PATH,
                                             "validated" + entry.name)):
                            os.remove(
                                os.path.join(MY_TRANSACTION_PATH,
                                             "validated" + entry.name))
                        if os.path.exists(
                                os.path.join(MY_TRANSACTION_PATH,
                                             "sended" + entry.name)):
                            os.remove(
                                os.path.join(MY_TRANSACTION_PATH,
                                             "sended" + entry.name))

        transaction_list = new_dict

        for tx in transaction_list:
            name = copy.copy(tx.encode("utf-8"))
            if tx == b"":
                name = "empty".encode("utf-8")

            with open(
                    os.path.join(MY_TRANSACTION_PATH,
                                 sha256(name).hexdigest()),
                    "w") as my_transaction_file:
                json.dump(transaction_list[tx]["tx"], my_transaction_file)
            if transaction_list[tx]["validated"]:
                with open(
                        os.path.join(MY_TRANSACTION_PATH,
                                     "validated" + sha256(name).hexdigest()),
                        "w",
                ) as my_transaction_file:
                    my_transaction_file.write("1")

            if transaction_list[tx]["sended"]:
                with open(
                        os.path.join(MY_TRANSACTION_PATH,
                                     "sended" + sha256(name).hexdigest()),
                        "w",
                ) as my_transaction_file:
                    my_transaction_file.write("1")
    elif type(transaction_list) is dict and transaction_list != {}:
        with open(
                os.path.join(MY_TRANSACTION_PATH,
                             sha256(
                                 transaction_list[0].signature).hexdigest()),
                "w",
        ) as my_transaction_file:
            json.dump(transaction_list[0].dump_json(), my_transaction_file)

        if transaction_list[1]:
            with open(
                    os.path.join(
                        MY_TRANSACTION_PATH,
                        "validated" +
                        sha256(transaction_list[0].signature).hexdigest(),
                    ),
                    "w",
            ) as my_transaction_file:
                my_transaction_file.write("1")
        if transaction_list[2]:
            with open(
                    os.path.join(
                        MY_TRANSACTION_PATH,
                        "sended" +
                        sha256(transaction_list[0].signature).hexdigest(),
                    ),
                    "w",
            ) as my_transaction_file:
                my_transaction_file.write("1")
