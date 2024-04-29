from random import randint

class Tree:
    height: int
    size: int
    blocks: list


    def __init__(self, height) -> None:
        self.height = height
        self.size = 2**height - 1
        self.blocks = [None] * self.size

    def randomLeaf(self)->int:
        return randint(self.size//2, self.size-1)
    
    def randomHeight(self)->int:
        return randint(0,self.height-1)
    
    def randomIndex(self)->int:
        return randint(0, self.size-1)
    
    def isEmptyIdx(self, idx) -> bool:
        return self.blocks[idx] == None
    
    def isEmpty(self, leaf, height) -> bool:
        return self.isEmptyIdx(self.findIdx(leaf, height))
    
    def findIdx(self, leaf, height)->int:
        idx = leaf
        for i in range(height):
            idx = (leaf - 1)//2
        return idx
    
    def getPath(self, leaf)->list[int]:
        path = [0] * self.height
        for i in range(self.height):
            path[i] = leaf
            if leaf != 0:
                leaf = (leaf -1)// 2
        return path