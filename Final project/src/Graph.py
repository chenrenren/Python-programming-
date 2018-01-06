'''
Created on Nov 14, 2017

@author: michellesong
'''

import sqlite3 as dbi
import sys
from copy import deepcopy
#from Test import drawshortest


class Graph(object):
    def __init__(self, folder_name):
        try:
            self.db = dbi.connect(folder_name)
            self.cu = self.db.cursor()
        except:
            #print 'failed'
            sys.exit()

    def getAirportCodes(self):
        cmd="""select AirportID from Airport order by AirportID"""
        self.cu.execute(cmd)
        l=[]
        for i in self.cu.fetchall():
            l.append(i[0])
        return l

    def ListofFlights(self):
        Flights = []
        cmd = """select Fl.FlightNum, Fl.FromCity, Fl.ToCity, 
                AP1.Longitude, AP1.Latitude, AP2.Longitude, AP2.Latitude from 
                Airport as AP1, Airport as AP2, Flights as Fl 
                where AP1.AirportID = Fl.FromCity and AP2.AirportID = Fl.ToCity
                order by Fl.FromCity, Fl.ToCity
                """
        self.cu.execute(cmd)
        for i in self.cu.fetchall():
            Flights.append(i)
        return Flights
    
    def getAirportPos(self):
        ListofAirports = []
        cmd = """select AP.AirportID, AP.Longitude, AP.Latitude from Airport as AP"""
        self.cu.execute(cmd)

        for i in self.cu.fetchall():
            ListofAirports.append(i)
        return ListofAirports
    
    def getAttachedLines(self, APName):
        sql="""select FlightID FROM Flights
               where FromCity='{}'"""
        self.cu.execute(sql.format(APName))
        l=[]
        for i in self.cu.fetchall():
            l.append(i[0])
        return l

    def getAttachedNodes(self, FtID):  
        sql="""select ToCity from Flights
               where FlightID='{}' """
        self.cu.execute(sql.format(FtID)) 
        return self.cu.fetchone()

    def getCityofAirport(self,APName):
        sql="""select Ct.Name, Ct.State FROM Cities as Ct, Airport as Ap 
                   where Ap.CityID=Ct.CityID and Ap.AirportID='{}'"""
        self.cu.execute(sql.format(APName))
        return self.cu.fetchone()

    def printFlightInfo(self, FtID):
        sql="""select Fl.FlightNum, Ct1.Name, Ct1.State, Ap1.AirportID, 
            Fl.DepartureTime, Ct2.Name, Ct2.State, Ap2.AirportID, Fl.ArrivalTime 
            from Flights as Fl, Airlines as Al, Airport as Ap1, Airport as Ap2, 
            Cities as Ct1, Cities as Ct2
            where Al.AirlineID=Fl.OperatorID and Fl.FromCity=Ap1.AirportID and 
            Ap1.CityID=Ct1.CityID and Fl.ToCity=Ap2.AirportID and 
            Ap2.CityID=Ct2.CityID and Fl.FlightID={}"""
        self.cu.execute(sql.format(FtID))
        fl = self.cu.fetchone()
        s="""on Flight Number {} from {}, {}, ({}) at {}:{:02d}, arrive at {}, {} ({}) at {}:{:02d} \n"""\
                 .format(fl[0], fl[1],fl[2],fl[3],fl[4]/60,fl[4]%60,fl[5], fl[6], fl[7], fl[8]/60,fl[8]%60)

        return s
    #helper function getting necessary information of flight for given flight ID and return a list of the infos rather than string
    def FlightInfo(self, FtID):
        sql="""SELECT Fl.FlightNum, Ct1.Name, Ct1.State, Ap1.AirportID, 
                        Fl.DepartureTime, Ct2.Name, Ct2.State, Ap2.AirportID, Fl.ArrivalTime
                          from Flights as Fl, Airlines as Al, Airport as Ap1, 
                          Airport as Ap2, Cities as Ct1, Cities as Ct2
                          where Al.AirlineID=Fl.OperatorID and Fl.FromCity=Ap1.AirportID and
                          Ap1.CityID=Ct1.CityID and Fl.ToCity=Ap2.AirportID and 
                          Ap2.CityID=Ct2.CityID and Fl.FlightID={}"""
        self.cu.execute(sql.format(FtID))
        return self.cu.fetchone()

    def __str__(self):  
        cmd="""select C.Name, A.AirportID, A.X, A.Y
        from Airport AS A, Cities AS C
        where A.CityID=C.CityID"""
        self.cu.execute(cmd)
        
        AllAirports=self.cu.fetchall()
        s='*Airport: \n'
        for i in AllAirports:
            s+="""{} : {} at ({} miles, {} miles) \n""".format(i[0], i[1], i[2], i[3])
            
        s += '* Flights:\n'
        
        cmd = """select Fl.FlightNum, Al.Operator, Ct1.Name, Ct1.State, Ap1.AirportID, 
                Fl.DepartureTime, Ct2.Name, Ct2.State, Ap2.AirportID, Fl.ArrivalTime 
                from Flights as Fl, Airlines as Al, Airport as Ap1, Airport as Ap2, 
                Cities as Ct1, Cities as Ct2 
                where Al.ID=Fl.OperatorID and Fl.FromCity=Ap1.AirportID and 
                Ap1.CityID=Ct1.CityID and Fl.ToCity=Ap2.AirportID and Ap2.CityID=Ct2.CityID"""
        self.cu.execute(cmd) 
        allFlights=self.cu.fetchall()
        
        for i in allFlights:
            s += """Flight Number {} operated by {}: leaving {}, {}, ({}) 
                at {}:{:02d} to {}, {} ({}) arriving at {}:{:02d} \n"""\
                 .format(i[0], i[1],i[2],i[3],i[4],i[5]/60,i[5]%60,i[6], 
                         i[7], i[8], i[9]/60, i[9]%60)
        return s
       
    def findPath(self, startID, endID, allpaths = []):
        sql = """select AirportID from Airport"""
        self.cu.execute(sql)
        AirportList = self.cu.fetchall()
        APorts=[]
        for l in AirportList:
            APorts.append(l[0])
        
        global PathList
        #global AllPaths
        #AllPaths = []
        PathList=[]
        if startID not in APorts:
            print "unknown AirportID=%s" % startID
        if endID not in APorts :
            print "unknown AirportID=%s" % endID
        #(Lines_Traveled, Nodes_Traveled)=([],[])
        Lines_Traveled = []
        Nodes_Traveled = []
        path = dict(nodepath=[], linepath=[], length= 0.0)
        allpaths += [startID]
        if startID == endID:
            return[allpaths]
        #path1 = dict(nodepath=[])
        self.DFS(str(startID), str(endID), path, Nodes_Traveled[:], Lines_Traveled[:])
        #print PathList
        return PathList

    def DFS(self, startID, endID, path, Nodes_Traveled1, Lines_Traveled1):

        if startID not in Nodes_Traveled1:
            #traveledNodes=GtraveledNodes[:]
            Nodes_Traveled1.append(startID)

            GetTT = """select DepartureTime, ArrivalTime from Flights
                                      where FlightID='{}'"""
            #get all the path has went through
            lastpath=path['linepath']
            if len(lastpath) > 0:
                #get the time information for the previous path has travelled
                self.cu.execute(GetTT.format(lastpath[len(lastpath)-1]))
                LastDeptTime = self.cu.fetchone()[0]
                self.cu.execute(GetTT.format(lastpath[len(lastpath)-1]))
                LastArrTime = self.cu.fetchone()[1]
            else:
                LastArrTime = -1
                
            for l in self.getAttachedLines(startID):
                self.cu.execute(GetTT.format(l))
                NewDeptTime= self.cu.fetchone()[0]
                self.cu.execute(GetTT.format(l))
                NewArrTime = self.cu.fetchone()[1]
        
                Nodes_Traveled = Nodes_Traveled1[:]
                Lines_Traveled = Lines_Traveled1[:]
            
                if (l not in Lines_Traveled):
                    Lines_Traveled.append(l)
                    for n in self.getAttachedNodes(l):
                        if n not in Nodes_Traveled:
                            pathreal=deepcopy(path)
                            pathreal['nodepath'].append(startID)
                            pathreal['linepath'].append(l)
                            if LastArrTime == -1:
                                T1=0
                            else:
                                T1=NewDeptTime-LastArrTime
                                if T1 <=0 :
                                    T1=T1+24*60
                            pathreal['length']+=T1+NewArrTime-NewDeptTime
                            if n==endID:     
                                pathreal['nodepath'].append(endID)
                                PathList.append(pathreal)
                            else:
                                self.DFS(n, endID, pathreal, Nodes_Traveled,
                                                  Lines_Traveled)
    
    def findShortestPath(self, startID, endID):
        Paths =self.findPath(startID, endID)
        shortest_path=Paths[0]['length']
        j=0
        for i in range(1,len(Paths)):
            if Paths[i]['length']<shortest_path:
                j=i
                shortest_path = Paths[i]['length']
        
        shortest=Paths[j]
        startInfo = self.getCityofAirport(startID)
        endInfo = self.getCityofAirport(endID)
        firstline = self.FlightInfo(shortest['linepath'][0])
        lastline = self.FlightInfo(shortest['linepath'][len(shortest['linepath'])-1])
