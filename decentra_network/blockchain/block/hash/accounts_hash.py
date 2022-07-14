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

    new_part = MerkleTree(
        [account.get_hash() for account in the_accounts]
    ).getRootHash()
    account_list = [new_part]
    account_list.extend(
        str(edited_account.get_hash()) for edited_account in block.edited_accounts
    )

    block.edited_accounts.clear()

    return MerkleTree(account_list).getRootHash()
