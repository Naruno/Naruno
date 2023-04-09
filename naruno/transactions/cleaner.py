#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy

from naruno.blockchain.block.block_main import Block
from naruno.transactions.check.check_transaction import \
    CheckTransaction
from naruno.transactions.check.datas.check_datas import Check_Datas
from naruno.transactions.pending.delete_pending import DeletePending
from naruno.transactions.pending.get_pending import GetPending
from naruno.transactions.pending.save_pending import SavePending


def Cleaner(block: Block, pending_list_txs: list,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
):
    system_txs = []

    for transaction in block.validating_list:
        if transaction.signature == "NARUNO":
            block.validating_list.remove(transaction)
            system_txs.append(transaction)
            

    for transaction in pending_list_txs:
        the_sequance_number = None
        if custom_sequence_number == -1:
            the_sequance_number = transaction.sequence_number -1
        if not Check_Datas(
            block, 
            transaction, 
            custom_current_time=custom_current_time,
            custom_balance=custom_balance,
            custom_sequence_number=the_sequance_number,          
            disable_already_in=True):
            DeletePending(transaction)
            pending_list_txs.remove(transaction)

    for transaction in block.validating_list:
            the_sequance_number = None
            if custom_sequence_number == -1:
                the_sequance_number = transaction.sequence_number -1
            if not Check_Datas(
                block, 
                transaction,
                custom_current_time=custom_current_time,
                custom_balance=custom_balance,
                custom_sequence_number=the_sequance_number,            
                disable_already_in=True):
                block.validating_list.remove(transaction)

    def clean(list_of_transactions: list) -> list:
        list_of_transactions = list(dict.fromkeys(list_of_transactions))

        list_of_transactions = sorted(list_of_transactions,
                                      key=lambda x: x.signature)

        clean_list = []
        for transaction in list_of_transactions:
            ok = False
            just = True
            for transaction_ in list_of_transactions:
                if not transaction.__dict__ == transaction_.__dict__:
                    if transaction.fromUser == transaction_.fromUser and block.just_one_tx:
                        just = False
                        if transaction.sequence_number < transaction_.sequence_number:
                            ok = True
                        
                        elif (transaction.sequence_number ==
                              transaction_.sequence_number):
                            if (transaction.transaction_time <
                                    transaction_.transaction_time):
                                ok = True
                            elif (transaction.transaction_time ==
                                    transaction_.transaction_time):
                                if (transaction.signature <
                                        transaction_.signature):
                                    ok = True
                                else:
                                    ok = False
                                    break
                            else:
                                ok = False
                                break
                        else:
                            ok = False
                            break

            if ok or just:
                clean_list.append(transaction)

        return clean_list

    first_validating_list = copy.copy(block.validating_list)
    cleaned_validating_list = clean(block.validating_list)
    difference = list(
        set(first_validating_list) - set(cleaned_validating_list))
    for transaction in difference:
        SavePending(transaction)
    block.validating_list = cleaned_validating_list

    pending_list_txs = GetPending()
    first_pending_list_txs = copy.copy(pending_list_txs)
    cleaned_pending_list_txs = clean(pending_list_txs)
    difference = list(
        set(first_pending_list_txs) - set(cleaned_pending_list_txs))
    for transaction in difference:

        DeletePending(transaction)
    pending_list_txs = cleaned_pending_list_txs


    for transaction in system_txs:
        block.validating_list.append(transaction)


    return (cleaned_validating_list, cleaned_pending_list_txs)
