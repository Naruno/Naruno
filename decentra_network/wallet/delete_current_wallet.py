#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet 

from decentra_network.wallet.ellipticcurve.wallet_delete import wallet_delete


from decentra_network.lib.settings_system import the_settings, change_wallet


from decentra_network.lib.log import get_logger

logger = get_logger("WALLET")


def delete_current_wallet():
    """
    Deletes the current wallet.
    """

    if the_settings()["wallet"] != 0:
        saved_wallets = get_saved_wallet()
        selected_wallet_pubkey = wallet_import(int(the_settings()["wallet"]), 0)
        for each_wallet in saved_wallets:
            if selected_wallet_pubkey == saved_wallets[each_wallet]["publickey"]:
                change_wallet(0)
                if wallet_delete(each_wallet):
                    logger.info(f"Wallet deleted: {each_wallet}")
                    return True
    else:
        logger.info("First wallet cannot be deleted.")
        return False
