#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wallet.wallet import Wallet_Import, get_saved_wallet, Wallet_Delete


from lib.settings_system import the_settings, change_wallet


def delete_current_wallet():
    """
    Deletes the current wallet.
    """

    if not the_settings()["wallet"] == 0:
        saved_wallets = get_saved_wallet()
        selected_wallet_pubkey = Wallet_Import(int(the_settings()["wallet"]), 0)
        for each_wallet in saved_wallets:
            if selected_wallet_pubkey == saved_wallets[each_wallet]["publickey"]:
                change_wallet(0)
                Wallet_Delete(each_wallet)
    else:
        print("First wallet cannot be deleted.")
