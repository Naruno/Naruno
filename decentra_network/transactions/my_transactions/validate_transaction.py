#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.config import MY_TRANSACTION_PATH
from distutils.log import info
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.my_transactions.get_my_transaction import (
    GetMyTransaction,
)
from decentra_network.transactions.my_transactions.save_my_transaction import (
    SaveMyTransaction,
)


def ValidateTransaction(tx):
    """
    Validates the transaction.
    """

    tx_list = GetMyTransaction()
    for i in tx_list:
        if i[0].signature == tx.signature:
            i[1] = True
    SaveMyTransaction(tx_list)
