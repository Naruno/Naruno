#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from transactions.tx_already_got import TxAlreadyGot


def SameTransactionGuard(block):
    """
    This function is used to check and delete same transaction.
    Inputs:
        * block: The block (class)
    """

    for tx in (block.validating_list + block.pendingTransaction):
        if TxAlreadyGot(block, tx.fromUser, tx.sequance_number, tx.temp_signature):
            try:
                block.validating_list.remove(tx)
            except:
                block.pendingTransaction.remove(tx)