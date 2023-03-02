#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from base64 import b64decode
from base64 import b64encode
from binascii import hexlify
from binascii import unhexlify
from hashlib import sha256
from random import SystemRandom
from sys import version_info as pyVersion

from naruno.config import *
from naruno.lib.config_system import get_config
from naruno.lib.encryption import decrypt
from naruno.lib.encryption import encrypt
from naruno.lib.settings_system import the_settings
from naruno.wallet.ellipticcurve.privateKey import PrivateKey
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.save_wallet_list import save_to_wallet_list
from naruno.wallet.wallet_create import wallet_create


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
        my_address = "".join([
            l.strip() for l in my_address.splitlines()
            if l and not l.startswith("-----")
        ])
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
    the_public_key = "".join([
        l.strip() for l in publickey.splitlines()
        if l and not l.startswith("-----")
    ])
    return sha256(
        sha256(the_public_key.encode("utf-8")).hexdigest().encode(
            "utf-8")).hexdigest()[-40:]
