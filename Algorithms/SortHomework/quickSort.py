'''
Created on Sep 14, 2014

@author: Calvin
'''

def quicksort(array, start_index, end_index ):
    if start_index < end_index:
        q = partition(array, start_index, end_index)
        quicksort(array, start_index, q - 1)
        quicksort(array, q +1, end_index)

def exchange_items(array, first_index, second_index):
    x = array[second_index ]
    array[second_index] = array[first_index]
    array[first_index] = x

def partition(array, start_index, end_index):
    x = array[end_index]
    i = start_index -1;
    for j in range(start_index, end_index):
        if array[j] <= x:       
            i = i + 1
            exchange_items(array, i, j)
    exchange_items(array, i +1, end_index)
    return i +1

# array = [3,14,5,76,24,2]
# quicksort(array, 0, 5);
# for i in array:
#     print(i)

            
        