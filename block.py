class Block:
    def __init__(self, blockID, leaf, name) -> None:
        self.blockID = blockID
        self.leaf = leaf
        self.name = name
    
    
    def getLeaf(self)->int:
        return self.leaf
    

    def setLeaf(self, leaf)->int:
        self.leaf = leaf
        return self.leaf
    
    def getBlockID(self)-> int:
        return self.blockID
    
    def getName(self)->str:
        return self.name
    
    def setName(self, name)->str:
        self.name = name
        return self.name