#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import PENDING_TRANSACTIONS_PATH
from naruno.lib.config_system import get_config

from naruno.transactions.transaction import Transaction

from naruno.transactions.pending.save_pending import pendingtransactions_db
from naruno.lib.kot import KOT

def GetPending(custom_PENDING_TRANSACTIONS_PATH=None):
    if custom_PENDING_TRANSACTIONS_PATH == PENDING_TRANSACTIONS_PATH:
        custom_PENDING_TRANSACTIONS_PATH = None
    the_pending_list = []
    all_records = pendingtransactions_db.get_all() if custom_PENDING_TRANSACTIONS_PATH is None else KOT("pendingtransactions"+custom_PENDING_TRANSACTIONS_PATH, folder=get_config()["main_folder"] + "/db").get_all()
    for entry in all_records:
        the_pending_list.append(Transaction.load_json(all_records[entry]))
    return sorted(the_pending_list, key=lambda x: x.signature)


def GetPendingLen(custom_PENDING_TRANSACTIONS_PATH=None):


    return pendingtransactions_db.get_count() if custom_PENDING_TRANSACTIONS_PATH is None else KOT("pendingtransactions"+custom_PENDING_TRANSACTIONS_PATH, folder=get_config()["main_folder"] + "/db").get_count()