#        s = 'Trip: {}: {}, {} to {}: {}, {}\n departs at {}:{:02d}, '\
#            'arrives at {}:{:02d} after traveling for {}:{:02d} hours\n'\
#           .format(startID, startInfo[0], startInfo[1], endID, endInfo[0], endInfo[1],\
#            firstline[4]/60, firstline[4]%60,\
#            lastline[8]/60, lastline[8]%60, int(shortest['length'])/60,\
#            int(shortest['length'])%60)
           
        s = 'Trip: {}: {}, {} to {}: {}, {}\n departs at {}:{:02d} and '\
            'arrives at {}:{:02d} after traveling for {}:{:02d} hours\n'\
           .format(startID, startInfo[0], startInfo[1], endID, endInfo[0], endInfo[1],\
            firstline[4]/60, firstline[4]%60,\
            lastline[8]/60, lastline[8]%60, int(shortest['length'])/60,\
            int(shortest['length'])%60)

        for f in shortest['linepath']:
            s += self.printFlightInfo(f)
            #print self.printFlightInfo(f)
        
        
        return s

    def numNodes(self):
        sql="""select count(AirportID) from Airport"""
        self.cu.execute(sql)
        return self.cu.fetchone()[0]
    
    def numLines(self):
        sql="""select count(FlightID) from Flights"""
        self.cu.execute(sql)
        return self.cu.fetchone()[0]
    
