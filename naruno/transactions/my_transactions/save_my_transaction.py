#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import json
import os
from hashlib import sha256

from naruno.config import MY_TRANSACTION_PATH
from naruno.lib.config_system import get_config

from naruno.lib.kot import KOT

mytransactions_db = KOT("mytransactions", folder=get_config()["main_folder"] + "/db")


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
            for entry in mytransactions_db.get_all():
                if (not entry.endswith("validated") and not entry.endswith("sended")):
                    if entry not in str(entry_name_list):
                        mytransactions_db.delete(entry)
                        mytransactions_db.delete(entry+"validated")
                        mytransactions_db.delete(entry+"sended")

        transaction_list = new_dict

        for tx in transaction_list:
            name = copy.copy(tx.encode("utf-8"))
            if tx == b"":
                name = "empty".encode("utf-8")
            mytransactions_db.set(sha256(name).hexdigest(), transaction_list[tx]["tx"])

            if transaction_list[tx]["validated"]:
                mytransactions_db.set(sha256(name).hexdigest()+"validated", True)
            if transaction_list[tx]["sended"]:
                mytransactions_db.set(sha256(name).hexdigest()+"sended", True)

    elif type(transaction_list) is dict and transaction_list != {}:
        mytransactions_db.set(sha256(transaction_list[0].signature).hexdigest(), transaction_list[0].dump_json())

        if transaction_list[1]:
            mytransactions_db.set(sha256(transaction_list[0].signature+"validated").hexdigest(), True)
        if transaction_list[2]:
            mytransactions_db.set(sha256(transaction_list[0].signature+"sended").hexdigest(), True)
