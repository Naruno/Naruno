#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.apps.apps_trigger import AppsTrigger
from decentra_network.blockchain.block.blocks_hash import (GetBlockshash,
                                                           SaveBlockshash)
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.blockchain.block.save_block_to_blockchain_db import \
    SaveBlockstoBlockchainDB
from decentra_network.consensus.finished.finished_main import finished_main
from decentra_network.consensus.ongoing.ongoing_main import ongoing_main
from decentra_network.consensus.rounds.round_1.round_1_main import \
    consensus_round_1
from decentra_network.consensus.rounds.round_2.round_2_main import \
    consensus_round_2
from decentra_network.lib.log import get_logger
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.transactions.pending_to_validating import \
    PendingtoValidating
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
        finished_main(block)
    else:
        ongoing_main(block)

    logger.info("Consensus process is done")
