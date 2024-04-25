from tree import Tree
from block import Block

class Oram:
    def __init__(self, height, max_file_size) -> None:
        self.tree = Tree(height)
        self.max_file_size = max_file_size
        self.file_ids = {}

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
            ## read, decrypt, re-encrypt (diff) and reupload
            ## if pos==node, keep the file and give it file_name
            ## else, delete download
            ## note: try reading into buffer from drive instead of whole new file
            pass
        return


        ### find id in tree

