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
from decentra_network.wallet.ellipticcurve.curve import getCurveByOid
from decentra_network.wallet.ellipticcurve.curve import secp256k1
from decentra_network.wallet.ellipticcurve.math import Math
from decentra_network.wallet.ellipticcurve.publicKey import PublicKey
from decentra_network.wallet.ellipticcurve.utils.binary import base64FromByteString
from decentra_network.wallet.ellipticcurve.utils.binary import byteStringFromBase64
from decentra_network.wallet.ellipticcurve.utils.binary import byteStringFromHex
from decentra_network.wallet.ellipticcurve.utils.binary import hexFromByteString
from decentra_network.wallet.ellipticcurve.utils.binary import intFromHex
from decentra_network.wallet.ellipticcurve.utils.der import DerFieldType
from decentra_network.wallet.ellipticcurve.utils.der import encodeConstructed
from decentra_network.wallet.ellipticcurve.utils.der import encodePrimitive
from decentra_network.wallet.ellipticcurve.utils.der import hexFromInt
from decentra_network.wallet.ellipticcurve.utils.der import parse
from decentra_network.wallet.ellipticcurve.utils.integer import RandomInteger
from decentra_network.wallet.ellipticcurve.utils.pem import createPem
from decentra_network.wallet.ellipticcurve.utils.pem import getPemContent


class PrivateKey:

    def __init__(self, curve=secp256k1, secret=None):
        self.curve = curve
        self.secret = secret or RandomInteger.between(1, curve.N - 1)

    def publicKey(self):
        curve = self.curve
        publicPoint = Math.multiply(
            p=curve.G,
            n=self.secret,
            N=curve.N,
            A=curve.A,
            P=curve.P,
        )
        return PublicKey(point=publicPoint, curve=curve)

    def toDer(self):
        publicKeyString = self.publicKey().toString(encoded=True)
        hexadecimal = encodeConstructed(
            encodePrimitive(DerFieldType.integer, 1),
            encodePrimitive(DerFieldType.octetString, hexFromInt(self.secret)),
            encodePrimitive(
                DerFieldType.oidContainer,
                encodePrimitive(DerFieldType.object, self.curve.oid),
            ),
            encodePrimitive(
                DerFieldType.publicKeyPointContainer,
                encodePrimitive(DerFieldType.bitString, publicKeyString),
            ),
        )
        return byteStringFromHex(hexadecimal)

    def toPem(self):
        der = self.toDer()
        return createPem(content=base64FromByteString(der),
                         template=_pemTemplate)

    @classmethod
    def fromPem(cls, string):
        privateKeyPem = getPemContent(pem=string, template=_pemTemplate)
        return cls.fromDer(byteStringFromBase64(privateKeyPem))

    @classmethod
    def fromDer(cls, string):
        hexadecimal = hexFromByteString(string)
        privateKeyFlag, secretHex, curveData, publicKeyString = parse(
            hexadecimal)[0]

        curve = getCurveByOid(curveData[0])
        privateKey = cls.fromString(string=secretHex, curve=curve)

        return privateKey

    @classmethod
    def fromString(cls, string, curve=secp256k1):
        return PrivateKey(secret=intFromHex(string), curve=curve)


_pemTemplate = """{content}"""
