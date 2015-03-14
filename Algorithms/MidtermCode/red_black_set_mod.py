
# pylint: disable=C0302
# C0302: Unfortunately, we want a lot of lines in this module

# duplicate-code: We m4 preprocess this file into 2 or more versions, so
#   of course we have "duplicate" code.  But things aren't duplicated in
#   the m4.  Unfortunately, pylint doesn't allow us to override this
#   one, so we use a regex to this-pylint in addition to this disable.
# too-many-lines: We want something self-contained, so this has a lot of
#   lines

'''Red-Black tree and plain Binary Tree module'''

##Copyright (c) 2013 duncan g. smith and Dan Stromberg
##
##(This is the well-known MIT license)
##
##Permission is hereby granted, free of charge, to any person obtaining a
##copy of this software and associated documentation files (the "Software"),
##to deal in the Software without restriction, including without limitation
##the rights to use, copy, modify, merge, publish, distribute, sublicense,
##and/or sell copies of the Software, and to permit persons to whom the
##Software is furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included
##in all copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
##THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
##OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
##ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
##OTHER DEALINGS IN THE SOFTWARE.

# This code was originally by Duncan G. Smith, but has been modified a
# bit by Dan Stromberg.



from __future__ import division

import sys
import math
import random
import itertools

if hasattr(itertools, 'izip_longest'):
    MY_ZIP_LONGEST = getattr(itertools, 'izip_longest')
else:
    MY_ZIP_LONGEST = getattr(itertools, 'zip_longest')

try:
    next
except NameError:
    def next(iterator):
        # pylint: disable=redefined-builtin
        '''A version of next() for python's that don't have it'''
        return iterator.next()

#class TreeError(Exception):
#    '''An exception to raise if the tree gets in a bad state - unused'''
#    pass

def center(string, field_use_width, field_avail_width):
    '''Center a string within a given field width'''
    field_use = (string + '_' * (field_use_width - 1))[:field_use_width - 1]
    pad_width = (field_avail_width - len(field_use)) / 2.0
    result = ' ' * int(pad_width) + field_use + ' ' * int(math.ceil(pad_width))
    return result

