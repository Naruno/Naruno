#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import GetBlockshash_part
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from decentra_network.consensus.rounds.round_1.checks.checks_main import \
    round_check
from decentra_network.consensus.rounds.round_1.process.transactions.checks.duplicated import \
    Remove_Duplicates
from decentra_network.consensus.rounds.round_1.process.transactions.find_newly.find_newly_main import \
    find_newly
from decentra_network.consensus.rounds.round_1.process.transactions.find_validated.find_validated_main import \
    find_validated
from decentra_network.lib.log import get_logger
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.process_the_transaction import \
    ProccesstheTransaction

logger = get_logger("CONSENSUS_FIRST_ROUND")


def transactions_main(block: Block, candidate_class: candidate_block,
                      unl_nodes: dict) -> list:
    temp_validating_list = find_validated(block,
                                          candidate_class=candidate_class,
                                          unl_nodes=unl_nodes)

    newly_added_list = find_newly(block,
                                  temp_validating_list=temp_validating_list)

    block.validating_list = temp_validating_list

    Remove_Duplicates(block)

    logger.debug(f"Newly validating list {block.validating_list}")

    [
        server.send_transaction(each_newly) if GetTransaction(
            block, each_newly) else None for each_newly in newly_added_list
    ]
    return temp_validating_list
