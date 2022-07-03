#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from lib.merkle_root import MerkleTree


def TransactionsHash(block):
    """
    Calculates and returns the hash of the validating list.
    """
    tx_list = []
    for element in block.validating_list[:]:
        tx_list.append(element.signature)
    if len(tx_list) != 0:
        tx_hash = MerkleTree(tx_list).getRootHash()
    else:
        tx_hash = "0"

    return tx_hash
