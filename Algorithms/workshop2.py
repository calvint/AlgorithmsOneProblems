

"""Heapsort Workshop
Calvin Troutt 9/7/14
"""
def makeHeap(array):
	result = {}
	index = 0
	for number in array:
		index += 1
		result[index] = number
	return result

def maxHeapify(heap, index):
	left = index << 1
	right = (index << 1) +1
	if left <= len(heap) and heap[left] > heap[index]:
		largest = left
	else:
		largest = index
	if right <= len(heap) and heap[right] > heap[largest]:
		largest = right
	if largest != index:
		tempVar = heap[index]
		heap[index] = heap[largest]
		heap[largest] = tempVar
		maxHeapify(heap, largest)

def buildMaxHeap(heap):
	for i in range(len(heap)/2, 0, -1):
		maxHeapify(heap, i)

def heapSort(heap):
	buildMaxHeap(heap)
	result = []
	for i in range(len(heap), 1, -1):
		result.append(heap[1])
		heap[1] = heap[i]
		del heap[i]
		maxHeapify(heap, 1)
	result.append(heap[1])
	return result

heap = makeHeap([3,14,5,76,24,2])
result = heapSort(heap)
for i in result:
	print(i)

		
		
		
		
