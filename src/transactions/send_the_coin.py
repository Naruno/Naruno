#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from hashlib import sha256

from transactions.send import send

from wallet.wallet import Wallet_Import


from blockchain.block.get_block import GetBlock

from lib.settings_system import the_settings


def send_the_coin(to_user, coin_amount, password):
    """
    A function for sending coins.

    Inputs:
      * to_user: Receiver's address.
      * coin_amount: A int or float amount to be sent.
      * password: Password of wallet.
    """

    try:
        coin_amount = float(coin_amount)
    except ValueError:
        print("This is not float coin amount.")
        return False

    if isinstance(coin_amount, int):
                coin_amount = float(coin_amount)

    if not isinstance(coin_amount, float):
                print("This is not int or float coin amount.")
                return None

    if coin_amount < 0:
                print("This is negative coin amount.")
                return None


    if not coin_amount < GetBlock().minumum_transfer_amount:
        if Wallet_Import(int(the_settings()["wallet"]), 2) == sha256(password.encode("utf-8")).hexdigest():
            my_public_key = Wallet_Import(-1, 0)
            my_private_key = Wallet_Import(-1, 1, password)

            send(
                my_public_key=my_public_key,
                my_private_key=my_private_key,
                to_user=to_user,
                password=password,
                amount=coin_amount,
            )

            del my_private_key

        else:
            print("Password is not correct")
