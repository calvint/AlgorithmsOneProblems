from __future__ import print_function

class Node:
    """
    Tree node: left and right child + data which can be any object
    """
    def __init__(self, char, count):
        """
        Node constructor

        @param data node data object
        """
        self.left  = None
        self.right = None
        self.parnt = None
        self.char  = char
        self.count = count

    def join(self, second_node):
        """
        Join two nodes into a single subtree

        @param second node to join
        @returns the root of combined subtree
        """
        retVal = Node('',0)
		
		#insert good code here!!!!
        retVal.right = self
        retVal.left = second_node
        retVal.count = self.count + second_node.count 
        self.parnt = retVal
        second_node.parnt = retVal
        return retVal, retVal.count

                
    def print_tree_nice(self, space_cnt, depth):
        """
        Print tree content in tree nicely
        Use .(0,0) as default call
        """
        if self.right:
            self.right.print_tree_nice(space_cnt+4, depth+1)

        if self.char == "":
            print (" "*space_cnt,     depth, "<", sep=''         )
        elif self.char == ' ':
            print (" "*space_cnt,  "_space", "(", self.count, ")")
        elif self.char == '\n':
            print (" "*space_cnt,     "\\n", "(", self.count, ")")
        elif self.char == '\r':
            print (" "*space_cnt,     "\\r", "(", self.count, ")")
        else:
            print (" "*space_cnt, self.char, "(", self.count, ")")

        if self.left:
            self.left.print_tree_nice(space_cnt+4, depth+1)
        
    def huffman_map(self,string = "", dict = {}):
        if self.left != None:
            if self.left.char == "":
                self.left.huffman_map(string + "0", dict)
            if self.left.char != "":
                dict[self.left.char] = string + "0"
        if self.right != None:
            if self.right.char == "":
                self.right.huffman_map(string + "1", dict)
            if self.right.char != "":
                dict[self.right.char] = string + "1"
        return dict
    
    
                
            

