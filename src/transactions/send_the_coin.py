#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from hashlib import sha256

from wallet.wallet import Wallet_Import

from transactions.send_coin import send_coin

from blockchain.block.get_block import GetBlock

from lib.settings_system import the_settings


def send_the_coin(receiver, temp_coin_amount, password):
    type_control = False
    try:
        float(temp_coin_amount)
        type_control = True
    except:
        print("This is not float coin amount.")

    if type_control and not float(temp_coin_amount) < GetBlock().minumum_transfer_amount:
        if Wallet_Import(int(the_settings()["wallet"]), 2) == sha256(password.encode("utf-8")).hexdigest():
            print(password)
            send_coin(float(temp_coin_amount), receiver, password)
        else:
            print("Password is not correct")
