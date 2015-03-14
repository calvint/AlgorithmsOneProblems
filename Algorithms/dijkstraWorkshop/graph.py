'''
Created on Nov 8, 2014

@author: Gary
'''
from numpy.f2py.auxfuncs import throw_error

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
    
    def weight_between(self, x, y ):
        #weight going from x to y
        for edge in self.edgeArray:
            if self.vertexNameArray[edge[0]] == x and self.vertexNameArray[edge[1]] == y:
                return edge[2]
        return None
    
    def relax(self, u, v,source):
        if self.weight_between(u,v) == None:
            raise Exception("finding weight between two nodes that are not connected")
        if self.find_distance(v, source) > self.find_distance(u, source) + self.weight_between(u, v):
            self.set_vertex(v, self.find_distance(u, source) + self.weight_between(u, v), source)
            self.set_previous(v, u, source)
    
    def verticies_unseen(self, source):
        #checks if there are any remaining verticies in Q
        for vertex in source:
            distance, previous_vertex, in_s = source[vertex]
            if in_s == False:
                return True
        return False
        
    def extract_min(self, source):
        #well I didn't use a heap so this is what I'm left with...
        result = []
        for vertex in source:
            distance, previous_vertex, in_s = source[vertex]
            if in_s == False:
                if result == [] or result[1] > distance:
                    result = [vertex, distance, previous_vertex]
        #remove resulting vertex from Q
        source[result[0]][2] = True
        return result
    
    def find_adjacent(self, u):
        result = []
        for edge in self.edgeArray:
            if edge[0] == self.vertexIndexMap[u]:
                result.append(self.vertexNameArray[edge[1]])
        return result
    
    def find_distance(self, vertex, source):
        return source[vertex][0]
    
    def set_vertex(self, vertex, distance, source):
        source[vertex][0] = distance
        
    def set_previous(self, vertex, previous, source):
        source[vertex][1] = previous
        
    def dijkstra(self, s):
        initializedSingleSource = {}
        for vertex in self.vertexIndexMap.keys():
            initializedSingleSource[vertex] = [float("inf"), None, False]
        initializedSingleSource[s][0] = 0
        S = {}
        while self.verticies_unseen(initializedSingleSource):
            u, vertex_distance, previous_vertex = self.extract_min(initializedSingleSource)
            S[u] = [vertex_distance, previous_vertex]
            for v in self.find_adjacent(u):
                self.relax(u, v, initializedSingleSource)
        return S
            
        
    
    
    
    
    
    
    
    
    
    