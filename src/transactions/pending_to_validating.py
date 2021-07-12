#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from lib.mixlib import dprint


def PendinttoValidating(block):
    """
    Adds transactions to the verification list
    if there are suitable conditions.
    """

    dprint("Pending transactions number: " + str(len(block.pendingTransaction)))
    dprint("Validating transactions number: " + str(len(block.validating_list)))

    if (
        len(block.validating_list) < block.max_tx_number
        and block.raund_1_starting_time is None
    ):
        for tx in block.pendingTransaction[:]:
            if len(block.validating_list) < block.max_tx_number:
                block.validating_list.append(tx)
                block.pendingTransaction.remove(tx)

    dprint(
        "End mining pending transactions number: " + str(len(block.pendingTransaction))
    )
    dprint(
        "End mining validating transactions number: " + str(len(block.validating_list))
    )
