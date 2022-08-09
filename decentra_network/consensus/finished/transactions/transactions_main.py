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

from decentra_network.consensus.time.true_time.true_time import true_time

from decentra_network.blockchain.block.block_main import Block

from decentra_network.transactions.my_transactions.get_my_transaction import (
    GetMyTransaction,
)

logger = get_logger("CONSENSUS")


def transactions_main(block: Block) -> list:
    """
    This function is responsible for the transactions of the block.
    Parameters:
        block: The block that is going to be validated.
    Returns:
        list: The list of the transactions that are going to be validated.
    """
    new_my_transactions_list = None
    my_address = wallet_import(-1, 3)
    my_public_key = wallet_import(-1, 0)
    custom_currently_list = GetMyTransaction()
    for tx in block.validating_list:
        if tx.toUser == my_address:
            new_my_transactions_list = SavetoMyTransaction(
                tx, validated=True, custom_currently_list=custom_currently_list)
        elif tx.fromUser == my_public_key:
            new_my_transactions_list = ValidateTransaction(
                tx, custom_currently_list=custom_currently_list)
    return new_my_transactions_list
