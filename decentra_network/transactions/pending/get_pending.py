#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import PENDING_TRANSACTIONS_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.transaction import Transaction


def GetPending():
    the_pending_list = []
    os.chdir(get_config()["main_folder"])
    for entry in os.scandir(PENDING_TRANSACTIONS_PATH):
        if entry.name != "README.md":
            with open(entry.path, "r") as my_transaction_file:
                the_pending_list.append(
                    Transaction.load_json(json.load(my_transaction_file)))
    return sorted(the_pending_list, key=lambda x: x.signature)
