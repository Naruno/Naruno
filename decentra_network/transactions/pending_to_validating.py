#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from decentra_network.transactions.pending.get_pending import GetPending
from decentra_network.transactions.pending.delete_pending import DeletePending


def PendingtoValidating(block, custom_PENDING_TRANSACTIONS_PATH=None):
    """
    Adds transactions to the verification list
    if there are suitable conditions.
    """

    if len(block.validating_list) < block.max_tx_number:
        if block.raund_2_starting_time is None:
            current_time = time.time()
            raund_1_starting_time = (
                current_time
                if block.raund_1_starting_time is None
                else block.raund_1_starting_time
            )
            if not (current_time - raund_1_starting_time) > (block.raund_1_time / 2):
                for tx in GetPending(
                    custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH
                ):
                    if len(block.validating_list) < block.max_tx_number:
                        block.validating_list.append(tx)
                        DeletePending(
                            tx,
                            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
                        )