class BinaryTree(object):
    # pylint: disable=too-many-public-methods,incomplete-protocol
    """
    A basic binary tree class.  Arbitrary data can be
    associated with a tree.  A tree that is root has
    parent equal to None; a tree that is leaf has left
    and right children that are empty trees (sentinels).
    An empty tree has left and right children equal to None.

    A tree can have children (or a parent) with equal
    data.
    """

    __slots__ = [ 'key', 'left', 'right', 'parent' ]

    def __init__(self, key=None, left=None, right=None, parent=None):
        """
        Initialises instance.

        @type     key: arbitrary type
        @param    key: data
        # placeholder
        # placeholder
        @type    left: L{BinaryTree} or C{None}
        @param   left: left child
        @type   right: L{BinaryTree} or C{None}
        @param  right: right child
        @type  parent: L{BinaryTree} or C{None}
        @param parent: parent
        """
        self.key = key
        # placeholder
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        """
        Returns a string representation of I{self}, containing
        the key in I{self} and left and right children.  If I{self}
        is a sentinel the string "sentinel" is returned.

        @rtype:  C{str}
        @return: string representation
        """
        if self:
            return '%s' % (self.key, )
        else:
            return "sent"

    def _depth_and_field_width(self):
        '''Compute the depth of the tree and the maximum width within the nodes - for pretty printing'''
        class maxer(object):
            '''Class facilitates computing the max depth of the treap (tree) and max width of the nodes'''
            def __init__(self, maximum=-1):
                self.depth_max = maximum
                self.field_width_max = -1

            def feed(self, node, key, depth, from_left):
                '''Check our maximums so far against the current node - updating as needed'''
                # pylint: disable=R0913
                # R0913: We need a bunch of arguments
                dummy = key
                # placeholder
                dummy = from_left
                if depth > self.depth_max:
                    self.depth_max = depth
                repr_node = repr(node)
                len_node = len(repr_node)
                if len_node > self.field_width_max:
                    self.field_width_max = len_node

            def result(self):
                '''Return the maximums we've computed'''
                return (self.depth_max + 1, self.field_width_max)

        max_obj = maxer()
        self.detailed_inorder_traversal(max_obj.feed)
        return max_obj.result()

    def to_dot(self, initial=True, file_=sys.stdout, visited=None):
        """Generate a dot file describing this tree"""

        if visited is None:
            visited = set()
        if initial:
            file_.write('digraph G {\n')
        this_node = '%s %s' % (id(self), repr(self))
        if this_node in visited:
            return
        visited.add(this_node)
        if self.left is not None:
            file_.write('   "%s" -> "%s %s" [ label="left" ]\n' % (this_node, id(self.left), repr(self.left)))
            self.left.to_dot(initial=False, file_=file_, visited=visited)
        if self.right is not None:
            file_.write('   "%s" -> "%s %s" [ label="right" ]\n' % (this_node, id(self.right), repr(self.right)))
            self.right.to_dot(initial=False, file_=file_, visited=visited)
        if initial:
            file_.write('}\n')

    def __str__(self):
        '''Format a tree as a string'''
        class Desc(object):
            # pylint: disable=R0903
            # R0903: We don't need a lot of public methods
            '''Build a pretty-print string during a recursive traversal'''
            def __init__(self, pretree):
                self.tree = pretree

            def update(self, node, key, depth, from_left):
                '''Add a node to the tree'''
                # pylint: disable=R0913
                # R0913: We need a bunch of arguments
                dummy = key
                # placeholder
                self.tree[depth][from_left] = repr(node)

        pretree = []
        depth, field_use_width = self._depth_and_field_width()
        field_use_width += 1
        for level in range(depth):
            string = '_' * (field_use_width - 1)
            pretree.append([string] * 2 ** level)
        desc = Desc(pretree)
        self.detailed_inorder_traversal(desc.update)
        result = []
        widest = 2 ** (depth - 1) * field_use_width
        for level in range(depth):
            two_level = 2 ** level
            field_avail_width = widest / two_level
            string = ''.join([center(x, field_use_width, field_avail_width) for x in desc.tree[level]])
            # this really isn't useful for more than dozen values or so
            result.append(('%2d ' % level) + string)
        return '\n'.join(result)

    def __nonzero__(self):
        """
        A sentinel node evaluates to False.

        @rtype:  C{bool}
        @return: True if neither left nor right are None,
                 otherwise False
        """
        return not (self.left is None and self.right is None)

    __bool__ = __nonzero__

    @property
    def is_root(self):
        """
        Returns True if I{self} is root.

        @rtype:  C{bool}
        @return: True if I{self} is root, otherwise False
        """
        return self.parent is None

    @property
    def sibling(self):
        """
        Returns the sibling of I{self}.

        @rtype:  L{BinaryTree} or C{None}
        @return: sibling
        """
        # sibling may be a sentinel node
        if self.is_root:
            return None
        elif self is self.parent.left:
            return self.parent.right
        else:
            return self.parent.left

    @property
    def size(self):
        """
        Return the number of key items / non-sentinel
        nodes in the subtree rooted at I{self}.

        @rtype:  C{int}
        @return: number of elements
        """
        if self:
            return self.left.size + self.right.size + 1
        return 0

    @property
    def num_levels(self):
        """
        Returns the number of levels in the subtree
        rooted at I{self}.

        @rtype:  C{int}
        @return: number of levels
        """
        if self:
            return max(self.left.num_levels, self.right.num_levels) + 1
        return 0

    @property
    def height(self):
        """
        Returns the height of the subtree rooted at
        I{self}.  This is the number of levels - 1.

        @rtype:  C{int}
        @return: number of levels
        """
        return self.num_levels - 1

    def copy(self, parent=None):
        """
        Returns a shallow copy of the subtree rooted
        at I{self} (does not copy data).

        @type  parent: L{BinaryTree} or C{None}
        @param parent: parent
        @rtype:        L{BinaryTree}
        @return:       a copy
        """
        if self:
            copy = self.__class__(key=self.key, parent=parent)
            copy.left = self.left.copy(copy)
            copy.right = self.right.copy(copy)
        else:
            copy = self.__class__(parent=parent)
        return copy

