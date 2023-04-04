#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import COMMANDERS_PATH
from naruno.lib.config_system import get_config
from naruno.transactions.transaction import Transaction


def GetCommander():
    the_pending_list = []
    os.chdir(get_config()["main_folder"])
    for entry in os.scandir(COMMANDERS_PATH):
        if entry.name != "README.md":
            with open(entry.path, "r") as my_transaction_file:
                the_pending_list.append(entry.name)

    # order the list by alphabetical order
    the_pending_list.sort()
    return the_pending_list
