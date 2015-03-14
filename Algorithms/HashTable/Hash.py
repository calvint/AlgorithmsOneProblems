'''
Created on Sep 22, 2014

@author: Calvin
'''
import random
from _ast import Num



#class implementing linked list
class Stack(object):
    
    itemArray = None
    
    def __init__(self):
        self.itemArray = []
    
    def push(self, int):
        self.itemArray.append(int)
    
    def pop(self):
        return self.pop()
    
    def search(self, int):
        count = 0
        searched = []
        while self.itemArray != []:
            num = self.itemArray.pop()
            searched.append(num)
            count += 1
            if num == int:
                for i in range(len(searched)):
                    self.itemArray.append(searched.pop())
                return (True, count)
        for i in range(len(searched)):
            self.itemArray.append(searched.pop())
        return (False, count)
    
    def delete(self, int):
        count = 0
        searched = []
        while self.itemArray != []:
            num = self.itemArray.pop()
            searched.append(num)
            count += 1
            if num == int:
                searched.pop()
                for i in range(len(searched)):
                    self.itemArray.append(searched.pop())
                return (True, count)
        for i in range(len(searched)):
            self.itemArray.append(searched.pop())
        return (False, count) 
    

#takes a dictionary as the hash table and a list of numbers that 
# must be added to the hash
class HashTable():
    table = None
    divCount = None
    
    def __init__(self, divisions):
        self.table = {}
        self.divCount = divisions
    
    def insert(self, keys):
        for num in keys:
            mod = num%100000
            if mod not in self.table.keys():
                self.table[mod] = Stack()
                self.table[mod].push(num)
            elif mod in self.table.keys():
                self.table[mod].push(num)
    
    def search(self, keys):
        results = []
        count = 0
        for num in keys:
            mod = num%100000
            if mod in self.table.keys():
                resultTuple = self.table[mod].search(num)
                count += resultTuple[1]
                if resultTuple[0]:
                    results.append(num)
                
        return results, count
    
    def delete(self, keys):
        results = []
        count = 0
        for num in keys:
            mod = num%100000
            if mod in self.table.keys():
                resultTuple = self.table[mod].delete(num)
                count += resultTuple[1]
                if resultTuple[0]:
                    results.append(num)
        return results, count


def generateKeys(number, domain):
    keys = []
    for i in range(number):
        keys.append(random.randrange(0,domain))
    return keys
    
def generateSmallKeys():
    keys = []
    for i in range(0, 10):
        keys.append(random.randrange(0,20))
    return keys
    
if __name__ == "__main__":
    hashtb = HashTable(100000)
    keys_one = generateKeys(10000, 2000000000)
    hashtb.insert(keys_one)
    keys_two = generateKeys(10000, 2000000000)
    results = hashtb.search(keys_two)
    print "search found this many matches: {0}  \n".format(len(results[0]))
    print "list of common keys from search: " + str(list( set(keys_one).intersection( set(keys_two) ) ) )
    print "number of comparisons: " + str(results[1])

    keys_three = generateKeys(10000, 2000000000)
    results = hashtb.delete(keys_three)
     
    print "delete found this many matches: {0}  \n".format(len(results[0]))
    print "list of common keys from delete: " + str(list( set(keys_one).intersection( set(keys_three) ) ) )
    print "number of comparisons: " + str(results[1])




