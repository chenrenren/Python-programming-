'''
Created on Oct 31, 2017

@author: michellesong
'''


class Line(object):

    def __init__(self, id, nodeIid, nodeJid, length):
        self.nodeIid = nodeIid
        self.nodeJid = nodeJid
        self.id = id
        self.nodes = [nodeIid, nodeJid]
        self.nodes.sort()
        self.length = length
        
    def __len__(self):
        return self.length
    
    def getID(self):
        return self.id
    
    def getNodes(self):
        return self.nodes
    
    def attach(self, nodeID):
        if nodeID not in self.nodes:
            self.nodes.append(nodeID)
            return self.nodes
        else:        
            return "{} is already in the Node.".format (nodeID)
    
    def detach(self, nodeID):
        if nodeID in self.nodes and len(self.nodes)>0:
            self.nodes.remove(nodeID)
            return self.nodes
        if nodeID not in self.nodes:
            return "{} is not in the Node".format(nodeID)
        
    def __str__(self): 
        return "\nID:{}, NodeStart:{}, NodeEnd:{}".format(self.id,self.nodeIid,self.nodeJid)
    
    def length(self):
        return self.length
    
    
   