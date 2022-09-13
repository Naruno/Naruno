#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Decentra Network Developers
Copyright (c) 2018 Stark Bank S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import os
from base64 import b64decode
from base64 import b64encode
from binascii import hexlify
from binascii import unhexlify
from hashlib import sha256
from random import SystemRandom
from sys import version_info as pyVersion

from decentra_network.config import *
from decentra_network.lib.config_system import get_config
from decentra_network.lib.encryption import decrypt
from decentra_network.lib.encryption import encrypt
from decentra_network.lib.settings_system import the_settings
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet 
from decentra_network.wallet.ellipticcurve.save_wallet_list import save_to_wallet_list
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create


def wallet_import(wallet, mode, password=None):
    """
    A function for get info about a wallet.

    Inputs:
      * account: Account index of saved accounts (if you give -1 the default wallet will use)
      * mode: Information mode [0 = Public key | 1 = Private key (needs password) | 2 = Returns sha256 of password | 3 = Returns the address of account]
      * password: Some function needed password for operation you can give with this input
    """

    account = wallet

    temp_saved_wallet = get_saved_wallet()

    number_of_wallet = len(temp_saved_wallet)
    if not number_of_wallet:
        wallet_create("123")
        temp_saved_wallet = get_saved_wallet()

    if isinstance(wallet, int):
        if wallet == -1:
            account = list(temp_saved_wallet)[the_settings()["wallet"]]

        elif wallet <= (len(temp_saved_wallet) - 1):
            account = list(temp_saved_wallet)[account]
        else:
            return False
    if mode == 0:
        return temp_saved_wallet[account]["publickey"]
    elif mode == 1:
        if password is None:
            if list(temp_saved_wallet).index(account) != 0:
                return False
            my_private_key = temp_saved_wallet[account]["privatekey"]
            return my_private_key

        elif list(temp_saved_wallet).index(account) != 0:

            return decrypt(temp_saved_wallet[account]["privatekey"], password)
        else:
            if wallet != -1:
                return False
            my_private_key = temp_saved_wallet[account]["privatekey"]
            return my_private_key
    elif mode == 2:
        return temp_saved_wallet[account]["password_sha256"]

    elif mode == 3:
        my_address = temp_saved_wallet[account]["publickey"]
        my_address = "".join(
            [
                l.strip()
                for l in my_address.splitlines()
                if l and not l.startswith("-----")
            ]
        )
        my_address = Address(my_address)
        return my_address
    else:
        return False


def wallet_import_all(mode, password=None):
    temp_saved_wallet = get_saved_wallet()
    the_result = []

    for account in temp_saved_wallet:
        the_result.append(wallet_import(account, mode, password))
    return the_result


def Address(publickey):
    the_public_key = "".join(
        [l.strip() for l in publickey.splitlines() if l and not l.startswith("-----")]
    )
    return sha256(
        sha256(the_public_key.encode("utf-8")).hexdigest().encode("utf-8")
    ).hexdigest()[-40:]
