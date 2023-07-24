#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import threading

from naruno.accounts.commanders.get_comnder import GetCommander
from naruno.blockchain.block.block_main import Block
from naruno.lib.log import get_logger
from naruno.lib.settings_system import the_settings
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.my_transactions.sended_transaction import \
    SendedTransaction
from naruno.transactions.my_transactions.validate_transaction import \
    ValidateTransaction
from naruno.wallet.wallet_import import wallet_import_all

logger = get_logger("CONSENSUS")



def transaction_main_


def transactions_main(block: Block) -> list:
    """
    This function is responsible for the transactions of the block.
    Parameters:
        block: The block that is going to be validated.
    Returns:
        list: The list of the transactions that are going to be validated.
    """
    new_my_transactions_list = False
    my_address = wallet_import_all(3)
    my_public_key = wallet_import_all(0)
    custom_currently_list = GetMyTransaction()
    commanders = GetCommander()
    for tx in block.validating_list:
        if tx.toUser in my_address:
            new_my_transactions_list = True
            threading.Thread(target=SavetoMyTransaction, args=(
                tx,
                ), kwargs={"validated":True,"custom_currently_list"=custom_currently_list}).start()
        elif tx.fromUser in my_public_key:
            new_my_transactions_list = True
            threading.Thread(target=ValidateTransaction, args(
                tx), kwargs={"custom_currently_list"=custom_currently_list}).start()
            threading.Thread(target=SendedTransaction, args(
                tx), kwargs={"custom_currently_list"=custom_currently_list}).start()
        elif tx.fromUser in commanders:
            new_my_transactions_list = True
            threading.Thread(target=SavetoMyTransaction, args(
                tx,
                ), kwargs={"validated":True,"custom_currently_list"=custom_currently_list}).start()
        else:
            if the_settings()["publisher_mode"]:
                threading.Thread(target=SavetoMyTransaction, args(
                    tx,
                    ), kwargs={"validated":True,"custom_currently_list"=custom_currently_list}).start()
    return True
