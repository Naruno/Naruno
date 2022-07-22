#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.transactions.pending.get_pending import GetPending


def ChangeTransactionFee(
    block,
    custom_pending_transactions=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
):
    """
    Increase transaction fee by 0.01 DNC for each block.default_optimum_transaction_number argument
    """
    pending_transactions = (GetPending(
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)
                            if custom_pending_transactions is None else
                            custom_pending_transactions)
    if (len(pending_transactions + block.validating_list) //
            block.default_optimum_transaction_number) != 0:
        increase = (len(pending_transactions + block.validating_list) //
                    block.default_optimum_transaction_number
                    ) * block.default_increase_of_fee
        block.transaction_fee += increase
    else:
        block.transaction_fee = block.default_transaction_fee
