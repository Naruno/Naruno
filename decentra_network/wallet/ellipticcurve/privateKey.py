#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
