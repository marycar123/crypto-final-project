class Block:


    def __init__(self, blockID, leaf, name, padding) -> None:
        self.blockID = blockID
        self.leaf = leaf
        self.name = name
        self.padding = padding
    
    
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
    
    def setPadding(self, padding)-> int:
        self.padding = padding
        return self.padding
    
    def getPadding(self)->int:
        return self.padding