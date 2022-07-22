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
from base64 import b64decode
from base64 import b64encode

from decentra_network.wallet.ellipticcurve.utils.compatibility import safeBinaryFromHex
from decentra_network.wallet.ellipticcurve.utils.compatibility import safeHexFromBinary
from decentra_network.wallet.ellipticcurve.utils.compatibility import toString


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
