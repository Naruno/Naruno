#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Decentra Network Developers
Copyright (c) 2021 Onur Atakan ULUSOY

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
import hashlib
from typing import List


class Leaf:
    """
    The leaf class for merkle tree.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.value = hashlib.sha256(
            (self.left + self.right).encode("utf-8")
        ).hexdigest()


class MerkleTree:
    """
    The merkle tree class.
    """

    def __init__(self, values: List[str]) -> None:
        if values:
            self.merkleCalculator(values)
        else:
            self.root = ""

    def merkleCalculator(self, hashList):
        """
        The main calculator.
        """

        if len(hashList) == 1:
            self.root = hashList[0]
            return
        newHashList = []

        for i in range(0, len(hashList) - 1, 2):
            newHashList.append(Leaf(hashList[i], hashList[i + 1]).value)
        if len(hashList) % 2 == 1:
            newHashList.append(Leaf(hashList[-1], hashList[-1]).value)

        return self.merkleCalculator(newHashList)

    def getRootHash(self) -> str:
        """
        Returns the merkle root.
        """

        return self.root
