#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def ChangeTransactionFee(block):
    """
    Increase transaction fee by 0.01 DNC for each block.default_optimum_transaction_number argument
    """
    if not (len(block.pendingTransaction + block.validating_list) // block.default_optimum_transaction_number) == 0:
        increase = (len(block.pendingTransaction + block.validating_list) // block.default_optimum_transaction_number) * block.default_increase_of_fee
        block.transaction_fee += increase
    else:
        block.transaction_fee = block.default_transaction_fee
