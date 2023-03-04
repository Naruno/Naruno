#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from naruno.accounts.get_accounts import GetAccounts
from naruno.accounts.save_accounts import SaveAccounts
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.blocks_hash import GetBlockshash
from naruno.blockchain.block.blocks_hash import GetBlockshash_part
from naruno.blockchain.block.blocks_hash import SaveBlockshash
from naruno.blockchain.block.blocks_hash import SaveBlockshash_part
from naruno.blockchain.block.hash.calculate_hash import CalculateHash
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.rounds.round_1.checks.checks_main import \
    round_check
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import \
    Remove_Duplicates
from naruno.consensus.rounds.round_1.process.transactions.find_newly.find_newly_main import \
    find_newly
from naruno.consensus.rounds.round_1.process.transactions.find_validated.find_validated_main import \
    find_validated
from naruno.lib.log import get_logger
from naruno.node.get_candidate_blocks import GetCandidateBlocks
from naruno.node.server.server import server
from naruno.node.unl import Unl
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.get_transaction import GetTransaction
from naruno.transactions.pending.get_pending import GetPending
from naruno.transactions.process_the_transaction import \
    ProccesstheTransaction

logger = get_logger("CONSENSUS_FIRST_ROUND")


def transactions_main(block: Block, candidate_class: candidate_block,
                      unl_nodes: dict, clean=True) -> list:
    temp_validating_list = find_validated(block,
                                          candidate_class=candidate_class,
                                          unl_nodes=unl_nodes)

    newly_added_list = find_newly(block,
                                  temp_validating_list=temp_validating_list)

    block.validating_list = temp_validating_list

    block = Remove_Duplicates(block)

    pending_list_txs = GetPending()
    if clean:
        cleaned_lists = Cleaner(block, pending_list_txs)
        block.validating_list = cleaned_lists[0]
        pending_list_txs = cleaned_lists[1]

    logger.debug(f"Newly validating list {block.validating_list}")
        
    
    return temp_validating_list
