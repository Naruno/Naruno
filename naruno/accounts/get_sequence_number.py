#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.accounts.get_accounts import GetAccounts
from naruno.transactions.pending.get_pending import GetPending
from naruno.wallet.wallet_import import Address


def GetSequanceNumber(user, account_list=None, dont_convert=False, block=None):
    user = Address(user) if not dont_convert else user
    sequence_number = 0
    the_account_list = GetAccounts() if account_list is None else account_list
    the_account_list.execute(
        f"SELECT * FROM account_list WHERE address = '{user}'")
    for Accounts in the_account_list.fetchall():
        sequence_number = Accounts[1]
        break
    if block is not None:
        if not block.just_one_tx:
            for tx in block.validating_list + GetPending():
                if Address(tx.fromUser) == user:
                    sequence_number += 1
    return sequence_number
