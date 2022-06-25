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
from datetime import datetime

from wallet.ellipticcurve.utils.binary import bitsFromHex
from wallet.ellipticcurve.utils.binary import byteStringFromHex
from wallet.ellipticcurve.utils.binary import hexFromInt
from wallet.ellipticcurve.utils.binary import intFromHex
from wallet.ellipticcurve.utils.oid import oidFromHex
from wallet.ellipticcurve.utils.oid import oidToHex


class DerFieldType:

    integer = "integer"
    bitString = "bitString"
    octetString = "octetString"
    null = "null"
    object = "object"
    printableString = "printableString"
    utcTime = "utcTime"
    sequence = "sequence"
    set = "set"
    oidContainer = "oidContainer"
    publicKeyPointContainer = "publicKeyPointContainer"


_hexTagToType = {
    "02": DerFieldType.integer,
    "03": DerFieldType.bitString,
    "04": DerFieldType.octetString,
    "05": DerFieldType.null,
    "06": DerFieldType.object,
    "13": DerFieldType.printableString,
    "17": DerFieldType.utcTime,
    "30": DerFieldType.sequence,
    "31": DerFieldType.set,
    "a0": DerFieldType.oidContainer,
    "a1": DerFieldType.publicKeyPointContainer,
}
_typeToHexTag = {v: k for k, v in _hexTagToType.items()}


def encodeConstructed(*encodedValues):
    return encodePrimitive(DerFieldType.sequence, "".join(encodedValues))


def encodePrimitive(tagType, value):
    if tagType == DerFieldType.integer:
        value = _encodeInteger(value)
    if tagType == DerFieldType.object:
        value = oidToHex(value)
    return "{tag}{size}{value}".format(
        tag=_typeToHexTag[tagType], size=_generateLengthBytes(value), value=value
    )


def parse(hexadecimal):
    if not hexadecimal:
        return []
    typeByte, hexadecimal = hexadecimal[:2], hexadecimal[2:]
    length, lengthBytes = _readLengthBytes(hexadecimal)
    content, hexadecimal = (
        hexadecimal[lengthBytes : lengthBytes + length],
        hexadecimal[lengthBytes + length :],
    )
    if len(content) < length:
        raise Exception("missing bytes in DER parse")

    tagData = _getTagData(typeByte)
    if tagData["isConstructed"]:
        content = parse(content)

    valueParser = {
        DerFieldType.null: _parseNull,
        DerFieldType.object: _parseOid,
        DerFieldType.utcTime: _parseTime,
        DerFieldType.integer: _parseInteger,
        DerFieldType.printableString: _parseString,
    }.get(tagData["type"], _parseAny)
    return [valueParser(content)] + parse(hexadecimal)


def _parseAny(hexadecimal):
    return hexadecimal


def _parseOid(hexadecimal):
    return tuple(oidFromHex(hexadecimal))


def _parseTime(hexadecimal):
    string = _parseString(hexadecimal)
    return datetime.strptime(string, "%y%m%d%H%M%SZ")


def _parseString(hexadecimal):
    return byteStringFromHex(hexadecimal).decode()


def _parseNull(_content):
    return None


def _parseInteger(hexadecimal):
    integer = intFromHex(hexadecimal)
    bits = bitsFromHex(hexadecimal[0])
    if bits[0] == "0":  # negative numbers are encoded using two's complement
        return integer
    bitCount = 4 * len(hexadecimal)
    return integer - (2**bitCount)


def _encodeInteger(number):
    hexadecimal = hexFromInt(abs(number))
    if number < 0:
        bitCount = 4 * len(hexadecimal)
        twosComplement = (2**bitCount) + number
        return hexFromInt(twosComplement)
    bits = bitsFromHex(hexadecimal[0])
    if (
        bits[0] == "1"
    ):  # if first bit was left as 1, number would be parsed as a negative integer with two's complement
        hexadecimal = "00" + hexadecimal
    return hexadecimal


def _readLengthBytes(hexadecimal):
    lengthBytes = 2
    lengthIndicator = intFromHex(hexadecimal[0:lengthBytes])
    # checks if first bit of byte is 1 (a.k.a. short-form)
    isShortForm = lengthIndicator < 128
    if isShortForm:
        length = lengthIndicator * 2
        return length, lengthBytes

    # nullifies first bit of byte (only used as long-form flag)
    lengthLength = lengthIndicator - 128
    if lengthLength == 0:
        raise Exception("indefinite length encoding located in DER")
    lengthBytes += 2 * lengthLength
    length = intFromHex(hexadecimal[2:lengthBytes]) * 2
    return length, lengthBytes


def _generateLengthBytes(hexadecimal):
    size = len(hexadecimal) // 2
    length = hexFromInt(size)
    # checks if first bit of byte should be 0 (a.k.a. short-form flag)
    if size < 128:
        return length.zfill(2)
    # +128 sets the first bit of the byte as 1 (a.k.a. long-form flag)
    lengthLength = 128 + len(length) // 2
    return hexFromInt(lengthLength) + length


def _getTagData(tag):
    bits = bitsFromHex(tag)
    bit8, bit7, bit6 = bits[:3]

    tagClass = {
        "0": {
            "0": "universal",
            "1": "application",
        },
        "1": {
            "0": "context-specific",
            "1": "private",
        },
    }[bit8][bit7]
    isConstructed = bit6 == "1"

    return {
        "class": tagClass,
        "isConstructed": isConstructed,
        "type": _hexTagToType.get(tag),
    }
