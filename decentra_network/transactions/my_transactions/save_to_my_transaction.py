#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from typing import List

from decentra_network.config import MY_TRANSACTION_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from decentra_network.transactions.transaction import Transaction


def SavetoMyTransaction(
    tx: Transaction,
    validated: bool = False,
    sended: bool = False,
    custom_currently_list: list = None,
) -> list:
    """
    Saves the transaction to the transaction db.
    Parameters:
        tx: The transaction that is going to be saved.
        validated: The boolean that sets if the transaction is validated or not.
        custom_currently_list: The list for custom situations.
    Returns:
        The list of the my transactions.
    """

    currently_list = (GetMyTransaction() if custom_currently_list is None else
                      custom_currently_list)
    tx_list = [tx, validated, sended]
    currently_list.append(tx_list)

    SaveMyTransaction(currently_list)

    return currently_list
