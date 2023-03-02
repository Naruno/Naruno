#!/usr/bin/python3
# -*- coding: utf-8 -*-
from hashlib import sha256

from naruno.wallet.ellipticcurve.math import Math
from naruno.wallet.ellipticcurve.signature import Signature
from naruno.wallet.ellipticcurve.utils.binary import \
    numberFromByteString
from naruno.wallet.ellipticcurve.utils.compatibility import *
from naruno.wallet.ellipticcurve.utils.integer import RandomInteger


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
