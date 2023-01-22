#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
from decentra_network.transactions.check.check_transaction import \
    CheckTransaction
from decentra_network.transactions.pending.save_pending import SavePending
from decentra_network.blockchain.block.block_main import Block
from decentra_network.transactions.pending.delete_pending import DeletePending

from decentra_network.transactions.pending.get_pending import GetPending

def Cleaner(block: Block, pending_list_txs: list):
    
    def clean(list_of_transactions: list) -> list:
        clean_list = []
        for transaction in list_of_transactions:
            for transaction_ in list_of_transactions:
                if not transaction == transaction_:
                    if transaction.fromUser == transaction_.fromUser:
                        if transaction.sequence_number < transaction_.sequence_number:
                                clean_list.append(transaction)
                        elif transaction.sequence_number == transaction_.sequence_number:
                            if transaction.transaction_time < transaction_.transaction_time:
                                clean_list.append(transaction_)
        return clean_list

    first_validating_list = copy.copy(block.validating_list)
    cleaned_validating_list = clean(block.validating_list)
    difference = list(set(first_validating_list) - set(cleaned_validating_list))
    for transaction in difference:
        SavePending(transaction)
    block.validating_list = cleaned_validating_list

    pending_list_txs = GetPending()
    first_pending_list_txs = copy.copy(pending_list_txs)
    cleaned_pending_list_txs = clean(pending_list_txs)
    difference = list(set(first_pending_list_txs) - set(cleaned_pending_list_txs))
    for transaction in difference:

        DeletePending(transaction)
    pending_list_txs = cleaned_pending_list_txs


    return (block.validating_list, pending_list_txs)