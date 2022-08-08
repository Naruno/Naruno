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
from decentra_network.consensus.rounds.round_1.round_1_main import consensus_round_1
from decentra_network.consensus.rounds.round_2.round_2_main import consensus_round_2
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

def ongoing_main(block):
    PendingtoValidating(block)
    if block.round_1_starting_time is None:
        block.round_1_starting_time = int(time.time())
        SaveBlock(block)
    if not block.round_1:
        logger.info("First round is starting")
        consensus_round_1(block)
        logger.info("First round is done")
    elif not block.round_2:
        logger.info("Second round is starting")
        consensus_round_2(block)
        logger.info("Second round is done")