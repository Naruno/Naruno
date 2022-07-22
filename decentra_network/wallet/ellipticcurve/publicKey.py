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
from decentra_network.wallet.ellipticcurve.point import Point
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
from decentra_network.wallet.ellipticcurve.utils.pem import createPem
from decentra_network.wallet.ellipticcurve.utils.pem import getPemContent


class PublicKey:

    def __init__(self, point, curve):
        self.point = point
        self.curve = curve

    def toString(self, encoded=False):
        baseLength = 2 * self.curve.length()
        xHex = hexFromInt(self.point.x).zfill(baseLength)
        yHex = hexFromInt(self.point.y).zfill(baseLength)
        string = xHex + yHex
        if encoded:
            return f"0004{string}"

    def toDer(self):
        hexadecimal = encodeConstructed(
            encodeConstructed(
                encodePrimitive(DerFieldType.object, _ecdsaPublicKeyOid),
                encodePrimitive(DerFieldType.object, self.curve.oid),
            ),
            encodePrimitive(DerFieldType.bitString,
                            self.toString(encoded=True)),
        )
        return byteStringFromHex(hexadecimal)

    def toPem(self):
        der = self.toDer()
        return createPem(content=base64FromByteString(der),
                         template=_pemTemplate)

    @classmethod
    def fromPem(cls, string):
        publicKeyPem = getPemContent(pem=string, template=_pemTemplate)
        return cls.fromDer(byteStringFromBase64(publicKeyPem))

    @classmethod
    def fromDer(cls, string):
        hexadecimal = hexFromByteString(string)
        curveData, pointString = parse(hexadecimal)[0]
        publicKeyOid, curveOid = curveData

        curve = getCurveByOid(curveOid)
        return cls.fromString(string=pointString, curve=curve)

    @classmethod
    def fromString(cls, string, curve=secp256k1, validatePoint=True):
        baseLength = 2 * curve.length()
        if len(string) > 2 * baseLength and string[:4] == "0004":
            string = string[4:]

        xs = string[:baseLength]
        ys = string[baseLength:]

        p = Point(
            x=intFromHex(xs),
            y=intFromHex(ys),
        )
        publicKey = PublicKey(point=p, curve=curve)

        return publicKey


_ecdsaPublicKeyOid = (1, 2, 840, 10045, 2, 1)

_pemTemplate = """{content}"""
