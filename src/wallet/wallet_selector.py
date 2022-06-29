#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.get_saved_wallet import get_saved_wallet

from wallet.print_wallets import print_wallets


from lib.settings_system import change_wallet

from lib.log import get_logger

logger = get_logger("WALLET")

def wallet_selector(new_wallet_number=None):
    """
    Changes the current wallet.
    """
    new_wallet_from_function = None

    all_wallets = list(get_saved_wallet())
    if not len(all_wallets) == 0:

        while True:
            try:
                if new_wallet_number is None:
                    new_wallet = input("Please select wallet: ")
                else:
                    new_wallet = new_wallet_number
                if int(new_wallet) in list(range(len(all_wallets))):
                    new_wallet_from_function = change_wallet(int(new_wallet))
                    logger.info("New Wallets:")
                    print_wallets()
                    break
                else:
                    logger.error("There is no such wallet")
                    new_wallet_from_function = False
                    break
            except:
                logger.error("This is not a number")
                if not new_wallet_number is None:
                    new_wallet_from_function = False
                    break
    else:
        logger.error("There is no wallet")
        new_wallet_from_function = False
    
    return new_wallet_from_function
