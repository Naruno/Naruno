#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def TxAlreadyGot(block, fromUser, sequance_number, temp_signature):
    """
    Checks if the transaction is already got.
    """

    for already_tx in (block.pendingTransaction + block.validating_list):
        if already_tx.signature == temp_signature:
            return True
        if already_tx.fromUser == fromUser:
            for already_tx_parent in (block.pendingTransaction + block.validating_list):
                if not already_tx.signature == already_tx_parent.signature:
                    if already_tx.sequance_number == already_tx_parent.sequance_number:
                        return True

    return False
