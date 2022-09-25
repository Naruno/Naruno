#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.mix.merkle_root import MerkleTree


def BlocksHash(block: Block, part_of_blocks_hash, the_blocks_hash):
    """
    Calculates and returns the hash of the blocks.
    """

    blocks_hash_list = [block.part_amount_cache]
    blocks_hash_list.extend(iter(the_blocks_hash))
    return MerkleTree(blocks_hash_list).getRootHash()
