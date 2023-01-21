#!/usr/bin/python3
# -*- coding: utf-8 -*-
from binascii import hexlify
from binascii import unhexlify
from sys import version_info as pyVersion

if pyVersion.major == 3:
    # py3 constants and conversion functions

    stringTypes = (str, )
    intTypes = (int, float)

    def toString(string, encoding="utf-8"):
        return string.decode(encoding)

    def toBytes(string, encoding="utf-8"):
        return string.encode(encoding)

    def safeBinaryFromHex(hexadecimal):

        return unhexlify(hexadecimal)

    def safeHexFromBinary(byteString):
        return toString(hexlify(byteString))
