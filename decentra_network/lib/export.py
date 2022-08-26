#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import csv
import os

from decentra_network.config import MY_TRANSACTION_EXPORT_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction


def export_the_transactions(
        custom_transactions: list = None,
        custom_MY_TRANSACTION_EXPORT_PATH: str = None) -> bool:
    """
    Export the transactions to a CSV file.
    """
    obj = GetMyTransaction(
    ) if custom_transactions is None else custom_transactions
    filename = (MY_TRANSACTION_EXPORT_PATH
                if custom_MY_TRANSACTION_EXPORT_PATH is None else
                custom_MY_TRANSACTION_EXPORT_PATH)
    if len(obj) == 0:
        return False
    os.chdir(get_config()["main_folder"])
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = list(obj[0][0].__dict__.keys()) + ["is_valid"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for obj in obj:
            trans = obj[0].__dict__
            trans["is_valid"] = obj[1]
            writer.writerow(trans)
    return True
