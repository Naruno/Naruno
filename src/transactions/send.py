#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from hashlib import sha256

from accounts.get_sequance_number import GetSequanceNumber
from blockchain.block.get_block import GetBlock
from lib.settings_system import the_settings
from transactions.save_to_my_transaction import SavetoMyTransaction
from transactions.send_transaction_to_the_block import \
    SendTransactiontoTheBlock
from wallet.wallet import Ecdsa
from wallet.wallet import PrivateKey
from wallet.wallet import Wallet_Import


def send(password, to_user, amount, data=None):
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
        print("This is not float coin amount.")
        return False

    if isinstance(amount, int):
        amount = float(amount)

    if not isinstance(amount, float):
        print("This is not int or float coin amount.")
        return None

    if amount < 0:
        print("This is negative coin amount.")
        return None

    block = GetBlock()

    if not amount < block.minumum_transfer_amount:
        if (Wallet_Import(int(the_settings()["wallet"]),
                          2) == sha256(password.encode("utf-8")).hexdigest()):

            my_private_key = Wallet_Import(-1, 1, password)
            my_public_key = "".join([
                l.strip() for l in Wallet_Import(-1, 0).splitlines()
                if l and not l.startswith("-----")
            ])

            sequance_number = GetSequanceNumber(my_public_key, block) + 1

            # Get the current fee
            transaction_fee = block.transaction_fee

            tx_time = int(time.time())

            the_tx = SendTransactiontoTheBlock(
                block,
                sequance_number=sequance_number,
                signature=Ecdsa.sign(
                    str(sequance_number) + str(my_public_key) + str(to_user) +
                    str(data) + str(amount) + str(transaction_fee) +
                    str(tx_time),
                    PrivateKey.fromPem(my_private_key),
                ).toBase64(),
                fromUser=str(my_public_key),
                toUser=str(to_user),
                data=data,
                amount=amount,
                transaction_fee=transaction_fee,
                transaction_sender=None,
                transaction_time=tx_time,
            )

            SavetoMyTransaction(the_tx)

            del my_private_key
            del password

        else:
            print("Password is not correct")
