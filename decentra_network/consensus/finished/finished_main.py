#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.apps.apps_trigger import AppsTrigger
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.block.save_block_to_blockchain_db import \
    SaveBlockstoBlockchainDB
from decentra_network.config import BLOCKS_PATH
from decentra_network.config import CONNECTED_NODES_PATH
from decentra_network.config import LOADING_ACCOUNTS_PATH
from decentra_network.config import LOADING_BLOCK_PATH
from decentra_network.config import LOADING_BLOCKSHASH_PART_PATH
from decentra_network.config import LOADING_BLOCKSHASH_PATH
from decentra_network.config import PENDING_TRANSACTIONS_PATH
from decentra_network.config import TEMP_ACCOUNTS_PATH
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.config import TEMP_BLOCKSHASH_PART_PATH
from decentra_network.config import TEMP_BLOCKSHASH_PATH
from decentra_network.config import UNL_NODES_PATH
from decentra_network.consensus.finished.transactions.transactions_main import \
    transactions_main
from decentra_network.consensus.time.true_time.true_time_main import true_time
from decentra_network.lib.log import get_logger
from decentra_network.transactions.pending_to_validating import \
    PendingtoValidating

logger = get_logger("CONSENSUS")


def finished_main(
    block: Block,
    custom_TEMP_BLOCK_PATH: str = None,
    custom_BLOCKS_PATH: str = None,
    custom_TEMP_ACCOUNTS_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PATH: str = None,
    custom_TEMP_BLOCKSHASH_PART_PATH: str = None,
) -> None:
    if true_time(block):
        block.newly = False
        logger.info("Consensus proccess is complated, the block will be reset")

        the_BLOCKS_PATH = (
            BLOCKS_PATH if custom_BLOCKS_PATH is None else custom_BLOCKS_PATH
        )
        the_TEMP_ACCOUNTS_PATH = (
            TEMP_ACCOUNTS_PATH
            if custom_TEMP_ACCOUNTS_PATH is None
            else custom_TEMP_ACCOUNTS_PATH
        )
        the_TEMP_BLOCKSHASH_PATH = (
            TEMP_BLOCKSHASH_PATH
            if custom_TEMP_BLOCKSHASH_PATH is None
            else custom_TEMP_BLOCKSHASH_PATH
        )
        the_TEMP_BLOCKSHASH_PART_PATH = (
            TEMP_BLOCKSHASH_PART_PATH
            if custom_TEMP_BLOCKSHASH_PART_PATH is None
            else custom_TEMP_BLOCKSHASH_PART_PATH
        )

        the_TEMP_BLOCK_PATH = (
            TEMP_BLOCK_PATH
            if custom_TEMP_BLOCK_PATH is None
            else custom_TEMP_BLOCK_PATH
        )

        current_blockshash_list = GetBlockshash(
            custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH
        )
        reset_block = block.reset_the_block(current_blockshash_list)
        if reset_block != False:
            block2 = reset_block[0]
            AppsTrigger(block2)
            transactions_main(block2)
            SaveBlockshash(
                current_blockshash_list,
                custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
            )
            SaveBlockstoBlockchainDB(
                block2,
                custom_BLOCKS_PATH=the_BLOCKS_PATH,
                custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
                custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
                custom_TEMP_BLOCKSHASH_PART_PATH=the_TEMP_BLOCKSHASH_PART_PATH,
            )
        PendingtoValidating(block)
        SaveBlock(
            block,
            custom_TEMP_BLOCK_PATH=the_TEMP_BLOCK_PATH,
            custom_TEMP_ACCOUNTS_PATH=the_TEMP_ACCOUNTS_PATH,
            custom_TEMP_BLOCKSHASH_PATH=the_TEMP_BLOCKSHASH_PATH,
            custom_TEMP_BLOCKSHASH_PART_PATH=the_TEMP_BLOCKSHASH_PART_PATH,
        )
        return True
    else:
        logger.info("Consensus proccess is complated, waiting for the true time")
        return False
