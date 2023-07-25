#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from urllib.request import urlopen

from naruno.accounts.get_accounts import GetAccounts
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.get_minumum_transfer_amount import \
    GetMinimumTransferAmount
from naruno.lib.settings_system import the_settings
from naruno.transactions.pending.get_pending import GetPending
from naruno.wallet.wallet_import import Address


def GetBalance(user,
               account_list=None,
               dont_convert=False,
               block=None,
               custom_TEMP_BLOCK_PATH=None,
               tx_signature=None,
               custom_pending=None):
    """
    Returns the users balance.
    """
    address = Address(user) if not dont_convert else user

    balance = GetMinimumTransferAmount(
        block=block, custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)

    if the_settings()["baklava"]:
        balance = float(
            urlopen(
                f"http://test_net.1.naruno.org:8000/balance/get/?address={address}"
            ).read().decode("utf-8").replace("\n", ""))
    else:
        if block is None:
            try:
                block = GetBlock(custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH)
            except TypeError:
                return None

        balance = -block.minumum_transfer_amount

        the_account_list = GetAccounts(
        ) if account_list is None else account_list
        balance += the_account_list[address][
            1] if address in the_account_list else 0

        if not block.just_one_tx:
            the_pending = custom_pending if custom_pending is not None else GetPending()
            for tx in block.validating_list + the_pending:
                sub_control = True
                if tx_signature is not None:
                    if tx.signature == tx_signature:
                        sub_control = False
                if Address(tx.fromUser) == user and sub_control:
                    balance -= float(tx.amount) + float(tx.transaction_fee)

    return balance
