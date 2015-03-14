'''
Created on Nov 8, 2014

@author: Gary
'''

import fileinput
import graph
import matplotlib.pyplot as plt
    
# Parse graph.txt and populate mygraph structure.
mygraph = graph.graph()
isVertices = True
for line in fileinput.input("interestingGraphTwo.txt"):
    if isVertices:
        if "----------" in line:
            isVertices = False
        else: #read vertices in this part
            split = line.split()
            mygraph.addVertex(split[0],float(split[1]),float(split[2]))
    else:     #read    edges in this part
        split = line.split()
        mygraph.addEdge(split[0], split[1], float(split[2]))
    print line, isVertices

# Display vertices
minX = minY =  1e1000
maxX = maxY = -1e1000
for iV in range (0, mygraph.vCount()):
    x = mygraph.vX(iV)
    y = mygraph.vY(iV)
    plt.plot(x,y,'wo', ms = 15)
    minX = min(minX,x)
    minY = min(minY,y)
    maxX = max(maxX,x)
    maxY = max(maxY,y)
    plt.text(x, y, mygraph.vName(iV), ha = 'center', va = 'center')
padX = .02*(maxX-minX)+5
padY = .02*(maxY-minY)+5
plt.axis([minX-padX, maxX+padX, minY-padY, maxY+padY])

# Display edges
for iE in range (0, mygraph.eCount()):
    x0 = mygraph.eV0X(iE)
    y0 = mygraph.eV0Y(iE)
    x1 = mygraph.eV1X(iE)
    y1 = mygraph.eV1Y(iE)
    xM = (x0+x1)/2
    yM = (y0+y1)/2
    plt.plot([x0,x1],[y0,y1],color='0.9')
    plt.text(xM, yM, mygraph.eWght(iE))
    
# Find out how to find edges and do that...

# add all of the edges
for iE in mygraph.getMinSpanningTreeEdgesIndexes():
    x0 = mygraph.eV0X(iE)
    y0 = mygraph.eV0Y(iE)
    x1 = mygraph.eV1X(iE)
    y1 = mygraph.eV1Y(iE)
    xM = (x0+x1)/2
    yM = (y0+y1)/2
    plt.plot([x0,x1],[y0,y1],color='c')
    plt.text(xM, yM, mygraph.eWght(iE))

plt.show()
