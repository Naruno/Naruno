#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sqlite3
from urllib.request import urlopen

from naruno.accounts.get_accounts import GetAccounts
from naruno.blockchain.block.get_block import GetBlock
from naruno.lib.settings_system import the_settings
from naruno.wallet.wallet_import import Address


def GetMinimumTransferAmount(block=None, custom_TEMP_BLOCK_PATH=None):
    """
    Returns the minimum transfer amount.
    """
    if the_settings()["baklava"]:
        minimum_transfer_amount = int(
            urlopen(
                "http://test_net.1.naruno.org:8000/blockminumumtransferamount/get/"
            ).read().decode("utf-8"))
    else:
        if block is None:
            try:
                block = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
            except FileNotFoundError:
                return None
        minimum_transfer_amount = block.minumum_transfer_amount

    return minimum_transfer_amount