#    def copy(self, parent=None):
#        """
#        Returns a shallow copy of the subtree rooted
#        at I{self} (does not copy data).
#
#        @type  parent: L{BinaryTree} or C{None}
#        @param parent: parent
#        @rtype:        L{BinaryTree}
#        @return:       a copy
#        """
#        if self:
#            copy = self.__class__(self.data, parent=parent)
#            copy.left = self.left.copy(copy)
#            copy.right = self.right.copy(copy)
#        else:
#            copy = self.__class__(parent=parent)
#        return copy

    def del_node(self):
        """
        Deletes a node from the subtree rooted at I{self},
        but does not delete the subtree rooted at node.  To
        delete a node on the basis of its data use the
        I{remove} method.
        """
        if self.left:
            if self.right:
                # method chosen randomly in order to
                # prevent tree becoming too unbalanced
                if random.random() < 0.5:
                    node = self.left.maximum
                    self.key = node.key
                    # placeholder
                    node.del_node()
                else:
                    node = self.right.minimum
                    self.key = node.key
                    # placeholder
                    node.del_node()
            else:
                node = self.left
                self.key, self.left, self.right = node.key, node.left, node.right
                # placeholder
                self.left.parent = self
                self.right.parent = self
        elif self.right:
            node = self.right
            self.key, self.left, self.right = node.key, node.left, node.right
            # placeholder
            self.left.parent = self
            self.right.parent = self
        else:
            # make node a sentinel node
            self.key = self.left = self.right = None
            # placeholder

    def add(self, key):
        """
        Adds a node containing I{key} to the subtree
        rooted at I{self}, returning the added node.

        @type  key: arbitrary type
        @param key: key
        placeholder
        placeholder
        @rtype:      L{BinaryTree}
        @return:     (replaced flag, added node)
        """
        node, count = self.findNCount(key)
        if not node:
            node.key = key
            # placeholder
            node.left, node.right = self.__class__(parent=node), self.__class__(parent=node)
            return (False, node, count)
        elif node.key == key:
            node.key = key
            # placeholder
            return (True, node, count)
        else:
            if random.random() < 0.5:
                return BinaryTree.add(node.left, key=key)
            else:
                return BinaryTree.add(node.right, key=key)

    def remove(self, key):
        """
        Removes a node containing I{key} from the
        subtree rooted at I{self}, raising an error
        if the subtree does not contain I{key}.

        @type        key: arbitrary type
        @param       key: data
        @raise ValueError: if key is not contained in the
                           subtree rooted at I{self}
        """
        node, count = self.findNCount(key)
        if node:
            node.del_node()           
        else:
            raise ValueError('tree.remove(x): x not in tree')
        return count

    def discard(self, key):
        """
        Discards a node containing I{key} from the subtree
        rooted at I{self} (without raising an error if the key
        is not present).

        @type  key: arbitrary type
        @param key: data
        """
        try:
            count = self.remove(key)
        except ValueError:
            pass
        return count

    def count(self, key):
        """
        Returns the number of occurrences of I{key} in
        the subtree rooted at I{self}.

        @type  key: arbitrary type
        @param key: data
        @rtype:      C{int}
        @return:     data count
        """
        if self:
            node = self.find(key)
            if node:
                return node.left.count(key) + node.right.count(key) + 1
        return 0

    def __add__(self, iterable):
        """
        Returns a tree with elements from the subtree
        rooted at I{self} and I{iterable}.  I{iterable}
        may be any iterable, not necessarily another
        tree.

        @type  iterable: any iterable type
        @param iterable: an iterable object
        @rtype:          L{BinaryTree}
        @return:         tree containing the elements in I{self}
                         and iterable
        """
        items = list(self) + list(iterable)
        random.shuffle(items)  # try to avoid unbalanced tree
        tree = self.__class__()
        for item in items:
            tree.add(item)
        return tree

    def __iadd__(self, iterable):
        """
        Adds the elements in I{iterable} to the
        subtree rooted at I{self}.

        @type  iterable: any iterable type
        @param iterable: an iterable object
        """
        items = list(iterable)
        random.shuffle(items)  # try to avoid unbalanced tree
        for item in items:
            self.add(item)

    def find(self, key):
        """
        Finds and returns a node containing I{key} in the
        subtree rooted at I{self}.  If I{key} is not in
        the tree, then a sentinel in the location where
        I{key} can be inserted is returned.

        @type  key: arbitrary type
        @param key: data
        @rtype:      L{BinaryTree}
        @return:     node containing key, or sentinel
                     node
        """
        if self:
            if self.key == key:
                return self
            elif key < self.key:
                return self.left.find(key)
            else:
                return self.right.find(key)
        return self
    
    def findNCount(self, key, count = 0):
        """
        Finds and returns a node containing I{key} in the
        subtree rooted at I{self}.  If I{key} is not in
        the tree, then a sentinel in the location where
        I{key} can be inserted is returned.

        @type  key: arbitrary type
        @param key: data
        @rtype:      L{BinaryTree}
        @return:     node containing key, or sentinel
                     node
        """
        if self:
            count += 1
            if self.key == key:
                return self, count +1
            elif key < self.key:
                return self.left.findNCount(key, count)
            else:
                return self.right.findNCount(key, count)
        return self, count

    @property
    def predecessor(self):
        """
        Returns the predecessor of I{self}, or None if
        self has no predecessor.
        
        @rtype:  L{BinaryTree} or None
        @return: predecessor of I{self}
        """
        if self.left:
            return self.left.maximum
        else:
            if not self.parent:
                return None
            if self is self.parent.right:
                return self.parent
            else:
                current, parent = self, self.parent
                while parent and parent.left is current:
                    current, parent = parent, parent.parent
                return parent

    @property
    def successor(self):
        """
        Returns the successor of I{self}, or None if
        self has no successor.
        
        @rtype:  L{BinaryTree} or None
        @return: successor of I{self}
        """
        if self.right:
            return self.right.minimum
        else:
            if not self.parent:
                return None
            if self is self.parent.left:
                return self.parent
            else:
                current, parent = self, self.parent
                while parent and parent.right is current:
                    current, parent = parent, parent.parent
                return parent

    def in_order(self):
        """
        Returns a generator of nodes in the subtree
        rooted at I{self} in sorted order of node keys.

        @rtype:  C{generator}
        @return: generator of sorted nodes
        """
        if self:
            for node in self.left.in_order():
                yield node
            yield self
            for node in self.right.in_order():
                yield node

    def detailed_inorder_traversal(self, visit, depth=0, from_left=0):
        '''Do an inorder traversal - with lots of parameters'''
        if self.left:
            self.left.detailed_inorder_traversal(visit, depth + 1, from_left * 2)
        visit(self, self.key, depth, from_left)
        if self.right:
            self.right.detailed_inorder_traversal(visit, depth + 1, from_left * 2 + 1)

    def __iter__(self):
        """
        Returns a generator of the node keys in
        the subtree rooted at I{self} in sorted
        order.

        @rtype:  C{generator}
        @return: generator of sorted node values
        """
        return (n.key for n in self.in_order())

    def in_reverse(self):
        """
        Returns a generator of nodes in the subtree
        rooted at I{self} in reverse sorted order
        of node keys.

        @rtype:  C{generator}
        @return: generator of reverse sorted nodes
        """
        if self:
            for node in self.right.in_reverse():
                yield node
            yield self
            for node in self.left.in_reverse():
                yield node

    def pre_order(self):
        """
        Returns a generator of the nodes in the
        subtree rooted at I{self} in preorder.

        @rtype:  C{generator}
        @return: generator of nodes in preorder
        """
        if self:
            yield self
            for node in self.left.pre_order():
                yield node
            for node in self.right.pre_order():
                yield node

    def post_order(self):
        """
        Returns a generator of the nodes in the
        subtree rooted at I{self} in postorder.

        @rtype:  C{generator}
        @return: generator of nodes in postorder
        """
        if self:
            for node in self.left.post_order():
                yield node
            for node in self.right.post_order():
                yield node
            yield self

    @property
    def minimum(self):
        """
        Returns a node for which the node key is minimum
        in the subtree rooted at I{self}.  Always returns
        the minimum-valued node with no left child.

        @rtype:  L{BinaryTree}
        @return: node with minimum key value
        """
        node = self
        while node.left:
            node = node.left
        return node

    @property
    def maximum(self):
        """
        Returns a node for which the node key is maximum
        in the subtree rooted at I{self}.  Always returns
        the maximum-valued node with no right child.

        @rtype:  L{BinaryTree}
        @return: node with maximum key value
        """
        node = self
        while node.right:
            node = node.right
        return node

    def is_similar(self, other):
        """
        Two binary trees are similar if they have the
        same structure.

        @rtype:  C{bool}
        @return: True if the subtrees rooted at I{self}
                 and I{other} are similar, otherwise False
        """
        if not self and not other:
            return True
        if self and other:
            return self.left.is_similar(other.left) and self.right.is_similar(other.right)
        return False

    def is_equivalent(self, other):
        """
        Two binary trees are equivalent if they are similar
        and corresponding nodes contain the same keys.

        @rtype:  C{bool}
        @return: True if the subtrees rooted at I{self}
                 and I{other} are equivalent, otherwise False
        """
        if not self and not other:
            return True
        if self and other:
            return (self.key == other.key and
                # placeholder
                self.left.is_equivalent(other.left) and
                self.right.is_equivalent(other.right))
        return False

