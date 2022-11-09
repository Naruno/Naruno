#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from hashlib import sha256

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.accounts.get_sequance_number import GetSequanceNumber
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.lib.log import get_logger
from decentra_network.lib.settings_system import the_settings
from decentra_network.transactions.get_transaction import GetTransaction
from decentra_network.transactions.transaction import Transaction
from decentra_network.wallet.ellipticcurve.ecdsa import Ecdsa
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import

logger = get_logger("TRANSACTIONS")


def send(
    password,
    to_user,
    amount=None,
    data="",
    block=None,
    custom_current_time=None,
    custom_sequence_number=None,
    custom_balance=None,
    custom_account_list=None,
):
    """
    The main function for sending the transaction.

    Inputs:
        password: The password of the wallet.
        to_user: The address of the recipient.
        amount: The amount of the transaction.
        data: The data of the transaction.

    """
    block = block if block is not None else GetBlock()

    the_minumum_amount = 0
    if (GetBalance(
            block, to_user, account_list=custom_account_list,
            dont_convert=True) >= 0):
        pass
    else:
        the_minumum_amount = block.minumum_transfer_amount
    amount = amount if amount is not None else the_minumum_amount

    try:
        amount = float(amount)
    except ValueError:
        logger.exception("This is not float coin amount.")
        return False

    if amount < 0:
        logger.error("This is negative coin amount.")
        return False

    if (block.max_data_size / block.max_tx_number) < len(data):
        logger.error("The data is too long.")
        return False

    decimal_amount = len(str(block.transaction_fee).split(".")[1])
    if len(str(amount).split(".")[1]) > decimal_amount:
        logger.error(
            f"The amount of decimal places is more than {decimal_amount}.")
        return False

    if (wallet_import(int(the_settings()["wallet"]),
                      2) == sha256(password.encode("utf-8")).hexdigest()):

        my_private_key = wallet_import(-1, 1, password)
        my_public_key = "".join([
            l.strip() for l in wallet_import(-1, 0).splitlines()
            if l and not l.startswith("-----")
        ])

        sequance_number = GetSequanceNumber(my_public_key) + 1

        # Get the current fee
        transaction_fee = block.transaction_fee

        tx_time = int(time.time())
        the_transaction = Transaction(
            sequance_number,
            Ecdsa.sign(
                (str(sequance_number) + my_public_key + str(to_user) +
                 str(data)) + str(amount) + str(transaction_fee) +
                str(tx_time),
                PrivateKey.fromPem(my_private_key),
            ).toBase64(),
            my_public_key,
            to_user,
            data,
            amount,
            transaction_fee,
            tx_time,
        )

        if GetTransaction(
                block,
                the_transaction,
                custom_current_time=custom_current_time,
                custom_sequence_number=custom_sequence_number,
                custom_balance=custom_balance,
                custom_account_list=custom_account_list,
        ):

            del my_private_key
            del password

            return the_transaction
        else:
            logger.error("The transaction is not valid.")
            return False

    else:
        logger.error("Password is not correct")
        return False
