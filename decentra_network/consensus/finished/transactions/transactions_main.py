#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.block_main import Block
from decentra_network.lib.log import get_logger
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.my_transactions.sended_transaction import \
    SendedTransaction
from decentra_network.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from decentra_network.wallet.ellipticcurve.wallet_import import \
    wallet_import_all

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
    my_address = wallet_import_all(3)
    my_public_key = wallet_import_all(0)
    custom_currently_list = GetMyTransaction()
    for tx in block.validating_list:
        if tx.toUser in my_address:
            new_my_transactions_list = SavetoMyTransaction(
                tx,
                validated=True,
                custom_currently_list=custom_currently_list)
        elif tx.fromUser in my_public_key:
            new_my_transactions_list = ValidateTransaction(
                tx, custom_currently_list=custom_currently_list)
            new_my_transactions_list = SendedTransaction(
                tx, custom_currently_list=custom_currently_list)
    return new_my_transactions_list
