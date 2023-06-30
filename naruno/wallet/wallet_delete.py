#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from naruno.config import WALLETS_PATH
from naruno.lib.config_system import get_config
from naruno.lib.log import get_logger
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.save_wallet_list import save_wallet_list

logger = get_logger("WALLET")

def wallet_delete(account):
    saved_wallet = get_saved_wallet()
    if account in saved_wallet:
        del saved_wallet[account]

        save_wallet_list(saved_wallet)
        logger.info(f"Wallet {account} deleted")
        return True
    else:
        logger.error(f"Wallet {account} not found")
        return False
