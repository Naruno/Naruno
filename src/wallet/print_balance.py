#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from accounts.get_balance import GetBalance
from blockchain.block.get_block import GetBlock
from wallet.wallet_import import wallet_import


def print_balance():
    """
    Prints the current wallet balance.
    """

    balance = GetBalance(GetBlock(), wallet_import(-1, 0))
    print(balance)
    return balance
