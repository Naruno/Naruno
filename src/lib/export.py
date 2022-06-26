#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import csv
import os

from config import MY_TRANSACTION_EXPORT_PATH
from lib.config_system import get_config
from transactions.get_my_transaction import GetMyTransaction


def export_the_transactions():
    """
    Export the transactions to a CSV file.
    """
    obj = GetMyTransaction()
    filename = MY_TRANSACTION_EXPORT_PATH
    if not len(obj) == 0:
        os.chdir(get_config()["main_folder"])
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [i for i in obj[0][0].__dict__.keys()] + ["is_valid"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for obj in obj:
                trans = obj[0].__dict__
                trans["is_valid"] = obj[1]
                writer.writerow(trans)
        return True
    else:
        return False
