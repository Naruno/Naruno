#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.hash.accounts_hash import AccountsHash
from decentra_network.blockchain.block.hash.blocks_hash import BlocksHash
from decentra_network.blockchain.block.hash.tx_hash import TransactionsHash
from decentra_network.lib.mix.merkle_root import MerkleTree


def CalculateHash(block, part_of_blocks_hash, the_blocks_hash, the_accounts):
    """
    Calculates and returns the hash of the block.
    """

    # Transaction Hash
    tx_hash = TransactionsHash(block)

    # Blocks Hash
    blocks_hash = BlocksHash(block, part_of_blocks_hash, the_blocks_hash)

    # Account
    accounts_hash = AccountsHash(block, the_accounts)

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
        str(block.validated_time),
        str(block.shares),
        str(block.fee_address),
    ]

    the_hash = MerkleTree(main_list).getRootHash()

    return the_hash
