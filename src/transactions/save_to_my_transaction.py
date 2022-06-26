#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import pickle

from config import MY_TRANSACTION_PATH
from lib.config_system import get_config
from transactions.get_my_transaction import GetMyTransaction
from transactions.save_my_transaction import SaveMyTransaction


def SavetoMyTransaction(tx, validated=False):
    """
    Saves the transaction to the transaction db.
    """

    currently_list = GetMyTransaction()
    tx_list = [tx, validated]
    currently_list.append(tx_list)

    SaveMyTransaction(currently_list)
