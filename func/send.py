#!/usr/bin/python3
# -*- coding: utf-8 -*-
from wallet.wallet import Ecdsa, PrivateKey

from node.myownp2pn import MyOwnPeer2PeerNode


def send(my_public_key, my_private_key, to_user, data = None, amount = None):
    from ledger.ledger_main import get_ledger
    system = get_ledger()
    sequance_number = (system.getSequanceNumber(my_public_key))+1
    transaction_fee = 0.02
    system.createTrans(sequance_number = sequance_number, signature = Ecdsa.sign(str(sequance_number)+str(my_public_key)+str(to_user)+str(data)+str(amount)+str(transaction_fee), PrivateKey.fromPem(my_private_key)).toBase64(), fromUser = str(my_public_key), toUser = str(to_user), data = str(data), amount = amount, transaction_fee = transaction_fee)
