#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from node.unl import get_unl_nodes, get_as_node_type

from blockchain.candidate_block.candidate_block_main import candidate_block


def GetCandidateBlocks():
    nodes = get_as_node_type(get_unl_nodes())

    the_candidate_blocks = []
    the_candidate_block_hashes = []

    for node in nodes:
        if node.candidate_block:
            the_candidate_blocks.append(node.candidate_block)
        if node.candidate_block_hash:
            the_candidate_block_hashes.append(node.candidate_block_hash)
    
    return candidate_block(the_candidate_blocks, the_candidate_block_hashes)
