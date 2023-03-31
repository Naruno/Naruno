#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from typing import List

from naruno.config import MY_TRANSACTION_PATH
from naruno.lib.config_system import get_config
from naruno.lib.notification import notification
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_my_transaction import \
    SaveMyTransaction
from naruno.transactions.transaction import Transaction
from naruno.wallet.wallet_import import Address


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
    if not tx.signature == "NARUNO":
        new = True

        for tx_list in currently_list:
            if tx_list[0].signature == tx.signature:
                new = False

        if new:
            if not sended and validated:
                notification(
                    "Incoming TX",
                    f"{tx.data}:{tx.amount} from {Address(tx.fromUser)}")
            elif sended and not validated:
                notification("Sended TX",
                             f"{tx.data}:{tx.amount} to {tx.toUser}")
            elif sended and validated:
                notification("Validated TX",
                             f"{tx.data}:{tx.amount} to {tx.toUser}")

            tx_list = [tx, validated, sended]
            currently_list.append(tx_list)

        else:
            for tx_list in currently_list:
                if tx_list[0].signature == tx.signature:
                    tx_list[1] = validated
                    tx_list[2] = sended

    SaveMyTransaction(currently_list)

    return currently_list
