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

from hashlib import sha256


from sys import version_info as pyVersion
from binascii import hexlify, unhexlify




if pyVersion.major == 3:
    # py3 constants and conversion functions

    xrange = range
    stringTypes = (str,) # lgtm [py/multiple-definition]
    intTypes = (int, float)

    def toString(string):
        return string.decode("latin-1")

    def toBytes(string):
        return string.encode("latin-1")

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)
else:
    # py2 constants and conversion functions

    stringTypes = (str, unicode) # lgtm [py/multiple-definition]
    intTypes = (int, float, long)

    def toString(string):
        return string

    def toBytes(string):
        return string

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)


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

from random import SystemRandom


class RandomInteger:

    @classmethod
    def between(cls, min, max):
        """
        Return integer x in the range: min <= x <= max
        :param min: minimum value of the integer
        :param max: maximum value of the integer
        :return:
        """

        return SystemRandom().randrange(min, max + 1)

from sys import version_info as pyVersion
from binascii import hexlify, unhexlify


if pyVersion.major == 3:
    # py3 constants and conversion functions

    xrange = range
    stringTypes = (str,)
    intTypes = (int, float)

    def toString(string):
        return string.decode("latin-1")

    def toBytes(string):
        return string.encode("latin-1")

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)
else:
    # py2 constants and conversion functions

    stringTypes = (str, unicode)
    intTypes = (int, float, long)

    def toString(string):
        return string

    def toBytes(string):
        return string

    def safeBinaryFromHex(hexString):
        return unhexlify(hexString)

    def safeHexFromBinary(byteString):
        return hexlify(byteString)


class Ecdsa:

    @classmethod
    def sign(cls, message, privateKey, hashfunc=sha256):
        hashMessage = hashfunc(toBytes(message)).digest()
        numberMessage = BinaryAscii.numberFromString(hashMessage)
        curve = privateKey.curve

        r, s, randSignPoint = 0, 0, None
        while r == 0 or s == 0:
            randNum = RandomInteger.between(1, curve.N - 1)
            randSignPoint = Math.multiply(curve.G, n=randNum, A=curve.A, P=curve.P, N=curve.N)
            r = randSignPoint.x % curve.N
            s = ((numberMessage + r * privateKey.secret) * (Math.inv(randNum, curve.N))) % curve.N
        recoveryId = randSignPoint.y & 1
        if randSignPoint.y > curve.N:
            recoveryId += 2

        return Signature(r=r, s=s, recoveryId=recoveryId)

    @classmethod
    def verify(cls, message, signature, publicKey, hashfunc=sha256):
        hashMessage = hashfunc(toBytes(message)).digest()
        numberMessage = BinaryAscii.numberFromString(hashMessage)
        curve = publicKey.curve
        sigR = signature.r
        sigS = signature.s
        inv = Math.inv(sigS, curve.N)
        u1 = Math.multiply(curve.G, n=(numberMessage * inv) % curve.N, A=curve.A, P=curve.P, N=curve.N)
        u2 = Math.multiply(publicKey.point, n=(sigR * inv) % curve.N, A=curve.A, P=curve.P, N=curve.N)


        #add = Math.add(u1, u2, P=curve.P, A=curve.A) # test and delete
        #return sigR == add.x # test and delete
        
        add = Math.add(u1, u2, P=curve.P, A=curve.A)
        modX = add.x % curve.N
        return sigR == modX



from base64 import b64encode, b64decode


class Base64:

    @classmethod
    def decode(cls, string):
        return b64decode(string)

    @classmethod
    def encode(cls, string):
        return b64encode(string)



hexAt = "\x00"
hexB = "\x02"
hexC = "\x03"
hexD = "\x04"
hexF = "\x06"
hex0 = "\x30"

hex31 = 0x1f
hex127 = 0x7f
hex129 = 0xa0
hex160 = 0x80
hex224 = 0xe0

bytesHex0 = toBytes(hex0)
bytesHexB = toBytes(hexB)
bytesHexC = toBytes(hexC)
bytesHexD = toBytes(hexD)
bytesHexF = toBytes(hexF)


def encodeSequence(*encodedPieces):
    totalLengthLen = sum([len(p) for p in encodedPieces])
    return hex0 + _encodeLength(totalLengthLen) + "".join(encodedPieces)


