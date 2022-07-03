#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from lib.merkle_root import MerkleTree


def BlocksHash(block, part_of_blocks_hash, the_blocks_hash):
    """
    Calculates and returns the hash of the blocks.
    """

    blocks_hash_list = []
    if len(the_blocks_hash) == block.part_amount: 
        for will_added_blocks_hash in the_blocks_hash:
            blocks_hash_list.append(will_added_blocks_hash)
    else:
        new_part = MerkleTree(the_blocks_hash).getRootHash()
        the_blocks_hash.clear()
        part_of_blocks_hash.append(new_part)
    for part_of_blocks_hash_element in part_of_blocks_hash:
        blocks_hash_list.append(part_of_blocks_hash_element)
    

    return MerkleTree(blocks_hash_list).getRootHash()
