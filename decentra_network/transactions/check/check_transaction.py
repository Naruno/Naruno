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
    custom_account_list=None,
):
    """
    This function checks the transaction.
    """

    logger.info(f"{transaction.signature}: Checking the transaction started")
    logger.debug(transaction.dump_json())
    ChangeTransactionFee(
        block,
        custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH)

    if Check_Type(transaction):
        pass
    else:
        logger.debug("The transaction type is not valid")
        return False

    if Check_Len(block, transaction):
        pass
    else:
        logger.debug("Transaction len is not correct")
        return False

    if Check_Datas(
            block,
            transaction,
            custom_current_time=custom_current_time,
            custom_balance=custom_balance,
            custom_sequence_number=custom_sequence_number,
            custom_PENDING_TRANSACTIONS_PATH=custom_PENDING_TRANSACTIONS_PATH,
            custom_account_list=custom_account_list,
    ):
        pass
    else:
        logger.debug("Transaction datas are not correct")
        return False

    if Check_Sign(transaction):
        pass
    else:
        logger.debug("Transaction sign is not correct")
        return False

    logger.info(
        f"{transaction.signature}: Checking the transaction finished as valid")
    return True