#############################
    def FlightInfos(self, FtID):
        sql="""select Fl.FlightNum, Ct1.Name, Ct1.State, Ap1.AirportID, 
            Fl.DepartureTime, Ct2.Name, Ct2.State, Ap2.AirportID, Fl.ArrivalTime 
            from Flights as Fl, Airlines as Al, Airport as Ap1, Airport as Ap2, 
            Cities as Ct1, Cities as Ct2
            where Al.AirlineID=Fl.OperatorID and Fl.FromCity=Ap1.AirportID and 
            Ap1.CityID=Ct1.CityID and Fl.ToCity=Ap2.AirportID and 
            Ap2.CityID=Ct2.CityID and Fl.FlightID={}"""
        self.cu.execute(sql.format(FtID))
        fl = self.cu.fetchone()
        s="""on Flight Number {} from {}, {}, ({}) at {}:{:02d}, arrive at {}, {} ({}) at {}:{:02d} \n"""\
                 .format(fl[0], fl[1],fl[2],fl[3],fl[4]/60,fl[4]%60,fl[5], fl[6], fl[7], fl[8]/60,fl[8]%60)

        return fl[0]
    
    def ShortestPath(self, startID, endID):
        Paths =self.findPath(startID, endID)
        shortest_path=Paths[0]['length']
        j=0
        for i in range(1,len(Paths)):
            if Paths[i]['length']<shortest_path:
                j=i
                shortest_path = Paths[i]['length']
        
        shortest=Paths[j]
        startInfo = self.getCityofAirport(startID)
        endInfo = self.getCityofAirport(endID)
        firstline = self.FlightInfo(shortest['linepath'][0])
        lastline = self.FlightInfo(shortest['linepath'][len(shortest['linepath'])-1])

        shortestflights = []
        for f in shortest['linepath']:
            s = self.FlightInfos(f)
            shortestflights.append(s)
    
        return shortestflights
    
    def drawshortest(self, Depart, Dest):
        #global drawshortFlights
        global drawshortFlights
        drawshortFlights = []
        Flights = self.ListofFlights()
        shortest_flights = self.ShortestPath(Depart,Dest)
        #print "shortest flights?"
        #print self.graph.ShortestPath(Depart,Dest)
        #print len(shortest_flights)
        #print len(Flights)
        #print Flights[0]
        
        for i in range(len(shortest_flights)):
            #print "i looooop"
            #print shortest_flights[i]
            for j in range(len(Flights)):
                #print "j loooooop"
                if shortest_flights[i] == Flights[j][0]:
                    drawshortFlights.append(Flights[j])
                    #print "Bbbbbb"
                else:
                    pass
        #print "aaaaaa"
        return drawshortFlights
    

    
    