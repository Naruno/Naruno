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

from transactions.get_my_transaction import GetMyTransaction


def SavetoMyTransaction(tx):
    """
    Saves the transaction to the transaction db.
    """

    currently_list = GetMyTransaction()
    currently_list.append(tx)

    os.chdir(get_config()["main_folder"])
    with open(MY_TRANSACTION_PATH, "wb") as my_transaction_file:
        pickle.dump(currently_list, my_transaction_file, protocol=2)
