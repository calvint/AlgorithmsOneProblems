#!/usr/bin/python

'''Test the red black tree module, plus a little test of the plain binary tree'''

# import sys
# import pprint

import red_black_set_mod
import red_black_dict_mod

def test_tree():
    '''Test the plain binary tree'''
    tree = red_black_set_mod.BinaryTree()
    items = [6, 3, 9, 14, 7, 5, 13, 2, 1, 10]
    for item in items:
        tree.add(item)
    return tree

def test_entire_tree_ops(tree, acopy):
    '''check copy() and comparisons'''

    all_good = True

    # Interesting: for a while, tree == acopy, but tree also != acopy
    if not (tree == acopy):
        sys.stderr.write('%s: test_entire_tree_ops: not (tree == acopy) (1)\n' % (sys.argv[0],))
        print(tree)
        print(acopy)
        all_good = False
        
    if tree != acopy:
        sys.stderr.write('%s: test_entire_tree_ops: tree != acopy (1)\n' % (sys.argv[0],))
        print(tree)
        print(acopy)
        all_good = False
        
    if not tree.is_similar(acopy):
        sys.stderr.write('%s: test_entire_tree_ops: not tree.is_similar(acopy)\n' % (sys.argv[0],))
        all_good = False

    if not tree.is_equivalent(acopy):
        sys.stderr.write('%s: test_entire_tree_ops: not tree.is_equivalent(acopy)\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_adding(tree, acopy):
    '''check adding and deleting nodes'''
    all_good = True

    acopy.add(101)
    if tree == acopy:
        sys.stderr.write('%s: test_adding: tree == acopy, but should not\n' % (sys.argv[0],))
        all_good = False

    if tree.is_similar(acopy):
        sys.stderr.write('%s: test_adding: tree.is_similar(acopy), but should not be\n' % (sys.argv[0],))
        all_good = False
        
    if tree.is_equivalent(acopy):
        sys.stderr.write('%s: test_adding: tree.is_equivalent(acopy), but should not be\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_tree_list_and_del_node(tree, acopy):
    '''check tree + list and del_node'''
    all_good = True

    new_tree = tree + [ 101 ]
    if new_tree != acopy:
        sys.stderr.write('%s: test_tree_plus_list_and_del_node: new_tree != acopy\n' % (sys.argv[0],))
        print(new_tree)
        print(acopy)
        all_good = False

    acopy.find(101).del_node()
    if tree != acopy:
        sys.stderr.write('%s: test_tree_plus_list_and_del_node: tree != acopy (2)\n' % (sys.argv[0],))
        print(new_tree)
        print(acopy)
        all_good = False

    return all_good

def test_in(tree):
    '''check 'in'''
    all_good = True

    if 14 not in tree:
        sys.stderr.write('%s: test_in: 14 not in tree\n' % (sys.argv[0],))
        all_good = False
        
    if 27 in tree:
        sys.stderr.write('%s: test_in: 27 in tree\n' % (sys.argv[0],))
        all_good = False

    return all_good
        

def test_min_and_max(tree):
    '''check minimum() and maximum()'''
    all_good = True

    if tree.minimum.key != 0:
        sys.stderr.write('%s: test_min_and_max: min is not -1\n' % (sys.argv[0],))
        all_good = False
        
    if tree.maximum.key != 17:
        sys.stderr.write('%s: test_min_and_max: max is not 17\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_contains_and_find(tree):
    '''check __contains__() and find()'''
    all_good = True

    if tree.find(8).key != 8:
        sys.stderr.write('%s: test_contains_and_find: member 8 is not 8\n' % (sys.argv[0],))
        all_good = False

    if 8 not in tree:
        sys.stderr.write('%s: test_contains_and_find: 8 not in tree\n' % (sys.argv[0],))
        all_good = False
        
    if tree.find(-23):
        sys.stderr.write('%s: test_contains_and_find: -23 mistakenly found in tree\n' % (sys.argv[0],))
        all_good = False
        
    if -23 in tree:
        sys.stderr.write('%s: test_contains_and_find: -23 mistakenly in tree\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_in_order(tree, items):
    '''check in_order()'''
    all_good = True

    items.sort()

    if items != [node.key for node in tree.in_order()]:
        sys.stderr.write('%s: test_in_order: items != in_order traversal\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_pred_and_succ(items, tree):
    '''check predecessor and successor'''
    all_good = True

    items.remove(8)
    tree.remove(8)
    for i in range(len(items) - 1):
        if tree.find(items[i+1]).predecessor.key != items[i]:
            sys.stderr.write('%s: predecessor problem\n' % (sys.argv[0],))
            all_good = False

        if tree.find(items[i]).successor.key != items[i+1]:
            sys.stderr.write('%s: successor problem\n' % (sys.argv[0],))
            all_good = False
            
    if tree.find(items[0]).predecessor is not None:
        sys.stderr.write('%s: nonexistent predecessor problem\n' % (sys.argv[0],))
        all_good = False

    if tree.find(items[-1]).successor is not None:
        sys.stderr.write('%s: nonexistent successor problem\n' % (sys.argv[0],))
        all_good = False

    return all_good

def test_check(tree):
    '''Test tree invariants'''
    all_good = True

    if tree.check() != True:
        sys.stderr.write('%s: test_check: tree does not check out ok\n' % (sys.argv[0],))
        all_good = False

    return all_good
    
def test_uniquing():
    '''Test set with uniquing property'''
    all_good = True

    tree = red_black_set_mod.RedBlackTree()

    list_ = list(range(10)) + list(range(-5, 5)) + list(range(5, 15))
    for value in list_:
        tree.add(value)

        if tree.check() != True:
            sys.stderr.write('%s: test_uniquing: tree does not check out ok\n' % (sys.argv[0],))
            all_good = False
            return False

    set_ = set(list_)
    list_ = list(set_)
    list_.sort()

    list_of_tree = list(tree)
    if list_ != list_of_tree:
        sys.stderr.write('%s: test_uniquing: unique values are not correct\n' % (sys.argv[0],))
        print(list_)
        print(list_of_tree)
        all_good = False
        
    return all_good

def test_similar():
    '''Test adding to a dictionary'''

    all_good = True

    dict_ = red_black_set_mod.RedBlackTree()
    for integer in range(5):
        dict_.add(integer)

    return all_good
        
    
def test_dict_add():
    '''Test adding to a dictionary'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()
    for integer in range(5):
        dict_.add(key=integer, value=2**integer)

    return all_good
        
def test_dict_find():
    '''Test adding to a dictionary'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()
    for integer in range(5):
        dict_.add(key=integer, value=2**integer)

    found_key = dict_.find(3).key

    if found_key != 3:
        sys.stderr.write('%s: test_dict_find: 3th element is not 3, instead got %s\n' % (sys.argv[0], found_key))
        all_good = False

    return all_good
        
    
def test_dict_setitem():
    '''Test dictionary-like operation: __setitem__'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()

    for number in range(10):
        dict_[number] = 2**number

    if len(dict_) != 10:
        sys.stderr.write('%s: test_dict_setitem: len(dict_) is not 10\n' % (sys.argv[0], ))
        all_good = False

    return all_good


def test_dict_getitem():
    '''Test dictionary-like operation: __getitem__'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()

    for number in range(10):
        dict_[number] = 2**number

    value = dict_[0]
    if value != 1:
        sys.stderr.write('%s: test_dict_getitem: 0th element of dict_ is not 1, instead got %s\n' % (sys.argv[0], value))
        all_good = False

    value = dict_[2]
    if value != 4:
        sys.stderr.write('%s: test_dict_getitem: 2nd element of dict_ is not 4, instead got %s\n' % (sys.argv[0], value))
        all_good = False

    value = dict_[9]
    if value != 512:
        sys.stderr.write('%s: test_dict_getitem: 9th element of dict_ is not 512, instead got %s\n' % (sys.argv[0], value))
        all_good = False

    return all_good

def test_dict_delitem():
    '''Test dictionary-like operation: __delitem__'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()

    for number in range(10):
        dict_[number] = 2**number

    for number in range(0, 10, 2):
        del dict_[number]

    if len(dict_) != 5:
        sys.stderr.write('%s: test_dict_delitem: len(dict_) is not 5\n' % (sys.argv[0], ))
        all_good = False

    if dict_[1] != 2:
        sys.stderr.write('%s: test_dict_delitem: 1th element of dict_ is not 2\n' % (sys.argv[0], ))
        all_good = False

    if dict_[9] != 512:
        sys.stderr.write('%s: test_dict_delitem: 9th element of dict_ is not 512\n' % (sys.argv[0], ))
        all_good = False

    return all_good

def test_dict_iteritems():
    '''Test dictionary-like operation: __iteritems__'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()
    list_ = []

    for number in range(10):
        dict_[number] = 2**number
        list_.append((number, 2**number))

    if list(dict_.iteritems()) != list_:
        sys.stderr.write('%s: test_dict_iteritems: dict_.iteritems() != list_\n' % (sys.argv[0], ))
        all_good = False
        
    return all_good

def test_dict_itervalues():
    '''Test dictionary-like operation: __itervalues__'''

    all_good = True

    dict_ = red_black_dict_mod.RedBlackTree()
    list_ = []

    for number in range(10):
        dict_[number] = 2**number
        list_.append(2**number)

    if list(dict_.itervalues()) != list_:
        sys.stderr.write('%s: test_dict_itervalues: dict_.itervalues() != list_\n' % (sys.argv[0], ))
        all_good = False
        
    return all_good

def test_successor():
    '''Test the successor property'''

    all_good = True

    # create a "dictionary" without duplicates
    dict_ = red_black_dict_mod.RedBlackTree()
    expected_keys = []
    expected_values = []
    for i in range(10):
        dict_[i] = 2 ** i
        expected_keys.append(i)
        expected_values.append(2 ** i)
#    for i in range(10):
#        dict_[i] = 2 ** i

    expected_keys.sort()
    expected_values.sort()

    keys_list = []
    values_list = []

    node = dict_.find(0)
    while node is not None:
        keys_list.append(node.key)
        values_list.append(node.value)
        node = node.successor

    if keys_list != expected_keys:
        sys.stderr.write('%s: test_successor: keys_list != expected_keys\n' % (sys.argv[0], ))
        sys.stderr.write('keys_list:\n%s\n' % (pprint.pformat(keys_list)))
        sys.stderr.write('exected_keys:\n%s\n' % (pprint.pformat(expected_keys)))
        all_good = False

    if values_list != expected_values:
        sys.stderr.write('%s: test_successor: values_list != expected_values\n' % (sys.argv[0], ))
        sys.stderr.write('values_list:\n%s\n' % (pprint.pformat(values_list)))
        sys.stderr.write('exected_values:\n%s\n' % (pprint.pformat(expected_values)))
        all_good = False

    return all_good


def test():
    '''Run the red black tree tests'''
    all_good = True

    rbset = red_black_set_mod.RedBlackTree()
    rbset_items = [6, 15, 16, 17, 5, 8, 0, 4, 10]
    for item in rbset_items:
        rbset.add(item)
    acopy = rbset.copy()


    dict_items = list(range(10))
    dict_ = red_black_dict_mod.RedBlackTree()
    for element in dict_items:
        dict_[element] = 2 ** element

    all_good &= test_entire_tree_ops(rbset, acopy)
    all_good &= test_adding(rbset, acopy)
    all_good &= test_tree_list_and_del_node(rbset, acopy)
    all_good &= test_min_and_max(rbset)
    all_good &= test_contains_and_find(rbset)
    all_good &= test_in_order(rbset, rbset_items)
    all_good &= test_pred_and_succ(dict_items, dict_)
    all_good &= test_check(rbset)
    all_good &= test_uniquing()
    all_good &= test_similar()
    all_good &= test_dict_add()
    all_good &= test_dict_find()
    all_good &= test_dict_setitem()
    all_good &= test_dict_getitem()
    all_good &= test_dict_delitem()
    all_good &= test_dict_iteritems()
    all_good &= test_dict_itervalues()
    all_good &= test_successor()

    if not all_good:
        sys.stderr.write('%s: One or more tests failed\n' % (sys.argv[0],))
        sys.exit(1)

test_tree()
test()
