#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from getpass import getpass

from wallet.wallet import Wallet_Create


def create_a_wallet(password=None):
    """
    Creates a wallet.
    """

    if password is None:
        password = getpass("Password: ")
    Wallet_Create(password)
    del password
