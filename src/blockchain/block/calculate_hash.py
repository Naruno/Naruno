#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from lib.mixlib import dprint
from lib.merkle_root import MerkleTree

from blockchain.block.blocks_hash import GetBlockshash, GetBlockshash_part, SaveBlockshash_part

from accounts.account import GetAccounts, GetAccounts_part
from accounts.save_accounts import save_accounts
from accounts.save_accounts_part import save_accounts_part


def CalculateHash(block):
    """
    Calculates and returns the hash of the block.
    """

    # Transaction
    tx_list = []
    dprint(len(block.validating_list))
    for element in block.validating_list[:]:
        dprint(element)
        tx_list.append(element.signature)
    if len(tx_list) != 0:
        tx_hash = MerkleTree(tx_list).getRootHash()
    else:
        tx_hash = "0"


    part_amount = 100000

    # Blocks Hash
    blocks_hash_list = []

    part_of_blocks_hash = GetBlockshash_part()
    the_blocks_hash = GetBlockshash()


    if not len(the_blocks_hash) - (len(part_of_blocks_hash) * part_amount) == part_amount:
        for will_added_blocks_hash in the_blocks_hash[(len(part_of_blocks_hash) * part_amount):]:
            blocks_hash_list.append(will_added_blocks_hash)
    else:
        part_of_blocks_hash.append(MerkleTree(the_blocks_hash[(len(part_of_blocks_hash) * part_amount):]).getRootHash())
        SaveBlockshash_part(part_of_blocks_hash)

    
    for part_of_blocks_hash_element in part_of_blocks_hash:
        blocks_hash_list.append(part_of_blocks_hash_element)
    

    blockshash_hash = MerkleTree(blocks_hash_list).getRootHash()


    # Account
    account_list = []

    part_of_account = GetAccounts_part()
    the_accounts = GetAccounts()

    if not len(the_accounts) - (len(part_of_account) * part_amount) >= part_amount:
        for will_added_accounts in the_accounts[(len(part_of_account) * part_amount):]:
            account_list.append(str(will_added_accounts.dump_json()))
    else:
        part_of_account.append(MerkleTree(the_accounts[(len(part_of_account) * part_amount):]).getRootHash())
        save_accounts(part_of_account)

    
    for part_of_account_element in part_of_account:
        account_list.append(part_of_account_element)

    for edited_account in block.edited_accounts:
        account_list.append(str(edited_account.dump_json()))

    block.edited_accounts.clear()
    
    ac_hash = MerkleTree(account_list).getRootHash()


    # Other elements
    main_list = []
    main_list.append(block.previous_hash)
    main_list.append(str(block.sequance_number))
    main_list.append(blockshash_hash)
    main_list.append(ac_hash)
    main_list.append(tx_hash)
    main_list.append(str(block.default_transaction_fee))
    main_list.append(str(block.default_increase_of_fee))
    main_list.append(str(block.default_optimum_transaction_number))

    # Calculating and returning
    return MerkleTree(main_list).getRootHash()
