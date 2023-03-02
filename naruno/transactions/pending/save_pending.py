#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from hashlib import sha256

from decentra_network.config import PENDING_TRANSACTIONS_PATH
from decentra_network.lib.config_system import get_config


def SavePending(tx, custom_PENDING_TRANSACTIONS_PATH=None):
    the_PENDING_TRANSACTIONS_PATH = (PENDING_TRANSACTIONS_PATH if
                                     custom_PENDING_TRANSACTIONS_PATH is None
                                     else custom_PENDING_TRANSACTIONS_PATH)
    file_name = sha256((tx.signature).encode("utf-8")).hexdigest()
    the_path = the_PENDING_TRANSACTIONS_PATH + f"{file_name}.json"
    os.chdir(get_config()["main_folder"])
    with open(the_path, "w") as my_transaction_file:
        json.dump(tx.dump_json(), my_transaction_file)
