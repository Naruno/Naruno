#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from hashlib import sha256

from naruno.config import PENDING_TRANSACTIONS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.kot import KOT

pendingtransactions_db = KOT(
    "pendingtransactions", folder=get_config()["main_folder"] + "/db"
)


def DeletePending(tx, custom_PENDING_TRANSACTIONS_PATH=None):
    the_PENDING_TRANSACTIONS_PATH = (
        PENDING_TRANSACTIONS_PATH
        if custom_PENDING_TRANSACTIONS_PATH is None
        else custom_PENDING_TRANSACTIONS_PATH
    )

    file_name = sha256((tx.signature).encode("utf-8")).hexdigest()
    pendingtransactions_db.delete(file_name)