#    def cmp(self, other):
#        """
#        Compares I{self} with I{other} lexocographically.
#
#        @type  other: L{BinaryTree}
#        @param other: tree being compared to I{self}
#        @rtype:       C{int}
#        @return:      0 if the subtrees rooted at I{self}
#                      and I{other} contain equal values,
#                      -1 if the ordered values in I{self} are lexicographically
#                      less than the ordered values in I{other}, and
#                      1 if the ordered values in I{self} are lexicographically
#                      greater than the ordered values in I{other}
#        """
#        other_items = iter(other)
#        for self_item in self:
#            try:
#                other_item = next(other_items)
#            except StopIteration:
#                return 1
#            else:
#                if self_item < other_item:
#                    return -1
#                elif self_item > other_item:
#                    return 1
#        try:
#            next(other_items)
#        except StopIteration:
#            return 0

    def __cmp__(self, other):
        """
        Returns C{0} if the subtrees rooted at
        I{self} and I{other} contain equal keys.
        I{other} need not be similar to I{self}.

        @type  other: L{BinaryTree}
        @param other: tree being compared to I{self}
        @rtype:       C{int}
        @return:      0 if the subtrees rooted at I{self}
                      and I{other} do contain equal values,
                      -1 if self < other.
                      1 if self > other.
        """
        # FIXME: This probably should compare values too.
        for self_node, other_node in MY_ZIP_LONGEST(self.in_order(), other.in_order()):
            if self_node is None:
                return -1
            elif other_node is None:
                return 1
            elif self_node.key < other_node.key:
                return -1
            elif self_node.key > other_node.key:
                return 1
        return 0
        
    cmp = __cmp__

    def __eq__(self, other):
        """
        Returns C{True} if the subtrees rooted at
        I{self} and I{other} contain equal keys.
        I{other} need not be similar to I{self}.

        @type  other: L{BinaryTree}
        @param other: tree being compared to I{self}
        @rtype:       C{bool}
        @return:      True if the subtrees rooted at I{self}
                      and I{other} contain equal values, otherwise
                      False
        """
        return self.cmp(other) == 0

    def __neq__(self, other):
        """
        Returns C{True} if the subtrees rooted at
        I{self} and I{other} do not contain equal keys.
        I{other} need not be similar to I{self}.

        @type  other: L{BinaryTree}
        @param other: tree being compared to I{self}
        @rtype:       C{bool}
        @return:      True if the subtrees rooted at I{self}
                      and I{other} do not contain equal values,
                      otherwise False
        """
        return self.cmp(other) != 0

    def __lt__(self, other):
        """
        Returns C{True} if the subtrees rooted at
        I{self} and I{other} do not contain equal keys.
        I{other} need not be similar to I{self}.

        @type  other: L{BinaryTree}
        @param other: tree being compared to I{self}
        @rtype:       C{bool}
        @return:      True if the subtrees rooted at I{self}
                      and I{other} do not contain equal values,
                      otherwise False
        """
        return self.cmp(other) < 0

    def __gt__(self, other):
        return other.cmp(self) < 0

    def __le__(self, other):
        return self.cmp(other) <= 0

    def __ge__(self, other):
        return self.cmp(other) >= 0

    def __contains__(self, key):
        """
        Returns true if I{key} is stored in any node in
        the subtree rooted at I{self}.

        @type  key: arbitrary type
        @param key: data
        @rtype:      C{bool}
        @return:     True if I{key} in subtree rooted at
                     I{self}, otherwise False
        """
        return bool(self.find(key))