def encodeInteger(x):
    assert x >= 0
    t = ("%x" % x).encode()

    if len(t) % 2:
        t = toBytes("0") + t

    x = BinaryAscii.binaryFromHex(t)
    num = x[0] if isinstance(x[0], intTypes) else ord(x[0])

    if num <= hex127:
        return hexB + chr(len(x)) + toString(x)
    return hexB + chr(len(x) + 1) + hexAt + toString(x)


def encodeOid(first, second, *pieces):
    assert first <= 2
    assert second <= 39

    encodedPieces = [chr(40 * first + second)] + [_encodeNumber(p) for p in pieces]
    body = "".join(encodedPieces)

    return hexF + _encodeLength(len(body)) + body


def encodeBitString(t):
    return hexC + _encodeLength(len(t)) + t


def encodeOctetString(t):
    return hexD + _encodeLength(len(t)) + t


def encodeConstructed(tag, value):
    return chr(hex129 + tag) + _encodeLength(len(value)) + value


def removeSequence(string):
    _checkSequenceError(string=string, start=bytesHex0, expected="30")

    length, lengthLen = _readLength(string[1:])
    endSeq = 1 + lengthLen + length

    return string[1 + lengthLen: endSeq], string[endSeq:]


def removeInteger(string):
    _checkSequenceError(string=string, start=bytesHexB, expected="02")

    length, lengthLen = _readLength(string[1:])
    numberBytes = string[1 + lengthLen:1 + lengthLen + length]
    rest = string[1 + lengthLen + length:]
    nBytes = numberBytes[0] if isinstance(
        numberBytes[0], intTypes
    ) else ord(numberBytes[0])

    assert nBytes < hex160

    return int(BinaryAscii.hexFromBinary(numberBytes), 16), rest


def removeObject(string):
    _checkSequenceError(string=string, start=bytesHexF, expected="06")

    length, lengthLen = _readLength(string[1:])
    body = string[1 + lengthLen:1 + lengthLen + length]
    rest = string[1 + lengthLen + length:]
    numbers = []

    while body:
        n, lengthLength = _readNumber(body)
        numbers.append(n)
        body = body[lengthLength:]

    n0 = numbers.pop(0)
    first = n0 // 40
    second = n0 - (40 * first)
    numbers.insert(0, first)
    numbers.insert(1, second)

    return tuple(numbers), rest


def removeBitString(string):
    _checkSequenceError(string=string, start=bytesHexC, expected="03")

    length, lengthLen = _readLength(string[1:])
    body = string[1 + lengthLen:1 + lengthLen + length]
    rest = string[1 + lengthLen + length:]

    return body, rest


def removeOctetString(string):
    _checkSequenceError(string=string, start=bytesHexD, expected="04")

    length, lengthLen = _readLength(string[1:])
    body = string[1 + lengthLen:1 + lengthLen + length]
    rest = string[1 + lengthLen + length:]

    return body, rest


def removeConstructed(string):
    s0 = _extractFirstInt(string)
    if (s0 & hex224) != hex129:
        raise Exception("wanted constructed tag (0xa0-0xbf), got 0x%02x" % s0)

    tag = s0 & hex31
    length, lengthLen = _readLength(string[1:])
    body = string[1 + lengthLen:1 + lengthLen + length]
    rest = string[1 + lengthLen + length:]

    return tag, body, rest


def fromPem(pem):
    t = "".join([
        l.strip() for l in pem.splitlines()
        if l and not l.startswith("-----")
    ])
    return Base64.decode(t)


def toPem(der, name):
    b64 = toString(Base64.encode(der))
    lines = ["-----BEGIN " + name + "-----\n"]
    lines.extend([
        b64[start:start + 64] 
        for start in xrange(0, len(b64), 64)
    ])
    lines.append("\n")
    lines.append("-----END " + name + "-----\n")

    return "".join(lines)


def _encodeLength(length):
    assert length >= 0

    if length < hex160:
        return chr(length)

    s = ("%x" % length).encode()
    if len(s) % 2:
        s = "0" + s

    s = BinaryAscii.binaryFromHex(s)
    lengthLen = len(s)

    return chr(hex160 | lengthLen) + str(s)


