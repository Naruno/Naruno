#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from transactions.send import send

from wallet.wallet import Wallet_Import


def send_coin(coin_amount, to_user):
    """
    A function for sending coins.

    Inputs:
      * coin_amount: A int or float amount to be sent.
      * to_user: Receiver's address.
    """

    my_public_key = Wallet_Import(0,0)
    my_private_key = Wallet_Import(0,1)

    if isinstance(coin_amount, int):
        coin_amount = float(coin_amount)

    if not isinstance(coin_amount, float):
        print("This is not int or float coin amount.")
        return None

    if coin_amount < 0:
        print("This is negative coin amount.")
        return None

    send(my_public_key = my_public_key, my_private_key = my_private_key, to_user = to_user, amount = coin_amount)
