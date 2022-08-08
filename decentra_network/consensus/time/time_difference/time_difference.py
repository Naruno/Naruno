#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time

from decentra_network.accounts.get_accounts import GetAccounts
from decentra_network.accounts.save_accounts import SaveAccounts
from decentra_network.blockchain.block.blocks_hash import GetBlockshash
from decentra_network.blockchain.block.blocks_hash import GetBlockshash_part
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash
from decentra_network.blockchain.block.blocks_hash import SaveBlockshash_part
from decentra_network.blockchain.block.hash.calculate_hash import CalculateHash
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.lib.log import get_logger
from decentra_network.node.server.server import server
from decentra_network.node.unl import Unl
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.process_the_transaction import ProccesstheTransaction
from decentra_network.blockchain.block.block_main import Block

logger = get_logger("CONSENSUS_FIRST_ROUND")


def time_difference_round_1(block: Block) -> bool:

    time_difference = int(time.time()) - block.start_time
    logger.info(f"Time difference is {time_difference}")
    if time_difference > block.round_1_time:
        return True
    else:
        return False

