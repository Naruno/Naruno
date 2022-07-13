#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
import sys

from decentra_network.lib.config_system import get_config


def testing_app_main_tx(tx):
    os.chdir(get_config()["main_folder"])
    with open(f"apps/testing_app/{tx.transaction_time}.tx", "w") as my_transaction_file:
        json.dump(tx.transaction_time, my_transaction_file)
    sys.exit()
