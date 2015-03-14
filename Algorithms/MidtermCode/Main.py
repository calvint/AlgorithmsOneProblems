'''
Created on Oct 2, 2014

@author: Calvin
'''
import red_black_set_mod
import random
import binary_tree

random.seed(1)

def generateKeys(number, domain):
    keys = []
    for i in range(number):
        keys.append(random.randrange(0,domain))
    return keys


keys = generateKeys(10000, 2000000000)

#red black BST
rb_tree = red_black_set_mod.RedBlackTree()

#new tree type
diffTree = binary_tree.Node(keys[0])


#i) 10,000 inserts


totalCount = 0
for key in keys:
    node, count = rb_tree.add(key)
    totalCount += count
print "inserted 10,000 elements into rb_tree with {0} comparisons\n\n".format(str(totalCount))

count = 0
rotates = 0
for key in keys[1:]:
    countInc, rotatesInc, root = diffTree.checkThenInsert(key, diffTree)
    diffTree = root
    count += countInc
    rotates += rotatesInc
print "inserted 10,000 elements into new type bst with {0} comparisons and {1} rotates\n\n".format(str(count) , str(rotates))


#(ii) deleting first 1000 elements


totalCount = 0 
for key in keys[9000:9999]:
    count = rb_tree.discard(key)
    totalCount += count
print "deleted last 1000 elements added to rb_tree with {0} comparisons\n\n".format(totalCount)

count = 0
rotates = 0
for key in keys[9000:9999]:
    countInc, rotatesInc, root = diffTree.delete(key, diffTree)
    diffTree = root
    count += countInc
    rotates += rotatesInc
print "deleted last 1000 elements from new type bst with {0} comparisons and {1} rotates\n\n".format(str(count) , str(rotates))

#(iii) inserting 1000 elements


rb_tree = red_black_set_mod.RedBlackTree()
totalCount = 0
for key in keys[:999]:
    node, count = rb_tree.add(key)
    totalCount += count
print "inserted 1000 elements into rb_tree with {0} comparisons and {1} rotates\n\n".format(str(count) , str(rotates))


count = 0
rotates = 0
for key in keys[1:999]:
    countInc, rotatesInc, root = diffTree.insert(key, diffTree)
    diffTree = root
    count += countInc
    rotates += rotatesInc
print "inserted 1000 elements into new type bst with {0} comparisons and {1} rotates\n\n".format(str(count) , str(rotates))


# (iv) deleting last 100 elements added

totalCount = 0 
for key in keys[900:999]:
    count = rb_tree.discard(key)
    totalCount += count
print "deleted last 100 elements added to rb_tree with {0} comparisons\n\n".format(totalCount)

count = 0
rotates = 0
for key in keys[900:999]:
    countInc, rotatesInc, root = diffTree.delete(key, diffTree)
    diffTree = root
    count += countInc
    rotates += rotatesInc
print "deleted last 100 elements from new type bst with {0} comparisons and {1} rotates\n\n".format(str(count) , str(rotates))
