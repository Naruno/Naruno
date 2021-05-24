#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from lib.mixlib import dprint
from lib.merkle_root import MerkleTree


def CalculateHash(block):
    """
    Calculates and returns the hash of the block.
    """

    # Transaction
    tx_list = []
    dprint(len(block.validating_list))
    for element in block.validating_list[:]:
        dprint(element)
        tx_list.append(element.signature)
    if len(tx_list) != 0:
        tx_hash = MerkleTree(tx_list).getRootHash()
    else:
        tx_hash = "0"
        
    # Account
    ac_list = []
    for element in block.Accounts[:]:
        ac_list.append(element.Address)
    dprint(ac_list)
    ac_hash = MerkleTree(ac_list).getRootHash()

    # Other elements
    main_list = []
    main_list.append(block.previous_hash)
    main_list.append(str(block.sequance_number))
    main_list.append(ac_hash)
    main_list.append(tx_hash)
    main_list.append(block.default_transaction_fee)
    main_list.append(block.default_increase_of_fee)

    # Calculating and returning
    return MerkleTree(main_list).getRootHash()
