#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from blockchain.block.hash.tx_hash import TransactionsHash
from blockchain.block.hash.blocks_hash import BlocksHash
from blockchain.block.hash.accounts_hash import AccountsHash
from lib.merkle_root import MerkleTree


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
    main_list = []
    main_list.append(block.previous_hash)
    main_list.append(str(block.sequance_number))
    main_list.append(blocks_hash)
    main_list.append(accounts_hash)
    main_list.append(tx_hash)
    main_list.append(str(block.default_transaction_fee))
    main_list.append(str(block.default_increase_of_fee))
    main_list.append(str(block.default_optimum_transaction_number))

    the_hash = MerkleTree(main_list).getRootHash()

    # Setting The Hashes
    block.hash = the_hash

    return the_hash
