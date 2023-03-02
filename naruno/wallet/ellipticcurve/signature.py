#!/usr/bin/python3
# -*- coding: utf-8 -*-
from naruno.wallet.ellipticcurve.utils.binary import base64FromByteString
from naruno.wallet.ellipticcurve.utils.binary import byteStringFromBase64
from naruno.wallet.ellipticcurve.utils.binary import byteStringFromHex
from naruno.wallet.ellipticcurve.utils.binary import hexFromByteString
from naruno.wallet.ellipticcurve.utils.compatibility import *
from naruno.wallet.ellipticcurve.utils.der import DerFieldType
from naruno.wallet.ellipticcurve.utils.der import encodeConstructed
from naruno.wallet.ellipticcurve.utils.der import encodePrimitive
from naruno.wallet.ellipticcurve.utils.der import parse


class Signature:

    def __init__(self, r, s, recoveryId=None):
        self.r = r
        self.s = s
        self.recoveryId = recoveryId

    def toDer(self, withRecoveryId=False):
        hexadecimal = self._toString()
        encodedSequence = byteStringFromHex(hexadecimal)
        if not withRecoveryId:
            return encodedSequence

    def toBase64(self, withRecoveryId=False):
        return base64FromByteString(self.toDer(withRecoveryId))

    @classmethod
    def fromDer(cls, string, recoveryByte=False):
        recoveryId = None

        hexadecimal = hexFromByteString(string)
        return cls._fromString(string=hexadecimal, recoveryId=recoveryId)

    @classmethod
    def fromBase64(cls, string, recoveryByte=False):
        der = byteStringFromBase64(string)
        return cls.fromDer(der, recoveryByte)

    def _toString(self):
        return encodeConstructed(
            encodePrimitive(DerFieldType.integer, self.r),
            encodePrimitive(DerFieldType.integer, self.s),
        )

    @classmethod
    def _fromString(cls, string, recoveryId=None):
        r, s = parse(string)[0]
        return Signature(r=r, s=s, recoveryId=recoveryId)
