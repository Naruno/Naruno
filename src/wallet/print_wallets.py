#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.wallet import Wallet_Import, get_saved_wallet

from lib.mixlib import menu_maker
from lib.settings_system import the_settings


def print_wallets():
    """
    Prints the wallets.
    """

    all_wallets = list(get_saved_wallet())
    current_wallet = the_settings()["wallet"]
    print("\nWallets:")
    result = []
    for wallet in all_wallets:
        number = all_wallets.index(wallet)
        address = Wallet_Import(all_wallets.index(wallet), 3)
        if not current_wallet == number:
            text = menu_maker(menu_number=number, menu_text=address)
            print(text)
            result.append(text)
        else:
            text = menu_maker(menu_number=number, menu_text=address + " - CURRENTLY USED")
            print(text)
            result.append(text)
    return result
