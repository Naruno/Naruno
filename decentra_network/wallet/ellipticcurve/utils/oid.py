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

from decentra_network.wallet.ellipticcurve.utils.binary import intFromHex, hexFromInt


def oidFromHex(hexadecimal):
    firstByte, remainingBytes = hexadecimal[:2], hexadecimal[2:]
    firstByteInt = intFromHex(firstByte)
    oid = [firstByteInt // 40, firstByteInt % 40]
    oidInt = 0
    while len(remainingBytes) > 0:
        byte, remainingBytes = remainingBytes[:2], remainingBytes[2:]
        byteInt = intFromHex(byte)
        if byteInt >= 128:
            oidInt = (128 * oidInt) + (byteInt - 128)
            continue
        oidInt = (128 * oidInt) + byteInt
        oid.append(oidInt)
        oidInt = 0
    return oid


def oidToHex(oid):
    hexadecimal = hexFromInt(40 * oid[0] + oid[1])
    for number in oid[2:]:
        hexadecimal += _oidNumberToHex(number)
    return hexadecimal


def _oidNumberToHex(number):
    hexadecimal = ""
    endDelta = 0
    while number > 0:
        hexadecimal = hexFromInt((number % 128) + endDelta) + hexadecimal
        number //= 128
        endDelta = 128
    return hexadecimal or "00"
