#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Decentra Network Developers
Copyright (c) 2018 Stark Bank S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from decentra_network.config import *
from decentra_network.lib.encryption import encrypt


from decentra_network.wallet.ellipticcurve.save_wallet_list import save_to_wallet_list
from decentra_network.wallet.ellipticcurve.get_saved_wallet import get_saved_wallet 
from decentra_network.wallet.ellipticcurve.privateKey import PrivateKey


def wallet_create(password, save=True):

    my_private_key = PrivateKey()
    my_public_key = my_private_key.publicKey()

    if save != True:
        return my_private_key
    encrypted_key = (
        encrypt(my_private_key.toPem(), password)
        if list(get_saved_wallet())
        else my_private_key.toPem()
    )

    del my_private_key
    save_to_wallet_list(my_public_key.toPem(), encrypted_key, password)
    return encrypted_key
