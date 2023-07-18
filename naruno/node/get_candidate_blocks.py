#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
import copy
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.node.unl import Unl
import naruno

our_candidates = []

def self_candidates(block: Block, reset=False):
            the_block = copy.copy(block)
            the_block_2 = copy.copy(block)
            if not len(naruno.node.get_candidate_blocks.our_candidates) == 0 and not reset:
                the_block = naruno.node.get_candidate_blocks.our_candidates[2]
                the_block_2 = naruno.node.get_candidate_blocks.our_candidates[3]

            new_list = []
            signature_list = []
            a_time = "self"
            for element in block.validating_list:
                new_list.append(element.dump_json())
                signature_list.append(element.signature)
            will_add_candidate_block = None
            will_add_candidate_block_hash = None
            if not len(naruno.node.get_candidate_blocks.our_candidates) == 0 and not reset:
                will_add_candidate_block = naruno.node.get_candidate_blocks.our_candidates[0]
                will_add_candidate_block_hash = naruno.node.get_candidate_blocks.our_candidates[1]
            
            first_validating = [i.dump_json() for i in the_block.validating_list]
            second_validating = [i.dump_json() for i in block.validating_list]
            if not block.round_1 or will_add_candidate_block is None:
                if block.sequence_number+block.empty_block_number > the_block.sequence_number+the_block.empty_block_number or block.sequence_number == 0 or reset or will_add_candidate_block is None:
                    will_add_candidate_block = {
                                "action": "myblock",
                                "transaction": new_list,
                                "signature": a_time,
                                "sequence_number": block.sequence_number+block.empty_block_number,
                                "total_length": len(new_list)
                            }
                    the_block = copy.copy(block)
            if (block.round_1 and not block.round_2)  or block.sequence_number == 0 or will_add_candidate_block_hash is None:
                if block.sequence_number+block.empty_block_number > the_block_2.sequence_number+the_block_2.empty_block_number or block.sequence_number == 0 or reset or will_add_candidate_block_hash is None:
                    will_add_candidate_block_hash = {
                                "action":
                                "myblockhash",
                                "hash":
                                block.hash,
                                "previous_hash":
                                block.previous_hash,
                                "signature":
                                a_time,
                                "sequence_number":
                                block.sequence_number+block.empty_block_number,
                            }
                    
                    the_block_2 = copy.copy(block)
                    
                
                
            
            naruno.node.get_candidate_blocks.our_candidates = [will_add_candidate_block, will_add_candidate_block_hash, the_block, the_block_2]
            

            return [the_block, the_block_2]


def our_candidates_f(block: Block, reset=False):
    
    self_candidates(block, reset=reset)
    return naruno.node.get_candidate_blocks.our_candidates


def GetCandidateBlocks(custom_nodes_list=None, block: Block = None, reset=False):
    """
    Collects candidate blocks and candidate block hashes
    from connected unl nodes and returns them in the
    candidate_block class
    """

    nodes = (Unl.get_as_node_type(Unl.get_unl_nodes()) + Unl.get_as_node_type(Unl.get_unl_nodes(),c_type=3)
             if custom_nodes_list is None else custom_nodes_list)

    the_candidate_blocks = []
    the_candidate_block_hashes = []
    id_control_list = []

    for node in nodes:
        if node.candidate_block is not None:
            the_id = ""
            if int(node.candidate_block["sequence_number"]
                   ) == block.sequence_number+block.empty_block_number:
                the_id = node.candidate_block["id"]
                if not the_id in id_control_list:
                    the_candidate_blocks.append(node.candidate_block)
            else:
                for i in node.candidate_block_history:
                    if i["sequence_number"] == block.sequence_number+block.empty_block_number:
                        the_id = i["id"]
                        if not the_id in id_control_list:
                            the_candidate_blocks.append(i)
                        
            if not the_id in id_control_list:
                id_control_list.append(the_id)
        else:
            pass
        if node.candidate_block_hash is not None:
            if (int(node.candidate_block_hash["sequence_number"]) ==
                    block.sequence_number+block.empty_block_number):
                the_candidate_block_hashes.append(node.candidate_block_hash)
            else:
                for i in node.candidate_block_hash_history:
                    if i["sequence_number"] == block.sequence_number+block.empty_block_number:
                        the_candidate_block_hashes.append(i)
        else:
            pass

    if block is not None:
        the_candidates = our_candidates_f(block, reset=reset)

        the_candidate_blocks.append(the_candidates[0])
        the_candidate_block_hashes.append(the_candidates[1])


    not_none_the_candidate_blocks = []

    for none_candidate_block in the_candidate_block_hashes:
        if not none_candidate_block["hash"] == None:
            not_none_the_candidate_blocks.append(none_candidate_block)

    return candidate_block(the_candidate_blocks, not_none_the_candidate_blocks)