def _encodeNumber(n):
    b128Digits = []
    while n:
        b128Digits.insert(0, (n & hex127) | hex160)
        n >>= 7

    if not b128Digits:
        b128Digits.append(0)

    b128Digits[-1] &= hex127

    return "".join([chr(d) for d in b128Digits])


def _readLength(string):
    num = _extractFirstInt(string)
    if not (num & hex160):
        return (num & hex127), 1

    lengthLen = num & hex127

    if lengthLen > len(string) - 1:
        raise Exception("ran out of length bytes")

    return int(BinaryAscii.hexFromBinary(string[1:1 + lengthLen]), 16), 1 + lengthLen


def _readNumber(string):
    number = 0
    lengthLen = 0
    while True:
        if lengthLen > len(string):
            raise Exception("ran out of length bytes")

        number <<= 7
        d = string[lengthLen]
        if not isinstance(d, intTypes):
            d = ord(d)

        number += (d & hex127)
        lengthLen += 1
        if not d & hex160:
            break

    return number, lengthLen


def _checkSequenceError(string, start, expected):
    if not string.startswith(start):
        raise Exception(
            "wanted sequence (0x%s), got 0x%02x" %
            (expected, _extractFirstInt(string))
        )


def _extractFirstInt(string):
    return string[0] if isinstance(string[0], intTypes) else ord(string[0])

#
# Elliptic Curve Equation
#
# y^2 = x^3 + A*x + B (mod P)
#

class Point:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class CurveFp:

    def __init__(self, A, B, P, N, Gx, Gy, name, oid, nistName=None):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.G = Point(Gx, Gy)
        self.name = name
        self.nistName = nistName
        self.oid = oid

    def contains(self, p):
        """
        Verify if the point `p` is on the curve
        :param p: Point p = Point(x, y)
        :return: boolean
        """
        return (p.y**2 - (p.x**3 + self.A * p.x + self.B)) % self.P == 0

    def length(self):
        return (1 + len("%x" % self.N)) // 2


secp256k1 = CurveFp(
    name="secp256k1",
    A=0x0000000000000000000000000000000000000000000000000000000000000000,
    B=0x0000000000000000000000000000000000000000000000000000000000000007,
    P=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    Gx=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    Gy=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    oid=(1, 3, 132, 0, 10)
)

prime256v1 = CurveFp(
    name="prime256v1",
    nistName="P-256",
    A=0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
    B=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    P=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    N=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
    Gx=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    Gy=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
    oid=(1, 2, 840, 10045, 3, 1, 7),
)
p256 = prime256v1

supportedCurves = [
    secp256k1,
    prime256v1,
]

curvesByOid = {curve.oid: curve for curve in supportedCurves}


hexAt = "\x00"


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

    def toString(self):
        return BinaryAscii.stringFromNumber(number=self.secret, length=self.curve.length())

    def toDer(self):
        encodedPublicKey = self.publicKey().toString(encoded=True)

        return encodeSequence(
            encodeInteger(1),
            encodeOctetString(self.toString()),
            encodeConstructed(0, encodeOid(*self.curve.oid)),
            encodeConstructed(1, encodeBitString(encodedPublicKey)),
        )

    def toPem(self):
        return toPem(der=toBytes(self.toDer()), name="EC PRIVATE KEY")

    @classmethod
    def fromPem(cls, string):
        privateKeyPem = string[string.index("-----BEGIN EC PRIVATE KEY-----"):]
        return cls.fromDer(fromPem(privateKeyPem))

    @classmethod
    def fromDer(cls, string):
        t, empty = removeSequence(string)
        if len(empty) != 0:
            raise Exception(
                "trailing junk after DER private key: " +
                BinaryAscii.hexFromBinary(empty)
            )

        one, t = removeInteger(t)
        if one != 1:
            raise Exception(
                "expected '1' at start of DER private key, got %d" % one
            )

        privateKeyStr, t = removeOctetString(t)
        tag, curveOidStr, t = removeConstructed(t)
        if tag != 0:
            raise Exception("expected tag 0 in DER private key, got %d" % tag)

        oidCurve, empty = removeObject(curveOidStr)

        if len(empty) != 0:
            raise Exception(
                "trailing junk after DER private key curve_oid: %s" %
                BinaryAscii.hexFromBinary(empty)
            )

        if oidCurve not in curvesByOid:
            raise Exception(
                "unknown curve with oid %s; The following are registered: %s" % (
                    oidCurve,
                    ", ".join([curve.name for curve in supportedCurves])
                )
            )

        curve = curvesByOid[oidCurve]

        if len(privateKeyStr) < curve.length():
            privateKeyStr = hexAt * (curve.lenght() - len(privateKeyStr)) + privateKeyStr

        return cls.fromString(privateKeyStr, curve)

    @classmethod
    def fromString(cls, string, curve=secp256k1):
        return PrivateKey(secret=BinaryAscii.numberFromString(string), curve=curve)


