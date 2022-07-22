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
from decentra_network.wallet.ellipticcurve.utils.binary import base64FromByteString
from decentra_network.wallet.ellipticcurve.utils.binary import byteStringFromBase64
from decentra_network.wallet.ellipticcurve.utils.binary import byteStringFromHex
from decentra_network.wallet.ellipticcurve.utils.binary import hexFromByteString
from decentra_network.wallet.ellipticcurve.utils.compatibility import *
from decentra_network.wallet.ellipticcurve.utils.der import DerFieldType
from decentra_network.wallet.ellipticcurve.utils.der import encodeConstructed
from decentra_network.wallet.ellipticcurve.utils.der import encodePrimitive
from decentra_network.wallet.ellipticcurve.utils.der import parse


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
