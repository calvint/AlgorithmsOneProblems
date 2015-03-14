'''
Created on Nov 8, 2014

@author: Gary
'''

import fileinput
import graph
import matplotlib.pyplot as plt
from   matplotlib.path import Path
import matplotlib.patches as patches
import math
    
def plotEdge( plot_axis, x0, y0, x1, y1, weight, clr):
    d0 = 4 # This is an offset so the edge is not drawn to the middle of vertex
    d2 = 20 # This is an offset to the end of the arrow tails
    dx = x1-x0
    dy = y1-y0
    length = math.sqrt(dx*dx+dy*dy)
    if length > 0:
        vx = dx/length
        vy = dy/length
        #plot_axis.plot([x0+vx*d0,x1-vx*d0],[y0+vy*d0,y1-vy*d0], color=clr) # Draw a line
        #plot_axis.text( x0+dx/2, y0+dy/2, weight)
        
        verts = [(x0+vy*d0,y0-vx*d0),(x0+vy*40,y0-vx*40),(x1-vx*80,y1-vy*80),(x1-vx*d0,y1-vy*d0),]
        codes = [Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,]
        path  = Path(verts,codes)
        patch = patches.PathPatch( path, facecolor = 'none', edgecolor = clr)
        plot_axis.add_patch( patch )

        plot_axis.plot([x1-vx*d2+vy*3,x1-vx*d0],[y1-vy*d2-vx*3,y1-vy*d0], color=clr)
        plot_axis.plot([x1-vx*d2-vy*3,x1-vx*d0],[y1-vy*d2+vx*3,y1-vy*d0], color=clr)

        plot_axis.text( x0+dx/2+vy*10, y0+dy/2-vx*10, weight)

# Parse graph.txt and populate mygraph structure.
mygraph = graph.graph()
isVertices = True
for line in fileinput.input("graph.txt"):
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

fig = plt.figure()
plt_ax  = fig.add_subplot(111)



# Display vertices
minX = minY =  1e1000
maxX = maxY = -1e1000
for iV in range (0, mygraph.vCount()):
    x = mygraph.vX(iV)
    y = mygraph.vY(iV)
    plt_ax.plot(x,y,'wo', ms = 15)
    minX = min(minX,x)
    minY = min(minY,y)
    maxX = max(maxX,x)
    maxY = max(maxY,y)
    plt_ax.text(x, y, mygraph.vName(iV), ha = 'center', va = 'center')
padX = .10*(maxX-minX)+10
padY = .10*(maxY-minY)+10
plt_ax.axis([minX-padX, maxX+padX, minY-padY, maxY+padY])

originallyTriedEdges, finalEdges = mygraph.findConvexHullEdges();

# Display edges originally tried edges
for edge in originallyTriedEdges:
    x0 = mygraph.vX(edge[0])
    y0 = mygraph.vY(edge[0])
    x1 = mygraph.vX(edge[1])
    y1 = mygraph.vY(edge[1])
    plotEdge(plt_ax, x0, y0, x1, y1, "", 'red')
    
# Display final edges
for edge in finalEdges:
    x0 = mygraph.vX(edge[0])
    y0 = mygraph.vY(edge[0])
    x1 = mygraph.vX(edge[1])
    y1 = mygraph.vY(edge[1])
    plotEdge(plt_ax, x0, y0, x1, y1, "", 'black')

plt.show()
