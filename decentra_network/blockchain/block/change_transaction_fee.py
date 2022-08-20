#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.transactions.pending.get_pending import GetPendingLen


def ChangeTransactionFee(
    block,
    custom_pending_transaction_len=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
):
    """
    Increase transaction fee by 0.01 DNC for each block.default_optimum_transaction_number argument
    """
    pending_transactions = (GetPendingLen(
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)
                            if custom_pending_transaction_len is None else
                            custom_pending_transaction_len)
    total_len = len(block.validating_list) + pending_transactions
    if (total_len // block.default_optimum_transaction_number) != 0:
        increase = (total_len // block.default_optimum_transaction_number
                    ) * block.default_increase_of_fee
        block.transaction_fee += increase
    else:
        block.transaction_fee = block.default_transaction_fee
