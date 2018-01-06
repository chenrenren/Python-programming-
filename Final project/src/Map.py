'''
Created on Dec 7, 2017

@author: michellesong
'''
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QPainterPath, QColor
from PyQt5.Qt import QVBoxLayout
import math
from PyQt5.QtCore import Qt
from sklearn.ensemble.tests.test_weight_boosting import y_class
from Graph import *
import sqlite3 as dbi
from Crypto.Cipher import DES


class Map(QWidget):
    '''
    variables:
    
    methods:
        def __init__(self, parent)
        def initUI(self)def setGraph(self, g)
        def eventPaint(self, evt)
        def drawFlights(self, qp)
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(Map, self).__init__(parent)
        
        self.shortest_flights = []
        self.x = []
        self.y = []
        #self.drawFlights(qp)
        
        self.initUI()
        self.graph = Graph('Graph.db')
        #self.graph = None
        
    def initUI(self):
        self.setMinimumSize(200, 120)

    def paintEvent(self, evt):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(self.rect(), QPixmap("USmap.png"))

        self.drawFlights(qp)
        #qp.end()
        
    def drawFlights(self, qp):        
        path = QPainterPath()
        #self.shortest_flights = []
        size = self.size()
        h = size.height()
        w = size.width()
        
        #qp.drawLine(w/9.6, h/10.4, 9*w/10.3, 1.97*h/5)
        Rx = (9*w/10.3-w/10)/(122.4167-73.8726)
        Ry = (1.97*h/5-h/1.955)/(math.tan(40.7772*math.pi/180)-
                                 math.tan(37.7833*math.pi/180))
        #SF as long0/lat0
        Long0 = 122.4167
        Lat0 = 37.7833
        
        Flights = self.graph.ListofFlights()
        pos = self.graph.getAirportPos()
        #print pos
        #print Flights
        
        for i in range(len(Flights)):
            counter = 0
            from_longitude = Flights[i][3]
            from_latitude = Flights[i][4]
            
            to_longitude = Flights[i][5]
            to_latitude = Flights[i][6]
            
            x1 = (w/10+Rx*(Long0-from_longitude))
            y1 = (h/1.955+Ry*(math.tan(from_latitude*math.pi/180)-
                             math.tan(Lat0*math.pi/180)))
            
            x2 = (w/10+Rx*(Long0-to_longitude))
            y2 = (h/1.955+Ry*(math.tan(to_latitude*math.pi/180)-
                             math.tan(Lat0*math.pi/180)))
            self.x.append(x1)
            #self.x.append(x2)
            self.y.append(y1)
            #self.y.append(y2)
            
            if i < 1:
                mid_x = (x1 + (x2-x1)/2 + 10)
                mid_y = (y1 + (y2-y1)/2 - 10)
                
            else:
                if Flights[i-1][1] == Flights[i][1] and Flights[i-1][2] == Flights[i][2]:
                    counter += 1
                    
                    #odd
                    if counter%2 == 1:
                        mid_x = (x1 + (x2-x1)/2 + 10*(counter+1))
                        mid_y = (y1 + (y2-y1)/2 -10*(counter+1))
                
                    #even
                    if counter%2 == 0:
                        mid_x = (y1 + (y2-y1)/2 -10*(counter))
                        mid_y = (x1 + (x2-x1)/2 + 10*(counter))
                    #print counter
                else:
                    mid_x = (x1 + (x2-x1)/2 + 10)
                    mid_y = (y1 + (y2-y1)/2 - 10)
                    #print mid_x
            
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            path.moveTo(x1,y1)
            path.lineTo(x1,y1)
            #path.quadTo(mid_x,mid_y,x2,y2)
            path.quadTo(mid_x,mid_y,x2,y2)
            #qp.drawLine(x1,y1,x2,y2)
            qp.drawPath(path)
            
        #This is above
        #pos = self.graph.getAirportPos()
        for i in range(len(pos)):   
            Rx = (9*w/10.3-w/10)/(122.4167-73.8726)
            Ry = (1.97*h/5-h/1.955)/(math.tan(40.7772*math.pi/180)-
                                 math.tan(37.7833*math.pi/180))
            #SF as long0/lat0
            Long0 = 122.4167
            Lat0 = 37.7833
            x = (w/10+Rx*(Long0-pos[i][1]))
            y = (h/1.955+Ry*(math.tan(pos[i][2]*math.pi/180)-
                             math.tan(Lat0*math.pi/180)))
            
            
            City = pos[i][0]
            
            qp.setPen(QColor(255, 255, 255))
            qp.drawText(x, y+10, str(City))
            qp.setBrush(QColor(255,255,0))
            qp.drawEllipse(x-5, y-5, 8, 8)
        #print pos
        #print self.x
        #print self.y
            #qp.drawEllipse(x2-5, y2-5, 8, 8)
        
        #pen = QPen(Qt.black, 2, Qt.SolidLine)
        #qp.setPen(pen)
        #qp.drawText(5, 5,20, 20, Qt.AlignCenter, "Print")
           
        self.draw(qp)

    def drawshortestflight(self, Depart, Dest):
        
        self.shortest_flights = self.graph.drawshortest(Depart, Dest)
        #print self.shortest_flights
        return self.shortest_flights     #this will print correctly here

    def draw(self, qp):  
        
        if self.shortest_flights == []:  
            return
            
        size = self.size()
        h = size.height()
        w = size.width()
        
        Rx = (9*w/10.3-w/10)/(122.4167-73.8726)
        Ry = (1.97*h/5-h/1.955)/(math.tan(40.7772*math.pi/180)-
                                 math.tan(37.7833*math.pi/180))
        #SF as long0/lat0
        Long0 = 122.4167
        Lat0 = 37.7833

        #try:
        for i in range(len(self.shortest_flights)):
            from_longitude = self.shortest_flights[i][3]
            from_latitude = self.shortest_flights[i][4]
                    
            to_longitude = self.shortest_flights[i][5]
            to_latitude = self.shortest_flights[i][6]
                    
            x1 = (w/10+Rx*(Long0-from_longitude))
            y1 = (h/1.955+Ry*(math.tan(from_latitude*math.pi/180)-
                             math.tan(Lat0*math.pi/180)))
                    
            x2 = (w/10+Rx*(Long0-to_longitude))
            y2 = (h/1.955+Ry*(math.tan(to_latitude*math.pi/180)-
                             math.tan(Lat0*math.pi/180)))
                    
            pen = QPen(Qt.red, 3, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(x1,y1,x2,y2)
            
            x_mid = (x1+(x2-x1)/2)
            y_mid = (y1 + (y2-y1)/2)
            Flight = str(self.shortest_flights[i][0])
            
            #qp.setPen(QColor(0, 0, 255))
            qp.drawText(x_mid-10, y_mid-10, str(Flight))
        
    def resetFlights(self):
        self.shortest_flights = []
        
        
        
        
        
        