'''
Created on Oct 31, 2017

@author: michellesong
'''

from Graph import *

folder_graph1= '/Users/michellesong/eclipse-workspace/Homework 4/src/Graph1'
folder_graph2= '/Users/michellesong/eclipse-workspace/Homework 4/src/Graph2'
g = Graph(folder_graph1)
g2 = Graph(folder_graph2)

print g,"\n"
for i in g.nodes.keys():
    for j in g.nodes.keys():
        if i!=j:
            pathList = g.findPath(i,j)
            for path in pathList:
                print "The length from nodeID {} to nodeID {} is {}, passing the lineID{}".format(i,j,path['length'],path['lines_path'])
            shortpath = g.findShortestPath(i,j)
            print "The shortest path above is {},which passes the nodesID {} and the linesID {}".format(shortpath['length'],shortpath['nodes_path'],shortpath['lines_path']),'\n'
            
              

print g2,"\n"
for i in g2.nodes.keys():
    for j in g2.nodes.keys():
        if i!=j:
            pathList = g2.findPath(i,j)
            for path in pathList:
                print "The length from nodeID {} to nodeID {} is {}, passing the lineID{}".format(i,j,path['length'],path['lines_path'])
            shortpath = g2.findShortestPath(i,j)
            print "The shortest path above is {},which passes the nodesID {} and the linesID {}".format(shortpath['length'],shortpath['nodes_path'],shortpath['lines_path']),'\n'
            
              
