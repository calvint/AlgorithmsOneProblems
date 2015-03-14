'''
Created on Oct 2, 2014

@author: Calvin
'''
import red_black_set_mod
import Hash


keys = Hash.generateKeys(10000, 2000000000)
#case (i)...
table_one = Hash.HashTable(100000)
#case (ii)...
table_two = Hash.HashTable(1000)
#red black BST
rb_tree = red_black_set_mod.RedBlackTree()

#a) the inserts
table_one.insert(keys)
print "inserted 10,000 elements into table_one with 0 comparisons\n"

table_two.insert(keys)
print "inserted 10,000 elements into table_two with 0 comparisons\n"

totalCount = 0
for key in keys:
    node, count = rb_tree.add(key)
    totalCount += count
print "inserted 10,000 elements into rb_tree with {0} comparisons\n".format(str(totalCount))

#b) the deletes

#(i) deleting first 1000 elements
results, count = table_one.delete(keys[9000:9999])
print "deleted last 1000 elements added to table_one with {0} comparisons\n".format(count)

results, count = table_one.delete(keys[9000:9999])
print "deleted last 1000 elements added to table_two with {0} comparisons\n".format(count)

totalCount = 0 
for key in keys[9000:9999]:
    count = rb_tree.discard(key)
    totalCount += count
print "deleted last 1000 elements added to rb_tree with {0} comparisons\n".format(totalCount)

#(i) deleting first 100 elements

#re-inserting all of the keys to delete the first 100
table_one = Hash.HashTable(100000)
table_two = Hash.HashTable(1000)
rb_tree = red_black_set_mod.RedBlackTree()
table_one.insert(keys)
table_two.insert(keys)
totalCount = 0
for key in keys:
    node, count = rb_tree.add(key)
    totalCount += count

#actually deleting stuff
results, count = table_one.delete(keys[9900:9999])
print "deleted last 100 elements added to table_one with {0} comparisons\n".format(count)

results, count = table_one.delete(keys[9900:9999])
print "deleted last 100 elements added to table_two with {0} comparisons\n".format(count)

totalCount = 0 
for key in keys[9900:9999]:
    count = rb_tree.discard(key)
    totalCount += count
print "deleted last 100 elements added to rb_tree with {0} comparisons\n".format(totalCount)

