#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.candidate_block.candidate_block_main import (
    candidate_block,
)
from decentra_network.node.unl import Unl


def GetCandidateBlocks(custom_nodes_list=None):
    """
    Collects candidate blocks and candidate block hashes
    from connected unl nodes and returns them in the
    candidate_block class
    """

    nodes = (
        Unl.get_as_node_type(Unl.get_unl_nodes())
        if custom_nodes_list is None
        else custom_nodes_list
    )

    the_candidate_blocks = []
    the_candidate_block_hashes = []

    for node in nodes:
        if node.candidate_block is not None:
            the_candidate_blocks.append(node.candidate_block)
        if node.candidate_block_hash is not None:
            the_candidate_block_hashes.append(node.candidate_block_hash)

    return candidate_block(the_candidate_blocks, the_candidate_block_hashes)
