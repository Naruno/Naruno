#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from decentra_network.blockchain.block.change_transaction_fee import \
    ChangeTransactionFee
from decentra_network.lib.log import get_logger
from decentra_network.transactions.check.datas.check_datas import Check_Datas
from decentra_network.transactions.check.len.check_len import Check_Len
from decentra_network.transactions.check.sign.check_sign import Check_Sign
from decentra_network.transactions.check.type.check_type import Check_Type

logger = get_logger("TRANSACTIONS")


def CheckTransaction(
    block,
    transaction,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
    custom_PENDING_TRANSACTIONS_PATH=None,
):
    """
    This function checks the transaction.
    """

    logger.info(
        f"Checking the transaction started {block.sequance_number}:{transaction.signature}"
    )
    ChangeTransactionFee(
        block,
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)

    if Check_Type(transaction):
        logger.info("Transaction type is correct")
    else:
        return False

    if Check_Len(block, transaction):
        logger.info("Transaction len is correct")
    else:
        return False

    if Check_Datas(
            block,
            transaction,
            custom_current_time=custom_current_time,
            custom_balance=custom_balance,
            custom_sequence_number=custom_sequence_number,
            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
    ):
        logger.info("Transaction balance is correct")
    else:
        return False

    if Check_Sign(transaction):
        logger.info("Transaction sign is correct")
    else:
        return False

    logger.info(
        f"Checking the transaction finished {block.sequance_number}:{transaction.signature}"
    )
    return True
