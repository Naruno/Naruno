#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Elliptic Curve Equation
#
# y^2 = x^3 + A*x + B (mod P)
#
from decentra_network.wallet.ellipticcurve.point import Point


class CurveFp:

    def __init__(self, A, B, P, N, Gx, Gy, name, oid, nistName=None):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.G = Point(Gx, Gy)
        self.name = name
        self.nistName = nistName
        self.oid = oid  # ASN.1 Object Identifier

    def length(self):
        return (1 + len("%x" % self.N)) // 2


secp256k1 = CurveFp(
    name="secp256k1",
    A=0x0000000000000000000000000000000000000000000000000000000000000000,
    B=0x0000000000000000000000000000000000000000000000000000000000000007,
    P=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    oid=[1, 3, 132, 0, 10],
)

prime256v1 = CurveFp(
    name="prime256v1",
    nistName="P-256",
    A=0xFFFFFFFF000000010000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    B=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    P=0xFFFFFFFF000000010000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    N=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    Gx=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    Gy=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
    oid=[1, 2, 840, 10045, 3, 1, 7],
)

p256 = prime256v1

supportedCurves = [
    secp256k1,
    prime256v1,
]

_curvesByOid = {tuple(curve.oid): curve for curve in supportedCurves}


def getCurveByOid(oid):

    return _curvesByOid[oid]
