#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.apps.apps_trigger import AppsTrigger
from decentra_network.blockchain.block.block_main import Block
from decentra_network.blockchain.block.blocks_hash import (GetBlockshash,
                                                           SaveBlockshash)
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.block.save_block_to_blockchain_db import \
    SaveBlockstoBlockchainDB
from decentra_network.consensus.finished.transactions.transactions_main import \
    transactions_main
from decentra_network.consensus.rounds.round_1.round_1_main import \
    consensus_round_1
from decentra_network.consensus.rounds.round_2.round_2_main import \
    consensus_round_2
from decentra_network.consensus.time.true_time.true_time import true_time
from decentra_network.lib.log import get_logger
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.transactions.pending_to_validating import \
    PendingtoValidating
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import

logger = get_logger("CONSENSUS")


def finished_main(block: Block) -> None:
    if true_time(block):
        block.newly = False
        logger.info("Consensus proccess is complated, the block will be reset")
        current_blockshash_list = GetBlockshash()
        reset_block = block.reset_the_block(current_blockshash_list)
        if reset_block != False:
            block2 = reset_block[0]
            AppsTrigger(block2)
            transactions_main(block2)
            SaveBlockshash(current_blockshash_list)
            SaveBlockstoBlockchainDB(block2)
        PendingtoValidating(block)
        SaveBlock(block)
