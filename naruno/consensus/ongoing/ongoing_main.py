#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.block.block_main import Block
from naruno.blockchain.block.save_block import SaveBlock
from naruno.blockchain.candidate_block.candidate_block_main import \
    candidate_block
from naruno.consensus.rounds.round_1.round_1_main import \
    consensus_round_1
from naruno.consensus.rounds.round_2.round_2_main import \
    consensus_round_2
from naruno.lib.log import get_logger
from naruno.node.client.client import client
from naruno.node.server.server import server
from naruno.transactions.cleaner import Cleaner
from naruno.transactions.pending.get_pending import GetPending
logger = get_logger("CONSENSUS")


def ongoing_main(
    block: Block,
    custom_candidate_class: candidate_block = None,
    custom_unl_nodes: dict = None,
    custom_UNL_NODES_PATH: str = None,
    custom_server: server = None,
    custom_unl: client = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
    custom_shares=None,
    custom_fee_address=None,
    pass_sync=False,
    clean=True
) -> Block:

    block.sync_empty_blocks() if pass_sync is False else None
    SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )    

    if not block.round_1:    
        logger.debug("First round is starting")
        if clean:
            cleaned = Cleaner(block, pending_list_txs=GetPending())
            block.validating_list = cleaned[0]      
        consensus_round_1(
            block,
            custom_candidate_class=custom_candidate_class,
            custom_unl_nodes=custom_unl_nodes,
            custom_UNL_NODES_PATH=custom_UNL_NODES_PATH,
            custom_server=custom_server,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
            custom_shares=custom_shares,
            custom_fee_address=custom_fee_address,
            clean=clean
        )
        logger.debug("First round is done")
    elif not block.round_2:
        logger.debug("Second round is starting")
        consensus_round_2(
            block,
            candidate_class=custom_candidate_class,
            unl_nodes=custom_unl_nodes,
            custom_server=custom_server,
            custom_unl=custom_unl,
            custom_TEMP_BLOCK_PATH=custom_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=custom_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=custom_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=custom_TEMP_BLOCKSHASH_PART_PATH,
        )
        logger.debug("Second round is done")
    return block
