'''
Created on Nov 8, 2014

@author: Gary
'''
from math import sqrt
from math import pow

class graph:
    def __init__(self):
        self.vertexNameArray       = [] # vertex names in an array
        self.vertexIndexMap        = {} # vertex names to index dictionary
        self.vertexPositionArray   = [] # x,y pair position array
        self.edgeArray             = [] # array of (vertex index pair, weight)
    
    def addVertex(self, name, x, y):
        self.vertexIndexMap[name] = self.vCount()
        self.vertexNameArray.append(name)
        self.vertexPositionArray.append((x,y))
        
    def addEdge(self, vName1, vName2, weight):
        self.edgeArray.append((self.vertexIndexMap[vName1],self.vertexIndexMap[vName2],weight))
        
    def vCount(self): return len(self.vertexNameArray)
    
    def eCount(self): return len(self.edgeArray)
    
    # Access functions for vertex information
    def  vX(   self, i): return self.vertexPositionArray[i][0]
    def  vY(   self, i): return self.vertexPositionArray[i][1]
    def  vName(self, i): return self.vertexNameArray[i]
    
    # Access functions for edge information
    def  eV0X( self, i): return self.vertexPositionArray[self.edgeArray[i][0]][0]
    def  eV0Y( self, i): return self.vertexPositionArray[self.edgeArray[i][0]][1]
    def  eV1X( self, i): return self.vertexPositionArray[self.edgeArray[i][1]][0]
    def  eV1Y( self, i): return self.vertexPositionArray[self.edgeArray[i][1]][1]
    def  eWght(self, i): return self.edgeArray[i][2]
    
    #uses the cross product to find wether the angle turns left or right
    def angleTurnsLeft(self, point1, middlePoint, point3):
        crossProduct = (self.vX(middlePoint) - self.vX(point1)) * (self.vY(point3) - self.vY(point1)) - (self.vX(point3) - self.vX(point1)) * (self.vY(middlePoint) - self.vY(point1))
        if crossProduct >= 0.0:
            return True
        else: 
            return False
        
    
    def findConvexHullEdges(self):
        #find lowest vertex
        yValMap = {}
        for i in range(self.vCount()):
            if self.vY(i) not in yValMap.keys():
                yValMap[self.vY(i)] = []
            yValMap[self.vY(i)].append(i)
        lowestVertexIndex = yValMap[sorted(yValMap.keys())[0]][0]
        
        
        #order other verticies acording to decreasing normalized x value
        xNormalizedMap = {}
        for i in range(self.vCount()):
            if i != lowestVertexIndex:
                #using formula: (Xi - X0)/(sqrt( (Xi - X0)^2 + (Yi - Y0)^2 )
                normalizedXValue = (self.vX(i) - self.vX(lowestVertexIndex)) / sqrt( (self.vX(i) - self.vX(lowestVertexIndex))**2 + (self.vY(i) - self.vY(lowestVertexIndex))**2 )
                if normalizedXValue not in xNormalizedMap.keys():
                    xNormalizedMap[normalizedXValue] = i
                else:
                    if self.vX(i) < self.vX(xNormalizedMap[normalizedXValue]):
                        xNormalizedMap[normalizedXValue] = i
        orderedVerticies = [lowestVertexIndex]
        for xValue in sorted(xNormalizedMap.keys(), reverse = True):
            orderedVerticies.append(xNormalizedMap[xValue])
        orderedVerticies.append(lowestVertexIndex)
        
        #select final and original edges
        originallyTriedEdges = []
        finalEdges = [(orderedVerticies[0], orderedVerticies[1])]
        i=0
        while i < len(orderedVerticies)-2:
            if self.angleTurnsLeft(orderedVerticies[i], orderedVerticies[i+1], orderedVerticies[i+2]):
                finalEdges.append((orderedVerticies[i+1],orderedVerticies[i+2]))
                i += 1
            else:
                orderedVerticies.pop(i+1)
                originallyTriedEdges.append(finalEdges.pop())
                i -= 1
        return originallyTriedEdges, finalEdges
            
        
        
        
        
        