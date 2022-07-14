#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet 

from decentra_network.lib.mix.mixlib import menu_maker
from decentra_network.lib.settings_system import the_settings


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
            text = menu_maker(
                menu_number=number, menu_text=f"{address} - CURRENTLY USED"
            )
        print(text)
        result.append(text)
    return result
