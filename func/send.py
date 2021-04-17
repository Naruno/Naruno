#!/usr/bin/python3
# -*- coding: utf-8 -*-
from wallet.wallet import Ecdsa, PrivateKey

from node.myownp2pn import mynode


def send(my_public_key, my_private_key, to_user, data = None, amount = None):
    my_public_key = "".join([
            l.strip() for l in my_public_key.splitlines()
            if l and not l.startswith("-----")
        ])  

    from blockchain.block.block_main import get_block
    system = get_block()
    sequance_number = system.getSequanceNumber(user = my_public_key) + 1
    transaction_fee = 0.02

    system.createTrans(sequance_number = sequance_number, signature = Ecdsa.sign(str(sequance_number)+str(my_public_key)+str(to_user)+str(data)+str(amount)+str(transaction_fee), PrivateKey.fromPem(my_private_key)).toBase64(), fromUser = str(my_public_key), toUser = str(to_user), data = data, amount = amount, transaction_fee = transaction_fee, transaction_sender = None, my_tx = True)
