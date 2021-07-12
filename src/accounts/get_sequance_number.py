#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.wallet import Address

from accounts.account import GetAccounts


def GetSequanceNumber(user, block):
    user = Address(user)
    sequance_number = 0
    for Accounts in GetAccounts():

        if Accounts.Address == user:

            sequance_number = Accounts.sequance_number

            for trans in block.pendingTransaction + block.validating_list:
                if user == trans.fromUser:
                    sequance_number += 1

            return sequance_number
    return sequance_number
