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

from typing import List

import hashlib


class Leaf:
    """
    The leaf class for merkle tree.
    """

    def __init__(self, left, right, value: str,content)-> None:
        self.left: Leaf = left
        self.right: Leaf = right
        self.value = value
        self.content = content
    
    @staticmethod
    def hash(val: str)-> str:
        """
        Returns the sha256 of the value.

        Inputs:
          * val: A string.
        """

        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
      return (str(self.value))



class MerkleTree:
    """
    The merkle tree class.
    """

    def __init__(self, values: List[str])-> None:
        self.__buildTree(values)
 
    def __buildTree(self, values: List[str])-> None:
        """
        Calculate and append the leafs
        """

        leaves: List[Leaf] = [Leaf(None, None, Leaf.hash(e),e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: Leaf = self.__buildTreeRec(leaves) 
    
    def __buildTreeRec(self, leafs: List[Leaf])-> Leaf:
        """
        Calculate and returns the results of the leaf by parent leafs
        """

        half: int = len(leafs) // 2
 
        if len(leafs) == 2:
            return Leaf(leafs[0], leafs[1], Leaf.hash(leafs[0].value + leafs[1].value), leafs[0].content+"+"+leafs[1].content)
        
        left: Leaf = self.__buildTreeRec(leafs[:half])
        right: Leaf = self.__buildTreeRec(leafs[half:])
        value: str = Leaf.hash(left.value + right.value)
        content: str = self.__buildTreeRec(leafs[:half]).content+"+"+self.__buildTreeRec(leafs[half:]).content
        return Leaf(left, right, value,content)
    
    def printTree(self)-> None:
        """
        Prints the last leaf element.
        """

        self.__printTreeRec(self.root)
 
    def __printTreeRec(self, node)-> None:
        """
        Prints the leaf elements.
        """

        if node != None:
            if node.left != None:
             print("Left: "+str(node.left))
             print("Right: "+str(node.right))
            else:
             print("Input")
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)
    
    def getRootHash(self)-> str:
        """
        Returns the merkle root.
        """

        return self.root.value
