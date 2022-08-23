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
from decentra_network.consensus.rounds.round_1.process.transactions.transactions_main import \
    transactions_main
from decentra_network.lib.log import get_logger
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.process_the_transaction import \
    ProccesstheTransaction

logger = get_logger("CONSENSUS_FIRST_ROUND")


def round_process(
    block: Block,
    candidate_class: candidate_block,
    unl_nodes: dict,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
) -> Block:

    transactions_main(block,
                      candidate_class=candidate_class,
                      unl_nodes=unl_nodes)

    block.round_1 = True
    block.round_2_starting_time = int(time.time())

    account_list = GetAccounts(
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH)
    ProccesstheTransaction(block,
                           account_list,
                           custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH)

    part_of_blocks_hash = GetBlockshash_part(
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH)
    the_blocks_hash = GetBlockshash(
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH)
    block.hash = CalculateHash(block, part_of_blocks_hash, the_blocks_hash,
                               account_list)

    logger.debug(f"Block hash {block.hash}")

    SaveBlock(
        block,
        custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
        custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
        custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
        custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
    )
    return block
