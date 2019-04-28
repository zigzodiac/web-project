import os
import sys

path1 = os.path.dirname(__file__)
print os.path.dirname(path1)
print sys.argv
# str = raw_input("please input:")
file_dir = open("filedir.txt","w")
print file_dir.name, file_dir.mode
file_dir.write("www.google.com\n")

str = file_dir.read()
print str
file_dir.close()
