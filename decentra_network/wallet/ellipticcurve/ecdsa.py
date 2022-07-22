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
from hashlib import sha256

from decentra_network.wallet.ellipticcurve.math import Math
from decentra_network.wallet.ellipticcurve.signature import Signature
from decentra_network.wallet.ellipticcurve.utils.binary import \
    numberFromByteString
from decentra_network.wallet.ellipticcurve.utils.compatibility import *
from decentra_network.wallet.ellipticcurve.utils.integer import RandomInteger


class Ecdsa:

    @classmethod
    def sign(cls, message, privateKey, hashfunc=sha256):
        byteMessage = hashfunc(toBytes(message)).digest()
        numberMessage = numberFromByteString(byteMessage)
        curve = privateKey.curve

        r, s, randSignPoint = 0, 0, None
        while r == 0 or s == 0:
            randNum = RandomInteger.between(1, curve.N - 1)
            randSignPoint = Math.multiply(curve.G,
                                          n=randNum,
                                          A=curve.A,
                                          P=curve.P,
                                          N=curve.N)
            r = randSignPoint.x % curve.N
            s = ((numberMessage + r * privateKey.secret) *
                 (Math.inv(randNum, curve.N))) % curve.N
        recoveryId = randSignPoint.y & 1

        return Signature(r=r, s=s, recoveryId=recoveryId)

    @classmethod
    def verify(cls, message, signature, publicKey, hashfunc=sha256):
        byteMessage = hashfunc(toBytes(message)).digest()
        numberMessage = numberFromByteString(byteMessage)
        curve = publicKey.curve
        r = signature.r
        s = signature.s

        inv = Math.inv(s, curve.N)
        u1 = Math.multiply(curve.G,
                           n=(numberMessage * inv) % curve.N,
                           N=curve.N,
                           A=curve.A,
                           P=curve.P)
        u2 = Math.multiply(publicKey.point,
                           n=(r * inv) % curve.N,
                           N=curve.N,
                           A=curve.A,
                           P=curve.P)
        v = Math.add(u1, u2, A=curve.A, P=curve.P)

        return v.x % curve.N == r
