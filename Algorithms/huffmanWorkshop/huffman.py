'''
Created on Oct 26, 2014
 
@author: Gary
'''
 
import huffman_tree
import os
from collections import Counter
from bitarray import bitarray
from Tkconstants import FIRST
# I used the module bitarray to write the binary files,
# read the binary files, and decode the binary to an original 
# message.
# 
# bitarray is easy to install with the python package manager (pip),
# but on my computer I was required to install a python c++ compiler
# as a dependency. To install pip, find the file get-pip.py on the 
# internet and run it in a command prompt.
# To install bit array use the following command:
# python -m pip install bitarray
# 
# Any dependency issues will be brought up on the command line when 
# that command is entered. 
 
 
 
#f_out = open('outfile.txt', 'w')
 
''' Count up the occurrences of each character '''
 
'''
USE "Counter()" container that you imported!!!!
cnt = Here it is a counter of characters
'''
cnt = Counter()
 
with open('infile2.txt' , 'r') as f:
    while True:
        c = f.read(1)
        if not c:
            print "End of file"
            break
		#INSERT use of Counter() here!!!!
        cnt[c] += 1
#         print "Read a character:", c
f.close()
 
''' Create a Huffman Tree '''
 
'''
USE a different instance of "Counter()" container!!!!
huffmanSubtrees = This time it will be a counter of huffmanNode type
'''
huffmanSubtrees = Counter()
 
for charCnt in cnt.most_common():
# 	Here we need code to copy from charCnt to huffmanSubtrees!!!!
# 	We are creating new HuffmanNode and stuffing it into huffmanSubtree container
# 	(charCnt[0],charCnt[1]) is a tupple with (character, countOfCharacter)
    node = huffman_tree.Node(charCnt[0], charCnt[1])
    huffmanSubtrees[node] = charCnt[1]
     
     
     
     
 	
 
while len(huffmanSubtrees) > 1 :
	# Take the two least common Nodes
    node1 = huffmanSubtrees.most_common()[len(huffmanSubtrees)-1][0]
    node2 = huffmanSubtrees.most_common()[len(huffmanSubtrees)-2][0]
	# Create a new Node with the two above as a leaf (TODO) and add to huffmanSubtrees (TODO)
    newNode, nodeCount = node2.join(node1)
    huffmanSubtrees[newNode] = nodeCount
 	
	# Delete the old nodes
    del huffmanSubtrees[node1]
    del huffmanSubtrees[node2]
     
''' Print our Huffman Tree '''
new_root = huffmanSubtrees.most_common()[0][0]
new_root.print_tree_nice(0,0)
 
 
#make huffman keys
huffman_encoding = new_root.huffman_map()
 
 
#make a bitarray from infile2.txt using keys 
bitArray = bitarray()
with open('infile2.txt' , 'r') as f:
    while True:
        c = f.read(1)
        if not c:
            print "End of file"
            break
        binChar = bitarray(huffman_encoding[c])
        bitArray += binChar
 
#write bitArray to file
with open(("outfile.bin"), "wb") as fh:
    bitArray.tofile(fh)
fh.close()
 
#read bits from file
bitArrayTwo = bitarray() 
with open(("outfile.bin"), "rb") as fhTwo:
    bitArrayTwo.fromfile(fhTwo)
 
#interpret message
 
#the cheating way..
for char in huffman_encoding.keys():
    huffman_encoding[char] = bitarray(huffman_encoding[char])
print "".join(bitArrayTwo.decode(huffman_encoding))
    
print "original file size: " + str(os.path.getsize("infile2.txt")) + "\n"
print "compressed file size: " + str(os.path.getsize("outfile.bin")) + "\n"
 
"""If I was going to do this without bitarray I would first 
read the bits of the file into a buffer variable. I would then 
loop through the bits and append them to a string variable. At 
each itteration of the loop I would check to see if the string 
variable contained a sequence that was in my huffman dictionary.
If so, I would add the corrisponding charicter to the result variable,
and then clear the string variable. eventually you would have 
the whole file written out into the result variable. 
"""
 
 
 


