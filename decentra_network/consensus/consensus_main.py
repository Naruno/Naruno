#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.apps.apps_trigger import AppsTrigger
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.block.save_block_to_blockchain_db import (
    SaveBlockstoBlockchainDB,
)
from decentra_network.consensus.consensus_first_round import consensus_round_1
from decentra_network.consensus.consensus_second_round import consensus_round_2
from decentra_network.lib.log import get_logger
from decentra_network.transactions.my_transactions.save_to_my_transaction import (
    SavetoMyTransaction,
)
from decentra_network.transactions.my_transactions.validate_transaction import (
    ValidateTransaction,
)
from decentra_network.transactions.pending_to_validating import PendingtoValidating
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import

logger = get_logger("CONSENSUS")


def consensus_trigger():
    """
    Consensus process consists of 2 stages. This function makes
    the necessary redirects according to the situation and works
    to shorten the block time.
    """

    block = GetBlock()

    logger.info(
        f"BLOCK#{block.sequance_number}:{block.empty_block_number} Consensus process started"
    )

    if block.validated:
        true_time = (
            block.genesis_time
            + block.block_time
            + ((block.sequance_number + block.empty_block_number) * block.block_time)
        )
        if block.newly:
            true_time -= 1
            logger.info(
                "Consensus proccess is complated but the time is not true, will be waiting for the true time"
            )
        if int(time.time()) >= true_time:
            block.newly = False
            logger.info("Consensus proccess is complated, the block will be reset")

            current_blockshash_list = GetBlockshash()
            reset_block = block.reset_the_block(current_blockshash_list)
            if reset_block != False:
                block2 = reset_block[0]
                AppsTrigger(block2)
                my_address = wallet_import(-1, 3)
                my_public_key = wallet_import(-1, 0)
                for tx in block2.validating_list:
                    if tx.toUser == my_address:
                        SavetoMyTransaction(tx, validated=True)
                    elif tx.fromUser == my_public_key:
                        ValidateTransaction(tx)
                SaveBlockshash(current_blockshash_list)
                SaveBlockstoBlockchainDB(block2)

            SaveBlock(block)
    else:
        PendingtoValidating(block)
        if block.raund_1_starting_time is None:
            block.raund_1_starting_time = int(time.time())
            SaveBlock(block)
        if not block.raund_1:
            logger.info("First round is starting")
            consensus_round_1(block)
            logger.info("First round is done")
        elif not block.raund_2:
            logger.info("Second round is starting")
            consensus_round_2(block)
            logger.info("Second round is done")

    logger.info("Consensus process is done")
