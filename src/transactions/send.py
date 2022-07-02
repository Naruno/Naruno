#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from hashlib import sha256

from accounts.get_sequance_number import GetSequanceNumber
from lib.log import get_logger
from lib.settings_system import the_settings
from node.node import Node
from transactions.check.check_transaction import CheckTransaction
from transactions.get_transaction import GetTransaction
from transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from transactions.transaction import Transaction
from wallet.ellipticcurve.ecdsa import Ecdsa
from wallet.ellipticcurve.privateKey import PrivateKey
from wallet.wallet_import import wallet_import

logger = get_logger("TRANSACTIONS")


def send(block, password, to_user, amount, data=""):
    """
    The main function for sending the transaction.

    Inputs:
        password: The password of the wallet.
        to_user: The address of the recipient.
        amount: The amount of the transaction.
        data: The data of the transaction.

    """

    try:
        amount = float(amount)
    except ValueError:
        logger.exception("This is not float coin amount.")
        return False

    if amount < 0:
        logger.error("This is negative coin amount.")
        return False

    if not (block.max_data_size / block.max_tx_number) >= len(data):
        logger.error("The data is too long.")
        return False

    decimal_amount = len(str(block.transaction_fee).split(".")[1])
    if len(str(amount).split(".")[1]) > decimal_amount:
        logger.error(
            f"The amount of decimal places is more than {decimal_amount}.")
        return False

    if not amount < block.minumum_transfer_amount:
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
                    str(sequance_number) + str(my_public_key) + str(to_user) +
                    str(data) + str(amount) + str(transaction_fee) +
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
            if GetTransaction(block, the_transaction):
                SavetoMyTransaction(the_transaction)

                del my_private_key
                del password

                return True
            else:
                logger.error("The transaction is not valid.")
                return False

        else:
            return False
            logger.error("Password is not correct")
    else:
        return False
        logger.error(
            f"The amount is too low. minumum:{block.minumum_transfer_amount}")
