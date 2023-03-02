#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from hashlib import sha256

from naruno.config import *
from naruno.lib.config_system import get_config
from naruno.wallet.get_saved_wallet import get_saved_wallet


def save_to_wallet_list(publicKey, privateKey, password):
    wallet_list = get_saved_wallet()

    wallet_list[publicKey] = {}

    wallet_list[publicKey]["publickey"] = publicKey.replace("\n", "")
    wallet_list[publicKey]["privatekey"] = privateKey

    wallet_list[publicKey]["password_sha256"] = sha256(
        password.encode("utf-8")).hexdigest()

    save_wallet_list(wallet_list)


def save_wallet_list(wallet_list):

    os.chdir(get_config()["main_folder"])
    with open(WALLETS_PATH, "w") as wallet_list_file:
        json.dump(wallet_list, wallet_list_file, indent=4)