class RedBlackTree(BinaryTree):
    # pylint: disable=attribute-defined-outside-init,maybe-no-member,too-many-public-methods,incomplete-protocol
    """
    A binary tree with an extra attribute, is_red.  Colour (red
    or black) is used to maintain a reasonably balanced tree.
    Changes to the tree structure (rotations) are carried out
    in such a way that the name bound to the initial empty
    tree will always refer to the root node.  The data stored
    in a given node may change, as well as its connectivity.
    e.g.

    >>> import trees
    >>> tree = trees.RedBlackTree()
    >>> tree.add(2)
    2 False None None
    >>> tree.key        # tree is bound to root node
    2
    >>> tree.add(-1)
    -1 True None None
    >>> tree.add(1)     # tree rotations are performed at this point
    1 False -1 2
    >>> tree.key        # the root node has changed (i.e. its key has been changed)
    1
    >>> 
    
    """

    __slots__ = BinaryTree.__slots__ + [ 'is_red' ]

    def __init__(self, key=None, left=None, right=None, parent=None):
        """
        Initialises instance.

        @type     key: arbitrary type
        @param    key: data
        @type    left: L{RedBlackTree} or C{None}
        @param   left: left child
        @type   right: L{RedBlackTree} or C{None}
        @param  right: right child
        @type  parent: L{RedBlackTree} or C{None}
        @param parent: parent
        """
        super(RedBlackTree, self).__init__(key, left, right, parent)
        self.is_red = False  # default for sentinel nodes

    @property
    def is_black(self):
        """
        Returns True if node colour is black.

        @rtype:  C{bool}
        @return: True if node colour is black, otherwise False
        """
        return not self.is_red

    @is_black.setter
    def is_black(self, val):
        """
        Sets node colour.
        """
        self.is_red = not val

    @property
    def black_height(self):
        """
        @rtype:  C{int}
        @return: black height of subtree rooted at I{self}
        """
        if self.left:
            if self.left.is_black:
                return self.left.black_height + 1
            else:
                return self.left.black_height
        elif self.right:
            if self.right.is_black:
                return self.right.black_height + 1
            else:
                return self.right.black_height
        else:
            return 0

    def __repr__(self):
        """
        Returns a string representation of I{self}, containing
        the key in I{self}, the colour, and the key in left and
        right children.  If I{self} is a sentinel the string
        "sentinel" is returned.

        @rtype:  C{str}
        @return: string representation
        """
        if self:
            if self.is_red:
                color_string = 'red'
            else:
                color_string = 'blk'
            return '%s %s' % (self.key, color_string)
        else:
            return "sent"

    def copy(self, parent=None):
        """
        Returns a shallow copy of the subtree rooted
        at I{self} (does not copy key).

        @type  parent: L{RedBlackTree} or C{None}
        @param parent: parent
        @rtype:        L{RedBlackTree}
        @return:       a copy
        """
        copy = super(RedBlackTree, self).copy(parent)
        copy.is_red = self.is_red
        return copy

    def add(self, key):
        """
        Adds a node containing I{key} to the subtree
        rooted at I{self}, returning the node which
        contains I{key}.  Note: the returned node might
        be an existing node due to key swaps on rotations.

        @type  key: arbitrary type
        @param key: data
        @rtype:      L{RedBlackTree}
        @return:     node containing I{key}
        """
        (replaced, node, count) = super(RedBlackTree, self).add(key=key)
        if not replaced:
            node.is_red = True
            node = node.fix_insert()
        return node, count

    def fix_insert(self):
        """
        Carries out tree rotations, key swaps and recolourings
        to ensure that the red / black properties of the tree
        are preserved on node insertion. The returned node contains
        the same value as I{self} (but might not be the inserted node
        due to key swaps / rotations).

        @rtype:  L{RedBlackTree}
        @return: node containing key originally
                 contained in I{self}
        """
        # case 1
        if self.parent is None:
            self.is_black = True
            return self
        # case 2
        if self.parent.is_black:
            return self
        # case 3
        sib = self.parent.sibling
        if sib.is_red:
            self.parent.is_black = True
            sib.is_black = True
            par = self.parent.parent
            par.is_red = True
            par.fix_insert()
            return self
        # cases 4 & 5
        par = self.parent.parent
        if not (self.parent.left is self) == (par.left is self.parent):
            self.rotate()
            self.parent.rotate()
            return par
        else:
            self.parent.rotate()
            return self

    def rotate(self):
        """
        Rotates I{self} with I{self.parent}.  Left / right rotations
        are performed as dictated by the parent-child relationship.
        The colours of I{self} and I{self.parent} are implicity swapped
        (as their values are swapped during the rotation).
        """
        # data swapped and connections updated
        # colours are (implicitly) swapped
        if self is self.parent.left:
            self.key, self.parent.key = self.parent.key, self.key
            # placeholder
            self.parent.left = self.left
            self.parent.left.parent = self.parent
            self.left = self.right
            self.right = self.parent.right
            self.left.parent = self.right.parent = self
            self.parent.right = self
        else:
            self.key, self.parent.key = self.parent.key, self.key
            # placeholder
            self.parent.right = self.right
            self.parent.right.parent = self.parent
            self.right = self.left
            self.left = self.parent.left
            self.left.parent = self.right.parent = self
            self.parent.left = self

    def del_node(self):
        """
        Deletes a node from the subtree rooted at I{self},
        but does not delete the subtree rooted at node.  To
        delete a node on the basis of its key use the
        I{remove} method.
        """
        # ensure that node being deleted has at most one child
        if self.left:
            if self.right:
                # method chosen randomly in order to
                # prevent tree becoming too unbalanced
                if random.random() < 0.5:
                    node = self.left.maximum
                else:
                    node = self.right.minimum
                self.key, node.key = node.key, self.key
                # placeholder
                node.del_node()  # node has at most one child  
            else:
                node = self.left
                self.key, self.left, self.right = node.key, node.left, node.right
                # placeholder
                self.left.parent = self  # this might result in sentinel node's parent attribute being set
                self.right.parent = self
                self.is_black = True
        elif self.right:
            node = self.right
            self.key, self.left, self.right = node.key, node.left, node.right
            # placeholder
            self.left.parent = self
            self.right.parent = self
            self.is_black = True
        else:
            # node being deleted is leaf
            self.key = self.left = self.right = None
            # placeholder
            if self.is_red:# or self.sibling:  # just make it a sentinel node
                self.is_black = True
            else:
                self.is_black = True
                # self has extra blackness
                self.fix_del()

    def fix_del(self):
        """
        Maintains red / black property on node
        deletion.
        """
        # case 1
        if self.parent is None:
            return
        sib = self.sibling
        # case 2
        if sib.is_red:
            sib.rotate()
            sib = self.sibling
        # case 3
        if (self.parent.is_black and sib.is_black and
            sib.left.is_black and sib.right.is_black):
            sib.is_red = True
            self.parent.fix_del()
            return
        # case 4
        if (self.parent.is_red and sib.is_black and
            sib.left.is_black and sib.right.is_black):
            sib.is_red = True
            self.parent.is_black = True
            return
        # case 5
        if sib.is_black:
            if self is self.parent.left and sib.right.is_black and sib.left.is_red:
                sib.left.rotate()
            elif self is self.parent.right and sib.left.is_black and sib.right.is_red:
                sib.right.rotate()
            sib = self.sibling
        # case 6
        sib.rotate()
        self.parent.sibling.is_black = True

    def check(self):
        """
        Checks whether the subtree rooted at I{self} is a valid
        red black tree U{http://en.wikipedia.org/wiki/Red_black_tree}.

        @rtype:  C{bool}
        @return: True if the tree is valid, otherwise False
        """
        leaf_nodes = []
        for node in self.in_order():
            if not node.left and not node.right:
                leaf_nodes.append(node)
            if node.is_red:
                if not (node.left.is_black and node.right.is_black):
                    return False
        black_height = 0
        if leaf_nodes:
            node = leaf_nodes[0]
            while node.parent:
                if node.is_black:
                    black_height += 1
                node = node.parent
            for node in leaf_nodes[1:]:
                height = 0
                while node.parent:
                    if node.is_black:
                        height += 1
                    node = node.parent
                if not height == black_height:
                    return False
        return True

    # placeholder
        # placeholder

        # placeholder
        # placeholder
            # placeholder
        # placeholder
            # placeholder

    # placeholder
        # placeholder

        # placeholder

    # placeholder
        # placeholder

        # placeholder
        # placeholder
            # placeholder
        # placeholder
            # placeholder

    # placeholder
        # placeholder

        # placeholder

    # placeholder
        # placeholder

        # placeholder

    def __len__(self):
        '''Return the number of elements in the container'''

        return self.size

