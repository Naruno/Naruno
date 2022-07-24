#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.transactions.check.check_transaction import CheckTransaction
from decentra_network.transactions.pending.save_pending import SavePending
from decentra_network.transactions.pending_to_validating import PendingtoValidating


def GetTransaction(
    block,
    the_transaction,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
):
    if CheckTransaction(
        block,
        the_transaction,
        custom_current_time,
        custom_sequence_number,
        custom_balance,
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
    ):
        SavePending(
            the_transaction,
            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
        )
        PendingtoValidating(block)
        return True
    else:
        return False
