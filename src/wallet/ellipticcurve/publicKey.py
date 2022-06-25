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

from wallet.ellipticcurve.math import Math
from wallet.ellipticcurve.point import Point
from wallet.ellipticcurve.curve import secp256k1, getCurveByOid
from wallet.ellipticcurve.utils.pem import getPemContent, createPem
from wallet.ellipticcurve.utils.der import hexFromInt, parse, DerFieldType, encodeConstructed, encodePrimitive
from wallet.ellipticcurve.utils.binary import hexFromByteString, byteStringFromHex, intFromHex, base64FromByteString, byteStringFromBase64


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
            return "0004" + string
        return string

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
        return createPem(content=base64FromByteString(der), template=_pemTemplate)

    @classmethod
    def fromPem(cls, string):
        publicKeyPem = getPemContent(pem=string, template=_pemTemplate)
        return cls.fromDer(byteStringFromBase64(publicKeyPem))

    @classmethod
    def fromDer(cls, string):
        hexadecimal = hexFromByteString(string)
        curveData, pointString = parse(hexadecimal)[0]
        publicKeyOid, curveOid = curveData
        if publicKeyOid != _ecdsaPublicKeyOid:
            raise Exception("The Public Key Object Identifier (OID) should be {ecdsaPublicKeyOid}, but {actualOid} was found instead".format(
                ecdsaPublicKeyOid=_ecdsaPublicKeyOid,
                actualOid=publicKeyOid,
            ))
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
        if not validatePoint:
            return publicKey
        if p.isAtInfinity():
            raise Exception("Public Key point is at infinity")
        if not curve.contains(p):
            raise Exception("Point ({x},{y}) is not valid for curve {name}".format(
                x=p.x, y=p.y, name=curve.name))
        if not Math.multiply(p=p, n=curve.N, N=curve.N, A=curve.A, P=curve.P).isAtInfinity():
            raise Exception(
                "Point ({x},{y}) * {name}.N is not at infinity".format(x=p.x, y=p.y, name=curve.name))
        return publicKey


_ecdsaPublicKeyOid = (1, 2, 840, 10045, 2, 1)


_pemTemplate = """{content}"""
