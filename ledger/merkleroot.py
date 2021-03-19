from typing import List
import typing
import hashlib
 
class Leaf:
    def __init__(self, left, right, value: str,content)-> None:
        self.left: Leaf = left
        self.right: Leaf = right
        self.value = value
        self.content = content
    
    @staticmethod
    def hash(val: str)-> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()
    def __str__(self):
      return (str(self.value))
 
class MerkleTree:
    def __init__(self, values: List[str])-> None:
        self.__buildTree(values)
 
    def __buildTree(self, values: List[str])-> None:
 
        leaves: List[Leaf] = [Leaf(None, None, Leaf.hash(e),e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: Leaf = self.__buildTreeRec(leaves) 
    
    def __buildTreeRec(self, Leafs: List[Leaf])-> Leaf:
        half: int = len(Leafs) // 2
 
        if len(Leafs) == 2:
            return Leaf(Leafs[0], Leafs[1], Leaf.hash(Leafs[0].value + Leafs[1].value), Leafs[0].content+"+"+Leafs[1].content)
        
        left: Leaf = self.__buildTreeRec(Leafs[:half])
        right: Leaf = self.__buildTreeRec(Leafs[half:])
        value: str = Leaf.hash(left.value + right.value)
        content: str = self.__buildTreeRec(Leafs[:half]).content+"+"+self.__buildTreeRec(Leafs[half:]).content
        return Leaf(left, right, value,content)
    
    def printTree(self)-> None:
        self.__printTreeRec(self.root)
 
    def __printTreeRec(self, Leaf)-> None:
        if Leaf != None:
            if Leaf.left != None:
             print("Left: "+str(Leaf.left))
             print("Right: "+str(Leaf.right))
            else:
             print("Input")
            print("Value: "+str(Leaf.value))
            print("Content: "+str(Leaf.content))
            print("")
            self.__printTreeRec(Leaf.left)
            self.__printTreeRec(Leaf.right)
    
    def getRootHash(self)-> str:
        return self.root.value
        
        
        
def mixmerkletree(list_data):
    """
    print("Inputs: ")
    print(*list_data, sep = " | ")
    print("")
    """
    mtree = MerkleTree(list_data)
    """
    print("Root Hash: "+mtree.getRootHash()+"\n")
    print(mtree.printTree())
    """
    return mtree