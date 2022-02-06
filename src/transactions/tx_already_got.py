#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def TXAlreadyGot(block, transaction):
    """
    Checks if the transaction is already in the block.
    """

    for already_tx in block.pendingTransaction + block.validating_list:
        if already_tx.signature == transaction.signature:
            return True

    return False
