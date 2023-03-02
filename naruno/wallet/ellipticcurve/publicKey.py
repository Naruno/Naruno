#!/usr/bin/python3
# -*- coding: utf-8 -*-
from naruno.wallet.ellipticcurve.curve import getCurveByOid
from naruno.wallet.ellipticcurve.curve import secp256k1
from naruno.wallet.ellipticcurve.math import Math
from naruno.wallet.ellipticcurve.point import Point
from naruno.wallet.ellipticcurve.utils.binary import base64FromByteString
from naruno.wallet.ellipticcurve.utils.binary import byteStringFromBase64
from naruno.wallet.ellipticcurve.utils.binary import byteStringFromHex
from naruno.wallet.ellipticcurve.utils.binary import hexFromByteString
from naruno.wallet.ellipticcurve.utils.binary import intFromHex
from naruno.wallet.ellipticcurve.utils.der import DerFieldType
from naruno.wallet.ellipticcurve.utils.der import encodeConstructed
from naruno.wallet.ellipticcurve.utils.der import encodePrimitive
from naruno.wallet.ellipticcurve.utils.der import hexFromInt
from naruno.wallet.ellipticcurve.utils.der import parse
from naruno.wallet.ellipticcurve.utils.pem import createPem
from naruno.wallet.ellipticcurve.utils.pem import getPemContent


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
