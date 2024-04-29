import oram

oram = oram.Oram(6, 2**16)
oram.write("file_name.txt")
oram.read("file_name.txt")