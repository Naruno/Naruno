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

from decentra_network.config import *
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet 

logger = get_logger("WALLET")


def wallet_delete(account):
    saved_wallet = get_saved_wallet()
    if account in saved_wallet:
        del saved_wallet[account]

        os.chdir(get_config()["main_folder"])
        with open(WALLETS_PATH, "w") as wallet_list_file:
            json.dump(saved_wallet, wallet_list_file, indent=4)
        logger.info(f"Wallet {account} deleted")
        return True
    else:
        logger.error(f"Wallet {account} not found")
        return False
