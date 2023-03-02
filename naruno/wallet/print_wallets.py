#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.lib.mix.mixlib import menu_maker
from naruno.lib.settings_system import the_settings
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.wallet_import import wallet_import


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
        address = wallet_import(all_wallets.index(wallet), 3)
        if current_wallet != number:
            text = menu_maker(menu_number=number, menu_text=address)
        else:
            text = menu_maker(menu_number=number,
                              menu_text=f"{address} - CURRENTLY USED")
        print(text)
        result.append(text)
    return result
