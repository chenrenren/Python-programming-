'''
Created on Oct 31, 2017

@author: michellesong
'''


import os
from Graph import *
from Line import *
from Node import *
from docutils.parsers.rst.directives import path
from copy import deepcopy

class Graph(object):
    def __init__(self, folder_name):
        '''
        Constructor:
        '''
        os.chdir(folder_name )
        self.nodes = {}
        f = open('nodes.txt', 'r')
        for line in f:
            l = line.rstrip().split('\t')
            v = Vector([float(l[1]), float(l[2])])
            self.nodes[l[0]]= Node(l[0],v)
        f.close()
        
        self.lines = {}
        f = open('lines.txt', 'r')
        for line in f:
            l = line.rstrip().split('\t')
            for nodeid in self.nodes.keys():
                if nodeid==l[1]:
                    self.nodes[nodeid].attach(l[0])
                    p1 = self.nodes[nodeid].getPosition()
                elif nodeid==l[2]:
                    self.nodes[nodeid].attach(l[0]);
                    p2 = self.nodes[nodeid].getPosition()
                else:
                    "The nodeID doesn't match"
            length=(Vector(p1-p2)).distance()
            length = round(length, 2)
            self.lines[l[0]] = Line(l[0], l[1], l[2],length) 
        
        f.close()
        
        
    def __str__(self):  
        Nodes_list = []
        Lines_list = []
        for i in self.nodes:
            Nodes_list.append(self.nodes[i].__str__())
        for i in self.lines:
            Lines_list.append(self.lines[i].__str__())
        return 'Nodes ='+'\n'.join(Nodes_list) +'\n'+'\n'+'Lines = '+'\n'.join(Lines_list)
    
    
    def findPath(self, startID, endID):
        global PathList
        PathList = []
        
        if startID not in self.nodes.keys() :
            print "unknown nodeid={}".format(startID)
        if endID not in self.nodes.keys():
            print "unknown nodeid={}".format(endID)
        
        path = dict(nodes_path = [], lines_path = [], length = 0.0)
        self.DFS(str(startID), str(endID), path, Nodes_Traveled = [], Lines_Traveled = [])
        return PathList
    
    
    def DFS(self, startID, endID, path,Nodes_Traveled, Lines_Traveled):
        if startID not in Nodes_Traveled:
            traveledNodes2 = deepcopy(Nodes_Traveled)
            traveledLines2 = deepcopy(Lines_Traveled)
            traveledNodes2.append(startID)
            for l in self.nodes[startID].getAttachedLines():
                if l not in traveledLines2:
                    traveledLines2.append(l)
                    for n in self.lines[l].getNodes():
                        if n not in traveledNodes2:
                            pathreal = deepcopy(path)
                            pathreal['nodes_path'].append(startID)
                            pathreal['lines_path'].append(l)
                            pathreal['length']+=self.lines[l].length
                            if n==endID:     
                                pathreal['nodes_path'].append(endID)
                                PathList.append(pathreal)
                            else:
                                self.DFS(n, endID, pathreal,traveledNodes2, traveledLines2)
    
    

    def findShortestPath(self, startID, endID):
        Paths = self.findPath(startID, endID)
        shortest_path = Paths[0]['length']
        j=0
        for i in range(1,len(Paths)):
            if Paths[i]['length'] < shortest_path:
                j=i
                shortest_path = Paths[i]['length']
        return Paths[j]
                          
    def numNodes(self):
        return len(self.nodes)
    
    def numLines(self):
        return len(self.lines)
    