#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wallet.wallet import Ecdsa, PrivateKey

from accounts.get_sequance_number import GetSequanceNumber

from blockchain.block.get_block import GetBlock


class TransactionConfig:
    """transaction related settings"""
    transaction_fee = 0.02

    @classmethod
    def change_transaction_fee(cls, transaction_fee: float) -> None:
        cls.transaction_fee = transaction_fee


def send(my_public_key, my_private_key, to_user, data = None, amount = None):
    my_public_key = "".join([
            l.strip() for l in my_public_key.splitlines()
            if l and not l.startswith("-----")
        ])  

    system = GetBlock()
    sequance_number = GetSequanceNumber(my_public_key, system) + 1
    transaction_fee = TransactionConfig.transaction_fee

    system.createTrans(sequance_number = sequance_number, signature = Ecdsa.sign(str(sequance_number)+str(my_public_key)+str(to_user)+str(data)+str(amount)+str(transaction_fee), PrivateKey.fromPem(my_private_key)).toBase64(), fromUser = str(my_public_key), toUser = str(to_user), data = data, amount = amount, transaction_fee = transaction_fee, transaction_sender = None)