class Signature:

    def __init__(self, r, s, recoveryId=None):
        self.r = r
        self.s = s
        self.recoveryId = recoveryId

    def toDer(self, withRecoveryId=False):
        encodedSequence = encodeSequence(encodeInteger(self.r), encodeInteger(self.s))
        if not withRecoveryId:
            return encodedSequence
        return chr(27 + self.recoveryId) + encodedSequence

    def toBase64(self, withRecoveryId=False):
        return toString(Base64.encode(toBytes(self.toDer(withRecoveryId=withRecoveryId))))

    @classmethod
    def fromDer(cls, string, recoveryByte=False):
        recoveryId = None
        if recoveryByte:
            recoveryId = string[0] if isinstance(string[0], intTypes) else ord(string[0])
            recoveryId -= 27
            string = string[1:]

        rs, empty = removeSequence(string)
        if len(empty) != 0:
            raise Exception("trailing junk after DER signature: %s" % BinaryAscii.hexFromBinary(empty))

        r, rest = removeInteger(rs)
        s, empty = removeInteger(rest)
        if len(empty) != 0:
            raise Exception("trailing junk after DER numbers: %s" % BinaryAscii.hexFromBinary(empty))

        return Signature(r=r, s=s, recoveryId=recoveryId)

    @classmethod
    def fromBase64(cls, string, recoveryByte=False):
        der = Base64.decode(string)
        return cls.fromDer(der, recoveryByte)



