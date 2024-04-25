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
        return randint(0,4)
    
    def isEmpty(self, idx) -> bool:
        return self.blocks[idx] == None
    
    def findIdx(self, leaf, height)->int:
        idx = leaf
        for i in range(height):
            idx = leaf//2
        return idx
    
    def getPath(self, leaf)->list[int]:
        path = [0] * self.height
        for i in range(self.height):
            path[i] = leaf
            if leaf != 0:
                leaf = leaf // 2
        return path