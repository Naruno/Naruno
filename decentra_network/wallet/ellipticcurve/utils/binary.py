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

from base64 import b64decode, b64encode

from decentra_network.wallet.ellipticcurve.utils.compatibility import (
    safeBinaryFromHex, safeHexFromBinary, toString)


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


class BinaryAscii:
    @classmethod
    def hexFromBinary(cls, data):
        """
        Return the hexadecimal representation of the binary data. Every byte of data is converted into the
        corresponding 2-digit hex representation. The resulting string is therefore twice as long as the length of data.
        :param data: binary
        :return: hexadecimal string
        """
        return safeHexFromBinary(data)

    @classmethod
    def binaryFromHex(cls, data):
        """
        Return the binary data represented by the hexadecimal string hexstr. This function is the inverse of b2a_hex().
        hexstr must contain an even number of hexadecimal digits (which can be upper or lower case), otherwise a TypeError is raised.
        :param data: hexadecimal string
        :return: binary
        """
        return safeBinaryFromHex(data)

    @classmethod
    def numberFromString(cls, string):
        """
        Get a number representation of a string
        :param String to be converted in a number
        :return: Number in hex from string
        """
        return int(cls.hexFromBinary(string), 16)

    @classmethod
    def stringFromNumber(cls, number, length):
        """
        Get a string representation of a number
        :param number to be converted in a string
        :param length max number of character for the string
        :return: hexadecimal string
        """

        fmtStr = "%0" + str(2 * length) + "x"
        return toString(cls.binaryFromHex((fmtStr % number).encode()))
