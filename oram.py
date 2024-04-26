from tree import Tree
from block import Block

class Oram:
    def __init__(self, height, max_file_size) -> None:
        self.tree = Tree(height)
        self.max_file_size = max_file_size
        self.file_ids = {}
        self.counter = 0

    def read(self, file_name) -> None:
        ### check to id associated with file_name
        if not (file_name in self.file_ids):
            print("file not found")
            return
        node = None
        block: Block = None
        file_id = self.file_ids[file_name]
        for i in range(self.tree.height):
            if self.tree.blocks[i] == file_id:
                node = i
                block =self.tree.blocks[i]
        
        readpath = self.tree.getPath(block.getLeaf())
        for pos in readpath:
            ## download, decrypt
            ## if pos==node, download as file_name
            ## keep track of new file names
            ## note: try reading into buffer from drive instead of whole new file
            pass
        for pos in readpath:
            ## upload, encrypt each file in file names
            pass
        for pos in readpath:
            ## delete files excdpt for filename
            pass

        return
    
    
    def write(self, file_name) -> None:
        self.counter += 1
        self.file_ids[file_name] = self.counter
        new_id = self.counter
        new_leaf = self.tree.randomLeaf()
        new_height = self.tree.randomHeight()
        while not self.tree.isEmpty(new_leaf, new_height):
            new_leaf = self.tree.randomLeaf()
            new_height = self.tree.randomHeight()
        pos = self.tree.findIdx(new_leaf, new_height)
        self.tree.blocks[pos] = Block(new_id, new_leaf, file_name)
        ## Encrypt file, write to l{pos}
        path = self.tree.getPath(new_leaf)
        for file in path:
            ##download and decrypt
            ## track names of files downloaded
            pass


        ### find id in tree

