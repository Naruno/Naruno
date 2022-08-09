#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.lib.mix.merkle_root import MerkleTree


def AccountsHash(block, the_accounts):
    """
    Calculates and returns the hash of the accounts.
    """

    account_list = MerkleTree([account.get_hash()
                               for account in the_accounts]).getRootHash()

    return MerkleTree(account_list).getRootHash()
