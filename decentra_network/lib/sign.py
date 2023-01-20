#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from decentra_network.wallet.ellipticcurve.ecdsa import Ecdsa
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey

def sign(data: str, password: str) -> str:
    
    my_private_key = wallet_import(-1, 1, password)
    signature = Ecdsa.sign(
                data,
                PrivateKey.fromPem(my_private_key),
            ).toBase64() 
   
   
    sign_json = {
        "data": data,
        "signature": signature,
        "publickey": wallet_import(-1, 0)
    }


    return signature

print(sign("Ali Eren", "123"))



