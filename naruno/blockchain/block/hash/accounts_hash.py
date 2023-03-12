#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.lib.mix.merkle_root import MerkleTree


def AccountsHash(block, the_accounts):
    """
    Calculates and returns the hash of the accounts.
    """
    the_list = []
    if isinstance(the_accounts, list):
        the_list = the_accounts
        the_list = [account.get_hash()
                               for account in the_list]
    else:
        the_accounts.execute("SELECT * FROM account_list")
        the_list = the_accounts.fetchall()
        the_list = [str(account[0])+str(account[1])+str(account[2])
                               for account in the_list]

    account_list = MerkleTree(the_list).getRootHash()

    return account_list
