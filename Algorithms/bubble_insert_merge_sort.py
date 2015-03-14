'''
Created on Aug 12, 2014

@author: Gary
'''

import time                                                

def sort_me(arr):
    sort_me_merge(arr,0,len(arr)-1)

def sort_me_merge(arr,p,r):
    # This is a merge sort
    if ( p < r ):
        q = (p + r) / 2
        sort_me_merge(      arr,p  ,q)
        sort_me_merge(      arr,q+1,r)
        
        #merge
        p2 = p
        q2 = q+1
        arrTemp = list(arr[p:r+1])
        i = 0
        while ( p2 <= q and q2 <= r ):
            if ( arr[p2] > arr[q2] ): # then swap
                arrTemp[i] = arr[q2]
                q2 = q2 + 1
            else:
                arrTemp[i] = arr[p2]
                p2 = p2 + 1
            i = i + 1
        if ( p2 <= q ):
            arrTemp[r-p-q+p2:r-p+1] = arr[p2:q+1]
        arr[p:r+1] = list(arrTemp)

def sort_me_insertion(arr):
    # This is an insertion sort
    for j in range(1,len(arr)):
        key = arr[j]
        i = j - 1
        while ( i>=0 and arr[i]>key ):
            arr[i+1] = arr[i]
            i = i-1
        arr[i+1] = key

def sort_me_bubble(arr):
    # This is a bubble sort
    for i in range(0,len(arr)-1):
        for j in range(i+1,len(arr)):
            if  arr[i] > arr[j]: # if TRUE then swap i and j in array
                temp   = arr[i]
                arr[i] = arr[j]
                arr[j] = temp

def time_me(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        #print(endTime - startTime,'ms')
        return [result,endTime-startTime]

    return wrapper

@time_me
def sort_me_timed(arr):
    sort_me(arr)

def is_sorted(lst, key=lambda x, y: x < y):
    for i, el in enumerate(lst[1:]):
        if key(el, lst[i]):
            return False
    return True

def generate_shuffled_array(nElements,isPrint=False):
    import numpy as np
    arr = np.arange(nElements)
    if isPrint: print(arr)
    np.random.shuffle(arr)
    if isPrint: print(arr)
    return arr

nElements = 100
for i in range(0,6):
    arr = generate_shuffled_array(nElements,False)
    timed_result = sort_me_timed(arr)
    print(nElements,timed_result[1])
    if not is_sorted(arr):
        print("Array not sorted")
        if nElements < 25: print(arr)
    nElements *= 2;