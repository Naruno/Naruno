#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.config import *
from naruno.lib.encryption import encrypt
from naruno.wallet.ellipticcurve.privateKey import PrivateKey
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.save_wallet_list import save_to_wallet_list


def wallet_create(password, save=True):

    my_private_key = PrivateKey()
    my_public_key = my_private_key.publicKey()

    if save != True:
        return my_private_key
    encrypted_key = (encrypt(my_private_key.toPem(), password)
                     if list(get_saved_wallet()) else my_private_key.toPem())

    del my_private_key
    save_to_wallet_list(my_public_key.toPem(), encrypted_key, password)
    return encrypted_key
