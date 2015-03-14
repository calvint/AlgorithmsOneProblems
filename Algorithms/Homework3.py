import time
import random

def findMaxCrossingSubarray(array, low, mid, high):
	tempSum = 0
	leftSum = None
	for i in range(mid, low - 1, -1):
		tempSum += array[i]
		if leftSum == None or tempSum > leftSum:
			leftSum = tempSum
			maxLeft = i
	tempSum = 0
	rightSum = None
	for i in range(mid+1, high+1):
		tempSum += array[i]
		if rightSum == None or tempSum > rightSum:
			rightSum = tempSum
			maxRight = i
	return (maxLeft, maxRight, leftSum+rightSum)


def findMaxSubArray(array, low, high):
	if high == low:
		return (low, high, array[low])
	else:
		mid = (low + high)/2
		(leftLow, leftHigh, leftSum) = findMaxSubArray(array, low, mid)
		(rightLow, rightHigh, rightSum) = findMaxSubArray(array, mid + 1, high)
		(crossingLow, crossingHigh, crossingSum) = findMaxCrossingSubarray(array, low, mid, high)
		if leftSum > rightSum and leftSum > crossingSum:
			return (leftLow, leftHigh, leftSum)
		if rightSum > leftSum and rightSum > crossingSum:
			return (rightLow, rightHigh, rightSum)
		else:
			return (crossingLow, crossingHigh, crossingSum)

#array = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
#(Low, High, Sum) = findMaxSubArray(array, 0, len(array)-1)
#print("The maximum subarray has a sum of " + str(Sum) + ", a lower index value of " + str(Low) + ", and a higher index value of " + str(High))


def bruteForceMaxSubArray(array):
	maxSum = None
	for low in range( 0, len(array)):
		for high in range( low, len(array)):
			tempSum = 0
			for k in range( low, high+1):
				tempSum += array[k]
			if maxSum == None or tempSum > maxSum:
				maxSum = tempSum
				maxLow = low
				maxHigh = high
	return (maxLow, maxHigh, maxSum)
	

#array = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
#(Low, High, Sum) = bruteForceMaxSubArray(array)
#print("The maximum subarray has a sum of " + str(Sum) + ", a lower index value of " + str(Low) + ", and a higher index value of " + str(High))

def findNForCrossover():
	for n in range(1, 1000):
		testArray = range(n)
		random.shuffle(testArray)
		recursiveStart = time.time()
		findMaxSubArray(testArray, 0, len(testArray)-1)
		recursiveTime = time.time()-recursiveStart
		
		testArray = range(n)
		random.shuffle(testArray)
		bruteStart = time.time()
		bruteForceMaxSubArray(testArray)
		bruteTime = time.time()-bruteStart
		
		if recursiveTime < bruteTime:
			print("The crossover occured at n = %s" %n)
			return (n, recursiveTime, bruteTime)

findNForCrossover()

def findMaxSubArrayWithBruteBase(array, low, high):
	if high == low:
		return bruteForceMaxSubArray(array)
	else:
		mid = (low + high)/2
		(leftLow, leftHigh, leftSum) = findMaxSubArray(array, low, mid)
		(rightLow, rightHigh, rightSum) = findMaxSubArray(array, mid + 1, high)
		(crossingLow, crossingHigh, crossingSum) = findMaxCrossingSubarray(array, low, mid, high)
		if leftSum > rightSum and leftSum > crossingSum:
			return (leftLow, leftHigh, leftSum)
		if rightSum > leftSum and rightSum > crossingSum:
			return (rightLow, rightHigh, rightSum)
		else:
			return (crossingLow, crossingHigh, crossingSum)

#array = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
#(Low, High, Sum) = findMaxSubArrayWithBruteBase(array, 0, len(array)-1)
#print("The maximum subarray has a sum of " + str(Sum) + ", a lower index value of " + str(Low) + ", and a higher index value of " + str(High))


def findNForCrossoverWithBruteBase():
	for n in range(1, 1000):
		testArray = range(n)
		random.shuffle(testArray)
		recursiveStart = time.time()
		findMaxSubArrayWithBruteBase(testArray, 0, len(testArray)-1)
		recursiveTime = time.time()-recursiveStart
		
		testArray = range(n)
		random.shuffle(testArray)
		bruteStart = time.time()
		bruteForceMaxSubArray(testArray)
		bruteTime = time.time()-bruteStart
		
		if recursiveTime < bruteTime:
			print("The crossover occured at n = %s" %n)
			return (n, recursiveTime, bruteTime)

findNForCrossoverWithBruteBase()


