#!/usr/bin/python3
# -*- coding: utf-8 -*-
from base64 import b64decode
from base64 import b64encode

from naruno.wallet.ellipticcurve.utils.compatibility import safeBinaryFromHex
from naruno.wallet.ellipticcurve.utils.compatibility import safeHexFromBinary
from naruno.wallet.ellipticcurve.utils.compatibility import toString


def hexFromInt(number):
    hexadecimal = "{0:x}".format(number)
    if len(hexadecimal) % 2 == 1:
        hexadecimal = f"0{hexadecimal}"
    return hexadecimal


def intFromHex(hexadecimal):
    return int(hexadecimal, 16)


def hexFromByteString(byteString):
    return safeHexFromBinary(byteString)


def byteStringFromHex(hexadecimal):
    return safeBinaryFromHex(hexadecimal)


def numberFromByteString(byteString):
    return intFromHex(hexFromByteString(byteString))


def base64FromByteString(byteString):
    return toString(b64encode(byteString))


def byteStringFromBase64(base64String):
    return b64decode(base64String)


def bitsFromHex(hexadecimal):
    return format(intFromHex(hexadecimal), "b").zfill(4 * len(hexadecimal))
