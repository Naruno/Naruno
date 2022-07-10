#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os

from config import VALIDATING_TRANSACTIONS_PATH
from lib.config_system import get_config

def SaveValidating(tx):
    the_path = VALIDATING_TRANSACTIONS_PATH + f"{tx.signature}.json"
    os.chdir(get_config()["main_folder"])
    with open(the_path, "w") as my_transaction_file:
        json.dump(tx.dump_json(), my_transaction_file)
