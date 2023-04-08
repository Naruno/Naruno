#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from naruno.blockchain.block.hash.accounts_hash import AccountsHash
from naruno.blockchain.block.hash.blocks_hash import BlocksHash
from naruno.blockchain.block.hash.tx_hash import TransactionsHash
from naruno.consensus.rounds.round_1.process.transactions.checks.duplicated import \
    Remove_Duplicates
from naruno.lib.log import get_logger
from naruno.lib.mix.merkle_root import MerkleTree

logger = get_logger("BLOCKCHAIN")


def CalculateHash(block, part_of_blocks_hash, the_blocks_hash, the_accounts):
    """
    Calculates and returns the hash of the block.
    """
    logger.info(f"Calculating the hash of the block#{block.sequence_number}")

    block = Remove_Duplicates(block)
    block.validating_list = sorted(block.validating_list,
                                   key=lambda x: x.fromUser)

    # Transaction Hash
    validating_list = [tx.dump_json() for tx in block.validating_list]
    logger.debug(f"block.validating_list: {validating_list}")
    tx_hash = TransactionsHash(block)
    logger.debug(f"tx_hash: {tx_hash}")

    # Blocks Hash
    blocks_hash = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)
    logger.debug(f"blocks_hash: {blocks_hash}")

    # Account
    accounts_hash = AccountsHash(block, the_accounts)
    logger.debug(f"accounts_hash: {accounts_hash}")

    # Other Elements
    main_list = [
        blocks_hash,
        accounts_hash,
        tx_hash,
        str(block.coin_amount),
        str(block.creator),
        str(block.genesis_time),
        str(block.block_time),
        str(block.previous_hash),
        str(block.sequence_number),
        str(block.hard_block_number),
        str(block.gap_block_number),
        str(block.transaction_fee),
        str(block.default_transaction_fee),
        str(block.default_optimum_transaction_number),
        str(block.default_increase_of_fee),
        str(block.transaction_delay_time),
        str(block.max_data_size),
        str(block.part_amount),
        str(block.max_tx_number),
        str(block.minumum_transfer_amount),
        str(block.round_1_time),
        str(block.round_2_time),
        # str(block.validated_time),
        str(block.just_one_tx),
        str(block.shares),
        str(block.fee_address),
    ]

    logger.debug(f"main_list: {main_list}")

    the_hash = MerkleTree(main_list).getRootHash()
    logger.debug(f"the_hash: {the_hash}")

    return the_hash
