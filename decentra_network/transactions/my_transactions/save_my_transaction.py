#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction


def SaveMyTransaction(transaction_list):
    """
    Saves the transaction_list to the transaction db.
    """

    if type(transaction_list) is list:
        new_dict = {
            tx[0].signature: {
                "tx": tx[0].dump_json(),
                "validated": tx[1],
                "sended": tx[2],
            }
            for tx in transaction_list
        }

        transaction_list = new_dict

    os.chdir(get_config()["main_folder"])
    with open(MY_TRANSACTION_PATH, "w") as my_transaction_file:
        json.dump(transaction_list, my_transaction_file)
