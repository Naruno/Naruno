#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from node.unl import get_unl_nodes, get_as_node_type

from blockchain.candidate_block.candidate_block_main import candidate_block


def GetCandidateBlocks():
    """
    Collects candidate blocks and candidate block hashes 
    from connected unl nodes and returns them in the 
    candidate_block class
    """    

    nodes = get_as_node_type(get_unl_nodes())

    the_candidate_blocks = []
    the_candidate_block_hashes = []

    for node in nodes:
        if node.candidate_block:
            already_in_list_candidate_blocks = False
            for other_blocks in the_candidate_blocks[:]:
                if other_blocks["signature"] == node.candidate_block["signature"]:
                    already_in_list_candidate_blocks = True
            if not already_in_list_candidate_blocks:
                the_candidate_blocks.append(node.candidate_block)
        if node.candidate_block_hash:
            already_in_list_candidate_block_hashes = False
            for other_block_hashes in the_candidate_block_hashes[:]:
                if (
                    other_block_hashes["signature"]
                    == node.candidate_block_hash["signature"]
                ):
                    already_in_list_candidate_block_hashes = True
            if not already_in_list_candidate_block_hashes:
                the_candidate_block_hashes.append(node.candidate_block_hash)

    return candidate_block(the_candidate_blocks, the_candidate_block_hashes)
