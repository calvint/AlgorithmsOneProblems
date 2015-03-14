'''
Created on Nov 8, 2014

@author: Gary
'''
import copy

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
    
    def getMinSpanningTreeEdgesIndexes(self):
        #make a modifyable copy of vertexIndexMap
        vertexMapCopy =  copy.deepcopy(self.vertexIndexMap)
        #make a dictionary of weights to edge indices
        weightMap = {}
        i=0
        for edge in self.edgeArray:
            if edge[2] not in weightMap.keys():
                weightMap[edge[2]] = [i] 
            else:
                weightMap[edge[2]].append(i)
            i+=1
        #make an ordered array of weights
        weightsArray = sorted(weightMap.keys())
        results = []
        for weight in weightsArray:
            edgeIndicies = weightMap.get(weight)
            for index in edgeIndicies:
                newGroupNum = vertexMapCopy[self.vName(self.edgeArray[index][0])]
                oldGroupNum = vertexMapCopy[self.vName(self.edgeArray[index][1])]
                #if they aren't already in the same connected group...
                if newGroupNum != oldGroupNum:
                    results.append(index)
                    #make them in the same group
                    for name, otherGroupNumber in vertexMapCopy.items():
                        if otherGroupNumber == oldGroupNum:
                            vertexMapCopy[name] = newGroupNum
        return results
                    
                
        
             