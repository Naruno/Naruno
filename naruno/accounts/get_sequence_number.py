#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.accounts.get_accounts import GetAccounts
from naruno.transactions.pending.get_pending import GetPending
from naruno.wallet.wallet_import import Address


def GetSequanceNumber(user, account_list=None, dont_convert=False, block=None,custom_pending=None):
    user = Address(user) if not dont_convert else user
    sequence_number = 0

    the_account_list = GetAccounts() if account_list is None else account_list

    sequence_number = the_account_list[user][
        0] if user in the_account_list else 0

    if block is not None:
        the_pending = custom_pending if custom_pending is not None else GetPending()
        if not block.just_one_tx:
            for tx in block.validating_list + the_pending:
                if Address(tx.fromUser) == user:
                    sequence_number += 1
    return sequence_number
