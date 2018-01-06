'''
Created on Dec 6, 2017

@author: michellesong
'''

import sqlite3 as DBI
import numpy as np
import sys
from itertools import product
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout,\
    QTableWidget, QGroupBox, QRadioButton, QHeaderView, QTableWidgetItem,QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.Qt import QHBoxLayout, QVBoxLayout, QTextEdit, QDesktopWidget,\
    QMenuBar
import sqlite3 as DBI
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize    
#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from Graph import *
from Map import *

class Airport(QWidget):

    def __init__(self):
        super(Airport, self).__init__()
        self.Depart = 'DFW'
        self.Dest = 'DFW'
        
        try:
            self.g = Graph('Graph.db')
            #Graph.db = Graph.Graph('Graph.db')
            #self.db = DBI.connect("/Users/myrc/Downloads/ChenRen_Midterm/Graph.db")
        except:
            print "Failure to access database"
            self.close()
        
        #self.cu = self.db.cursor()
        self.initUI()
        
    def initUI(self):
        
        self.departure = QComboBox(self)
        label_1 = QLabel('Departure:', self.departure)
        model = QStandardItemModel(0,1) 
        
        for item in (self.g.getAirportCodes()):
            model.appendRow(QStandardItem(item))
        self.departure.setModel(model)
        self.departure.currentTextChanged.connect(self.on_departureChanged)

        self.destination = QComboBox(self)
        label_2 = QLabel('Destination:', self.destination)
        model = QStandardItemModel(0,1) 
        
        for item in (self.g.getAirportCodes()):
            model.appendRow(QStandardItem(item))
        self.destination.setModel(model)
        self.destination.currentTextChanged.connect(self.on_destinationChanged)
        
        
        pbtn_reverse = QPushButton("Reverse direction", self)
        pbtn_reverse.clicked.connect(self.on_reverse_clicked)
        
        pbtn_short = QPushButton("Search shortest", self)
        pbtn_short.clicked.connect(self.search_shortest)
        pbtn_all = QPushButton("Search all", self)
        pbtn_all.clicked.connect(self.search_all)
        pbtn_reset = QPushButton("Reset View", self)
        pbtn_reset.clicked.connect(self.reset_view_clicked)
        pbtn_quit = QPushButton("Quit", self)
        pbtn_quit.clicked.connect(self.close)
        
        self.result = QTextEdit(self)
        self.result.setText("Result will be shown here!")
        self.result.setReadOnly(1)
        #self.le_name_2.textChanged.connect(self.on_StudentNameChanged)
        #self.le_name_2.textEdited.connect(self.on_StudentNameChanged)
        
        lyt_1_1 = QHBoxLayout()
        lyt_1_1.addWidget(label_1)
        lyt_1_1.addWidget(self.departure)
        
        lyt_1_2 = QHBoxLayout()
        lyt_1_2.addWidget(label_2)
        lyt_1_2.addWidget(self.destination)
        
        lyt_2_1 = QVBoxLayout()
        lyt_2_1.addLayout(lyt_1_1)
        lyt_2_1.addLayout(lyt_1_2)
        lyt_2_1.addWidget(pbtn_reverse)
        
        lyt_2_2 = QVBoxLayout()
        lyt_2_2.addWidget(pbtn_short)
        lyt_2_2.addWidget(pbtn_all)
        
        lyt_2_3 = QVBoxLayout()
        lyt_2_3.addWidget(pbtn_reset)
        
        lyt_2_4 = QVBoxLayout()
        lyt_2_4.addWidget(pbtn_quit)
        
        lyt_left=QVBoxLayout()
        lyt_left.addLayout(lyt_2_1)
        lyt_left.addLayout(lyt_2_2)
        lyt_left.addLayout(lyt_2_3)
        lyt_left.addLayout(lyt_2_4)
      
        self.map = Map(self)
        #self.map.setGraph(self.g)
        
        self.result.setMaximumHeight(125)
        lyt_right = QVBoxLayout()
        lyt_right.addWidget(self.map)
        lyt_right.addWidget(self.result)
        
        lyt=QHBoxLayout()
        lyt.addLayout(lyt_left)
        lyt.addLayout(lyt_right)
        
        self.setLayout(lyt)
        self.show()
    
    def on_departureChanged(self, depart):
        #global Depart
        self.Depart = depart
        self.result.setText("")
        self.map.resetFlights()
        self.update()
        
    def on_destinationChanged(self, dest):
        #global Dest
        self.Dest = dest
        self.result.setText("")
        self.map.resetFlights()
        self.update()
        
    def on_reverse_clicked(self):
        try:
            t1 = self.Depart
            t2 = self.Dest
            self.departure.setCurrentText(t2)
            self.destination.setCurrentText(t1)
            self.map.resetFlights()
            self.update()
        except:
            self.result.setText('Error: Select Departure and Destination')
            self.map.resetFlights()
       
    def search_shortest(self):
        #print Depart
        #print Dest
        try:
            if self.Depart == self.Dest:
                self.result.setText('Error: Departure airport matches the destination')
                return
            if self.Depart == "IAH":
                #print self.Depart
                self.result.setText('Error: No available flights')
                return
            if self.Dest == "IAH":
                #print self.Dest
                self.result.setText('Error: No available flights')
                return
            else:
                Paths = self.g.findShortestPath(self.Depart, self.Dest)
                self.result.setText(Paths)
    
            allpaths = self.g.findPath(self.Depart, self.Dest)
            nodes = []
            for i in range(len(allpaths)):
                nodes.append(allpaths[i]['nodepath'])
            #global List
            List = []
            for i in range(len(nodes)):
                s = "Flight "
                for j in range(len(nodes[i])):
                    if j < (len(nodes[i]) - 1):
                        s += nodes[i][j] + " to "
                    else:
                        s += nodes[i][j]
                List.append(s)
            #self.g.drawshortest(Depart, Dest)
            self.update()
            self.map.drawshortestflight(self.Depart, self.Dest)
        except:
            self.result.setText('Error: Select Departure and Destination')
            self.map.resetFlights()

    
    def search_all(self):     
        try:
            if self.Depart == self.Dest:
                self.result.setText('Error: Departure airport matches the destination')
                return
            if self.Depart == "IAH" or self.Dest == "IAH":
                self.result.setText('Error: No available flights')
                return
                
            allpaths = self.g.findPath(self.Depart, self.Dest)
            #print Depart
            #print Dest
            #print allpaths[0]['nodepath'][0]
            #print len(allpaths)
            nodes = []
            for i in range(len(allpaths)):
                nodes.append(allpaths[i]['nodepath'])
            #print nodes
            #print nodes[0][1]
            #for i in range(len(nodes)):
            #global List
            List = []
            for i in range(len(nodes)):
                s = "Flight "
                for j in range(len(nodes[i])):
                    if j < (len(nodes[i]) - 1):
                        s += nodes[i][j] + " to "
                    else:
                        s += nodes[i][j]
                List.append(s)
            #self.result.setText(s)
            new_list = np.column_stack((List))
            self.result.setText(str(new_list))
            
            self.map.resetFlights()
            self.update()
            #print pic.width()
        except:
            self.result.setText('Error: Select Departure and Destination')
            self.map.resetFlights()

    def reset_view_clicked(self):
        screen = QDesktopWidget().availableGeometry()
        width = (2*screen.width()/3)
        height = (2*screen.height()/3)
        self.resize(width, height)

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        fg = self.frameGeometry()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

        #print self.g.ListofFlights()
        #print self.g.ShortestPath(Depart, Dest)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Airport()
    sys.exit(app.exec_())