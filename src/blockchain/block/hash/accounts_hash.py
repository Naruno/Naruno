#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from lib.merkle_root import MerkleTree


def AccountsHash(block, the_accounts):
    """
    Calculates and returns the hash of the accounts.
    """

    account_list = []

    new_part = MerkleTree(
        [account.get_hash() for account in the_accounts]
    ).getRootHash()
    account_list.append(new_part)

    for edited_account in block.edited_accounts:
        account_list.append(str(edited_account.get_hash()))

    block.edited_accounts.clear()

    return MerkleTree(account_list).getRootHash()
