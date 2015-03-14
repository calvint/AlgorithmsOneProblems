class Node:
    """
    Tree node: left and right child + data which can be any object
    """
    def __init__(self, data, parent = None):
        """
        Node constructor

        @param data node data object
        """
        self.parent = parent
        self.left = None
        self.right = None
        self.data = data
        self.count = 1
    
    def checkThenInsert(self, data, root, compares = 0):
        node, parent, compares = self.lookup(data)
        if node != None:
            return compares, 0, root
        else:
            return self.insert(data, root, compares)
    
    def insert(self, data, root, compares = 0):
        """
        Insert new node with data

        @param data node data object to insert
        """
        
        self.count += 1
        if data < self.data:
            if self.left is None:
                self.left = Node(data, self)
                rotates, root = self.left.checkForRotates(root)
                return compares +1, rotates, root
            else:
                return self.left.insert(data, root, compares + 1)
        elif data > self.data:
            if self.right is None:
                self.right = Node(data, self)
                rotates, root = self.right.checkForRotates(root)
                return compares + 1, rotates, root
            else:
                return self.right.insert(data, root, compares + 2)
        else:
            return compares +1, 0, root

    def lookup(self, data, parent=None, comparesNum = 0):
        """
        Lookup node containing data

        @param data node data object to look up
        @param parent node's parent
        @returns node and node's parent if found or None, None
        """
        if data < self.data:
            if self.left is None:
                return None, None, comparesNum +1
            return self.left.lookup(data, self, comparesNum +1)
        elif data > self.data:
            if self.right is None:
                return None, None, comparesNum +2
            return self.right.lookup(data, self, comparesNum +2)
        else:
            return self, parent, comparesNum +2
    
    def subtractOneFromParents(self):
        self.count -= 1
        if self.parent != None:
            self.parent.subtractOneFromParents()
    
    def checkForRotates(self, root):
        rotates = 0
        if self.parent != None and str(self.parent) != "None":
            if self.parent.right == self:
                if self.parent.left != None and self.parent.left.left != None:
                    if self.parent.left.left.count > self.count:
                        root = self.parent.left.rotate_right(root)
                        rotates +=1
                if self.parent.parent != None and self.parent == self.parent.parent.right and self.parent.parent.left != None:
                    if self.parent.parent.left.count < self.count:
                        root = self.parent.rotate_left(root)
                        rotates +=1
            if self.parent.left == self:
                if self.parent.right != None and self.parent.right.right != None:
                    if self.parent.right.right.count > self.count:
                        root = self.parent.right.rotate_left(root)
                        rotates +=1
#                 print "***" + str(self) + "***" + str(self.parent) + "***\n"
                if self.parent.parent != None and self.parent == self.parent.parent.left and self.parent.parent.right != None:
                    if self.parent.parent.right.count < self.count:
                        root = self.parent.rotate_right(root)
                        rotates +=1
            moreRotates, root = self.parent.checkForRotates(root)
            return rotates + moreRotates, root
        else:
            return rotates, root
    
    def delete(self, data, root):
        """
        Delete node containing data

        @param data node's content to delete
        """
        # get node containing data
        node, parent, count = self.lookup(data)
        rotates = 0
        string = str(node)
        if string != "None":
            children_count = node.children_count()
            if children_count == 0:
                node.parent.subtractOneFromParents()
                rotates, root = node.parent.checkForRotates(root)
                # if node has no children, just remove it
                if parent.left is node:
                    parent.left = None
                else:
                    parent.right = None
                del node
            elif children_count == 1:
                node.parent.subtractOneFromParents()
                rotates, root = node.parent.checkForRotates(root)
                # if node has 1 child
                # replace node by its child
                if node.left:
                    n = node.left
                else:
                    n = node.right
                if parent:
                    if parent.left is node:
                        parent.left = n
                    else:
                        parent.right = n
                del node
            else:
                # if node has 2 children
                # find its successor
                parent = node
                successor = node.right
                while successor.left:
                    parent = successor
                    successor = successor.left
                # replace node data by its successor data
                node.data = successor.data
                # fix successor's parent node child
                if parent.left == successor:
                    parent.left = successor.right
                else:
                    parent.right = successor.right
                parent.subtractOneFromParents()
                rotates, root = parent.checkForRotates(root)
            return count, rotates, root
        else:
            return 0, 0, root

    def compare_trees(self, node):
        """
        Compare 2 trees

        @param node tree to compare
        @returns True if the tree passed is identical to this tree
        """
        if node is None:
            return False
        if self.data != node.data:
            return False
        res = True
        if self.left is None:
            if node.left:
                return False
        else:
            res = self.left.compare_trees(node.left)
        if res is False:
            return False
        if self.right is None:
            if node.right:
                return False
        else:
            res = self.right.compare_trees(node.right)
        return res
                
    def print_tree(self):
        """
        Print tree content inorder
        """
        if self.left:
            self.left.print_tree()
        print self.data,
        if self.right:
            self.right.print_tree()

    def print_tree2(self):
        """
        Print tree content in tree order
        """
        print self.data,
        print ' l ',
        if self.left:
            self.left.print_tree2()
        print ' r ',
        if self.right:
            self.right.print_tree2()

    def tree_data(self):
        """
        Generator to get the tree nodes data
        """
        # we use a stack to traverse the tree in a non-recursive way
        stack = []
        node = self
        while stack or node: 
            if node:
                stack.append(node)
                node = node.left
            else: # we are returning so we pop the node and we yield it
                node = stack.pop()
                yield node.data
                node = node.right

    def children_count(self):
        """
        Return the number of children

        @returns number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt
    
#     def rotate_right(self, parent, root):
    def rotate_right(self, root):
        """
        During the right rotation:
            a is decreased by b-e,
            b is increased by a-b,
            c, d, e, f, g are left alone 
        """
        parent = self.parent
        if self.right != None:
            oldCount = self.count - self.right.count
            self.right.parent = parent
        else:
            oldCount = self.count
        self.count += (parent.count - self.count)
        parent.count -= oldCount
        parent.left = self.right;
        self.parent = parent.parent
        if parent.parent != None:
            if parent.parent.left == parent:
                parent.parent.left = self
            else:
                parent.parent.right = self
        self.right  = parent;
        parent.parent = self
        if root == parent:
            return self;
        return root;
            

#         def rotate_left(self, parent, root):
    def rotate_left(self, root):
        """
        During the left rotation:
            a is decreased by c-f,
            c is increased by a-c,
            b, d, e, f, and g are left alone.
        """
        parent = self.parent
        if self.left != None:
            oldCount = self.count - self.left.count
            self.left.parent = parent
        else:
            oldCount = self.count
        self.count += (parent.count - self.count)
        parent.count -= oldCount
        parent.right = self.left
        self.parent = parent.parent
        if parent.parent != None:
            if parent.parent.left == parent:
                parent.parent.left = self
            else:
                parent.parent.right = self
        parent.parent = self
        self.left  = parent
        if root == parent:
            return self;
        return root;