class Math:

    @classmethod
    def multiply(cls, p, n, N, A, P):
        """
        Fast way to multily point and scalar in elliptic curves
        :param p: First Point to mutiply
        :param n: Scalar to mutiply
        :param N: Order of the elliptic curve
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        return cls._fromJacobian(
            cls._jacobianMultiply(
                cls._toJacobian(p),
                n,
                N,
                A,
                P,
            ),
            P,
        )

    @classmethod
    def add(cls, p, q, A, P):
        """
        Fast way to add two points in elliptic curves
        :param p: First Point you want to add
        :param q: Second Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        return cls._fromJacobian(
            cls._jacobianAdd(
                cls._toJacobian(p),
                cls._toJacobian(q),
                A,
                P,
            ),
            P,
        )

    @classmethod
    def inv(cls, x, n):
        """
        Extended Euclidean Algorithm. It's the 'division' in elliptic curves
        :param x: Divisor
        :param n: Mod for division
        :return: Value representing the division
        """
        if x == 0:
            return 0

        lm, hm = 1, 0
        low, high = x % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low

        return lm % n

    @classmethod
    def _toJacobian(cls, p):
        """
        Convert point to Jacobian coordinates
        :param p: First Point you want to add
        :return: Point in Jacobian coordinates
        """
        return Point(p.x, p.y, 1)

    @classmethod
    def _fromJacobian(cls, p, P):
        """
        Convert point back from Jacobian coordinates
        :param p: First Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point in default coordinates
        """
        z = cls.inv(p.z, P)

        return Point(
            (p.x * z ** 2) % P,
            (p.y * z ** 3) % P,
        )

    @classmethod
    def _jacobianDouble(cls, p, A, P):
        """
        Double a point in elliptic curves
        :param p: Point you want to double
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        if not p.y:
            return Point(0, 0, 0)

        ysq = (p.y ** 2) % P
        S = (4 * p.x * ysq) % P
        M = (3 * p.x ** 2 + A * p.z ** 4) % P
        nx = (M**2 - 2 * S) % P
        ny = (M * (S - nx) - 8 * ysq ** 2) % P
        nz = (2 * p.y * p.z) % P
        return Point(nx, ny, nz)

    @classmethod
    def _jacobianAdd(cls, p, q, A, P):
        """
        Add two points in elliptic curves
        :param p: First Point you want to add
        :param q: Second Point you want to add
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """

        if not p.y:
            return q
        if not q.y:
            return p

        U1 = (p.x * q.z ** 2) % P
        U2 = (q.x * p.z ** 2) % P
        S1 = (p.y * q.z ** 3) % P
        S2 = (q.y * p.z ** 3) % P

        if U1 == U2:
            if S1 != S2:
                return Point(0, 0, 1)
            return cls._jacobianDouble(p, A, P)

        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % P
        H3 = (H * H2) % P
        U1H2 = (U1 * H2) % P
        nx = (R ** 2 - H3 - 2 * U1H2) % P
        ny = (R * (U1H2 - nx) - S1 * H3) % P
        nz = (H * p.z * q.z) % P

        return Point(nx, ny, nz)

    @classmethod
    def _jacobianMultiply(cls, p, n, N, A, P):
        """
        Multily point and scalar in elliptic curves
        :param p: First Point to mutiply
        :param n: Scalar to mutiply
        :param N: Order of the elliptic curve
        :param P: Prime number in the module of the equation Y^2 = X^3 + A*X + B (mod p)
        :param A: Coefficient of the first-order term of the equation Y^2 = X^3 + A*X + B (mod p)
        :return: Point that represents the sum of First and Second Point
        """
        if p.y == 0 or n == 0:
            return Point(0, 0, 1)

        if n == 1:
            return p

        if n < 0 or n >= N:
            return cls._jacobianMultiply(p, n % N, N, A, P)

        if (n % 2) == 0:
            return cls._jacobianDouble(
                cls._jacobianMultiply(
                    p,
                    n // 2,
                    N,
                    A,
                    P
                ),
                A,
                P,
            )

        # (n % 2) == 1:
        return cls._jacobianAdd(
            cls._jacobianDouble(
                cls._jacobianMultiply(
                    p,
                    n // 2,
                    N,
                    A,
                    P,
                ),
                A,
                P,
            ),
            p,
            A,
            P,
        )
class PublicKey:

    def __init__(self, point, curve):
        self.point = point
        self.curve = curve

    def toString(self, encoded=False):
        xString = BinaryAscii.stringFromNumber(
            number=self.point.x,
            length=self.curve.length(),
        )
        yString = BinaryAscii.stringFromNumber(
            number=self.point.y,
            length=self.curve.length(),
        )
        return "\x00\x04" + xString + yString if encoded else xString + yString

    def toDer(self):
        oidEcPublicKey = (1, 2, 840, 10045, 2, 1)
        encodeEcAndOid = encodeSequence(
            encodeOid(*oidEcPublicKey),
            encodeOid(*self.curve.oid),
        )

        return encodeSequence(encodeEcAndOid, encodeBitString(self.toString(encoded=True)))

    def toPem(self):
        return toPem(der=toBytes(self.toDer()), name="PUBLIC KEY")

    @classmethod
    def fromPem(cls, string):
        return cls.fromDer(fromPem(string))

    @classmethod
    def fromDer(cls, string):
        s1, empty = removeSequence(string)
        if len(empty) != 0:
            raise Exception("trailing junk after DER public key: {}".format(
                BinaryAscii.hexFromBinary(empty)
            ))

        s2, pointBitString = removeSequence(s1)

        oidPk, rest = removeObject(s2)

        oidCurve, empty = removeObject(rest)
        if len(empty) != 0:
            raise Exception("trailing junk after DER public key objects: {}".format(
                BinaryAscii.hexFromBinary(empty)
            ))

        if oidCurve not in curvesByOid:
            raise Exception(
                "Unknown curve with oid %s. Only the following are available: %s" % (
                    oidCurve,
                    ", ".join([curve.name for curve in supportedCurves])
                )
            )

        curve = curvesByOid[oidCurve]

        pointStr, empty = removeBitString(pointBitString)
        if len(empty) != 0:
            raise Exception(
                "trailing junk after public key point-string: " +
                BinaryAscii.hexFromBinary(empty)
            )

        return cls.fromString(pointStr[2:], curve)

    @classmethod
    def fromString(cls, string, curve=secp256k1, validatePoint=True):
        baseLen = curve.length()

        xs = string[:baseLen]
        ys = string[baseLen:]

        p = Point(
            x=BinaryAscii.numberFromString(xs),
            y=BinaryAscii.numberFromString(ys),
        )

        if validatePoint and not curve.contains(p):
            raise Exception(
                "point ({x},{y}) is not valid for curve {name}".format(
                    x=p.x, y=p.y, name=curve.name
                )
            )

        return PublicKey(point=p, curve=curve)




from config import *

from lib.config_system import get_config
from lib.settings_system import the_settings
from lib.encryption import encrypt, decrypt

import json
import os
from hashlib import sha256

def save_wallet_list(publicKey,privateKey,password):
    wallet_list = get_saved_wallet()


    wallet_list[publicKey] = {}

    wallet_list[publicKey]["publickey"] = publicKey
    wallet_list[publicKey]["privatekey"] = privateKey

    wallet_list[publicKey]["password_sha256"] = sha256(password.encode("utf-8")).hexdigest()


    



    os.chdir(get_config()["main_folder"])
    with open(WALLETS_PATH, 'w') as wallet_list_file:
        json.dump(wallet_list, wallet_list_file, indent=4)



def get_saved_wallet():
    
        os.chdir(get_config()["main_folder"])

        if not os.path.exists(WALLETS_PATH):
            return {}
        

        with open(WALLETS_PATH, 'rb') as wallet_list_file:
            return json.load(wallet_list_file)






def Wallet_Create(password, save = True):

    my_private_key = PrivateKey()
    my_public_key = my_private_key.publicKey()




    if save == True:
        encrypted_key = encrypt(my_private_key.toPem(),password) if not len(list(get_saved_wallet())) == 0 else my_private_key.toPem()
        del my_private_key
        save_wallet_list(my_public_key.toPem(),encrypted_key, password)
        return (encrypted_key)
    else:
        return (my_private_key)

def Wallet_Import(account,mode,password = None):
    """
    A function for get info about a wallet.

    Inputs:
      * account: Account index of saved accounts (if you give -1 the default wallet will use)
      * mode: Information mode [0 = Public key | 1 = Private key (needs password) | 2 = Returns sha256 of password | 3 = Returns the address of account]
      * password: Some function needed password for operation you can give with this input
    """

    temp_saved_wallet = get_saved_wallet()

    number_of_wallet = len(temp_saved_wallet)
    if not number_of_wallet:
        return None

    if isinstance(account,int):
        if not -1 == account:
            account = list(temp_saved_wallet)[account]
        else:
            account = list(temp_saved_wallet)[the_settings()["wallet"]]

    if mode == 0:
        my_public_key = temp_saved_wallet[account]["publickey"]

        return my_public_key
    elif mode == 1:
        if not password is None and not list(temp_saved_wallet).index(account) == 0:

            return decrypt(temp_saved_wallet[account]["privatekey"], password)
        else:
            my_private_key = temp_saved_wallet[account]["privatekey"]

            return my_private_key

    elif mode == 2:
            return temp_saved_wallet[account]["password_sha256"]

    elif mode == 3:
        my_address = temp_saved_wallet[account]["publickey"]
        my_address = "".join([
            l.strip() for l in my_address.splitlines()
            if l and not l.startswith("-----")
        ])
        my_address = Address(my_address)
        return my_address
    else:
        raise ValueError("the mode variable contains an unplanned value")


def Wallet_Delete(account):
    saved_wallet = get_saved_wallet()
    if account in saved_wallet:
        del saved_wallet[account]
        from lib.config_system import get_config
    
        os.chdir(get_config()["main_folder"])
        with open(WALLETS_PATH, 'w') as wallet_list_file:
            json.dump(saved_wallet, wallet_list_file, indent=4)

def Address(publickey):

    return sha256(sha256(publickey.encode("utf-8")).hexdigest().encode("utf-8")).hexdigest()[-40:]
