#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from hashlib import sha256

from decentra_network.config import PENDING_TRANSACTIONS_PATH
from decentra_network.transactions.pending.delete_pending import DeletePending


def RemoveSamePending(transactions: list, custom_PENDING_TRANSACTIONS_PATH=None) -> list:
    the_PENDING_TRANSACTIONS_PATH = (PENDING_TRANSACTIONS_PATH if
                                     custom_PENDING_TRANSACTIONS_PATH is None
                                     else custom_PENDING_TRANSACTIONS_PATH)
    for tx in transactions:
        same = False
        for tx2 in transactions:
            if tx != tx2:
                if tx.signature == tx2.signature:
                    same = True
                    break
        if same:
            DeletePending(
                tx, custom_PENDING_TRANSACTIONS_PATH=the_PENDING_TRANSACTIONS_PATH)
            transactions.remove(tx)
    return transactions
