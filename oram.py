from tree import Tree
from block import Block
import main
from shutil import copy

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
        
        node, block = self.findFile(self.file_ids[file_name])
        
        readpath = self.tree.getPath(block.getLeaf())
        for pos in readpath:
            ## download, decrypt
            ## if pos==node, download as file_name
            ## keep track of new file names
            ## note: try reading into buffer from drive instead of whole new file
            main.download_and_decrypt([f"File_{pos}.txt"], [f"File_{pos}.txt"])
            print(pos)
            pass
        copy(f"File_{node}.txt", file_name)
        for pos in readpath:
            ## upload, encrypt each file in file names
            main.enc_and_upload(f"File_{pos}.txt")
            print(pos)
            pass
        ##print("copy file to copy into filename")
        for pos in readpath:
            ## delete files excdpt for filename
            print(pos)
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
        ## pad the file to size
        padding_length, padded_file = self.filePad(file_name)
        for file in path:
            ##download and decrypt
            ## track names of files downloaded
            main.download_and_decrypt([f"File_{file}.txt"], [f"File_{file}.txt"])            
            print(file)
        copy(padded_file, f"File_{pos}.txt")
        for file in path:
            main.enc_and_upload(f"File_{file}.txt")
        return
    
    def delete(self, file_name) -> None:
        if not (file_name in self.file_ids):
            print("file not found")
            return
        pos, block = self.findFile(self.file_ids[file_name])
        self.tree.blocks[pos] = None
        self.file_ids.pop(file_name)

    def findFile(self, file_id) -> tuple[int, Block]:
        for i in range(len(self.tree.blocks)):
            if self.tree.blocks[i]:
                if self.tree.blocks[i].blockID == file_id:
                    return (i, self.tree.blocks[i])


    def filePad(self, file_name) -> tuple[int, str]:
        my_file = open(file_name, "r")
        contents = my_file.read().encode('utf-8')
        my_file.close()
        padding_length = 2**16 - len(contents)
        contents += ("0" * padding_length).encode("utf-8")
        padded_file = open(f"{file_name}_padded", "w")
        print(len(contents.decode('utf-8')))
        padded_file.write(contents.decode("utf-8"))
        padded_file.close()
        return (padding_length, f"{file_name}_padded")

        



        ### find id in tree

