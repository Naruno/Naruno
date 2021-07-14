#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pickle
import os

from lib.config_system import get_config
from config import MY_TRANSACTION_PATH

from transactions.transaction import Transaction


def SavetoMyTransaction(tx):
    """
    Saves the transaction to the transaction db.
    """
    currently_list = GetMyTransaction()

    for i in currently_list:
        if i.sequance_number == None:
            currently_list.remove(i)

    currently_list.append(tx)

    os.chdir(get_config()["main_folder"])
    with open(MY_TRANSACTION_PATH, "wb") as my_transaction_file:
        pickle.dump(currently_list, my_transaction_file, protocol=2)


def GetMyTransaction():
    """
    Returns the transaction db.
    """

    os.chdir(get_config()["main_folder"])

    if not os.path.exists(MY_TRANSACTION_PATH):
        return [Transaction(None, None, None, None, None, None, None, None)]

    with open(MY_TRANSACTION_PATH, "rb") as my_transaction_file:
        return pickle.load(my_transaction_file)
