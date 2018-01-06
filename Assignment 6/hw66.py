# -*- coding: utf-8 -*-
"""
Created on Sat Dec 02 22:16:28 2017

@author: RC
"""

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
from PyQt5.QtGui import QIcon
class Graph(object):
    def __init__(self, database):
   
        try:
            self.db = DBI.connect("/Users/myrc/Downloads/ChenRen_Midterm/Graph.db")
            self.db.text_factory = str
            self.cu = self.db.cursor()
            print "Success"
        except:
            print "failure to access database"
            self.close()
    
    def find_path(self, start, end, path = []):
        if tuple([start]) in self.cu.execute('''SELECT Airport FROM Airports;'''): 
            startID=start
        else:
            return "Departure airport can't be found!"
        if tuple([end]) in self.cu.execute('''SELECT Airport FROM Airports;'''):
            endID=end
        else:
            return "Arrival airport can't be found!"
        path = path + [start]
        
        if startID == endID:
            return [path]

        paths = []
        Ends = self.cu.execute('''SELECT End FROM Flights WHERE Start = '{}';'''.format(start)).fetchall()
        
        for i in np.arange(0, len(Ends)):
            node = list(Ends[i])[0].encode('utf-8') 
            if node not in path:
                branchs = self.find_path(node, endID, path)
                for branch in branchs:
                    paths.append(branch)
        return paths

    # Find all airlines between start and end 
    def find_Airlines(self, start, end):
        paths = self.find_path(start, end)
        allAirlines = []
        for path in paths:
            airlines = []
            for i in np.arange(0, len(path) - 1):
                find_list = self.cu.execute('''SELECT flightnumber FROM Flights WHERE Start = '{}' AND End = '{}';'''\
                                            .format(path[i], path[i + 1])).fetchall()     
                airline_list = []
                for i in np.arange(0,len(find_list)):
                    airline_list = airline_list + [list(find_list[i])[0].encode('utf-8')]
                airlines.append(airline_list)
            allAirlines = allAirlines + [airlines]
            
        return allAirlines
    
    #Find all combinations
    def find_Combine(self, start, end):
        lines = self.find_Airlines(start, end);
        combine_list = []
        for line in lines:
            list1 = list(product(line[0], line[1]))
            list2 = []
            for i in list1:
                str = list(i)               
                if str not in list2:
                    list2.append(str)   
            for j in np.arange(2,len(line)):
                comb_1 = list(product(list2, line[j]))
                comb_2 = []
                for i in comb_1:
                    str = list(i)
                    if str not in comb_2:
                        comb_2.append(str)
                        comb_3 = []
                        for k in comb_2:
                            str1 = i[0] + [k[1]]
                            comb_3.append(str1)
                        list2 = comb_3
            combine_list = combine_list + list2
        return combine_list
    
    global OneDay_Minutes            
    OneDay_Minutes=24*60  
    # Calculate the flight time
    def flight_Time(self, flightnumber):
        dep = list(self.cu.execute('''SELECT Depart FROM Flights WHERE 
                    flightnumber = '{}';'''.format(flightnumber)).fetchone())[0].encode('utf-8')
        arr = list(self.cu.execute('''SELECT Arrival FROM Flights WHERE 
                    flightnumber = '{}';'''.format(flightnumber)).fetchone())[0].encode('utf-8')
                    
        depart_hour, dep_min = dep.split(':')
        arrival_hour, arr_min = arr.split(':')
        depart_time = int(dep_min) + 60 * int(depart_hour)
        arrive_time = int(arr_min) + 60 * int(arrival_hour)
        
        time = 0
        if depart_time < arrive_time:
            time = arrive_time - depart_time
        else:
            time = OneDay_Minutes - depart_time + arrive_time
        
        return time

    # Calculate the layover time for a path
    def Layover_Time(self, StartWait_time, Leave_Time):
    
        Leave_Time_hour, Leave_Time_min = Leave_Time.split(':')
        StartWait_time_hour, StartWait_time_min = StartWait_time.split(':')
        depart_time = int(Leave_Time_min) + 60 * int(Leave_Time_hour)
        arrive_time = int(StartWait_time_min) + 60 * int(StartWait_time_hour)
        
        waiting_time = 0
        # If arrival time < depart time, add one more day
        if arrive_time < depart_time:
            if arrive_time < depart_time - 30:
                waiting_time = depart_time - arrive_time
            else:
                waiting_time = OneDay_Minutes + depart_time - arrive_time
        else:
            waiting_time = OneDay_Minutes + depart_time - arrive_time
        
        return waiting_time
    
    # Calculate the total time
    def total_time(self, start, end):
        combs = self.find_Combine(start, end)
        total_time = []
        
        for comb in combs:
            flight_time = 0
            for i in comb:
                time1 = self.flight_Time(i)
                flight_time += time1
            
            layover_time=0
            for i in np.arange(0, len(comb) - 1):
                st = list(self.cu.execute('''SELECT Arrival FROM Flights WHERE flightnumber = "{}";'''\
                          .format(comb[i])).fetchone())[0].encode('utf-8')
                tt = list(self.cu.execute('''SELECT Depart FROM Flights WHERE flightnumber = "{}";'''\
                          .format(comb[i + 1])).fetchone())[0].encode('utf-8')
            
                time2 = self.Layover_Time(st, tt)
                layover_time += time2
            
            sum_time = flight_time + layover_time
            total_time.append(sum_time)
    
        return total_time

    # Get flight information
    def flight_Info(self, flightnumber):
        info = []

        info_start = list(self.cu.execute('''SELECT Start FROM Flights WHERE flightnumber = '{}';'''\
                                          .format(flightnumber)).fetchall()[0])[0].encode('utf-8')
        info.append(info_start)
            
        info_end = list(self.cu.execute('''SELECT End FROM Flights WHERE flightnumber = '{}';'''\
                                      .format(flightnumber)).fetchall()[0])[0].encode('utf-8')
        info.append(info_end)
            
        info_depart = list(self.cu.execute('''SELECT Depart FROM Flights WHERE flightnumber = '{}';'''\
                                           .format(flightnumber)).fetchall()[0])[0].encode('utf-8')
        info.append(info_depart)
            
        info_arrival = list(self.cu.execute('''SELECT Arrival FROM Flights WHERE flightnumber = '{}';'''\
                                            .format(flightnumber)).fetchall()[0])[0].encode('utf-8')
        info.append(info_arrival)

        return info
   
    # Calculate the shortest time
    def shortest_time(self, start, end):
        airlines = self.find_Combine(start, end)
        total_time = self.total_time(start, end)
        i = total_time.index(min(total_time))
        Airline = airlines[i]
        sum_time = total_time[i]
        
        return [Airline, sum_time]   


f=Graph("/Users/myrc/Downloads/ChenRen_Midterm/Graph.db")
sm=f.shortest_time("SEA", "MIA")
print "The shortest flight between SEA-MIA is through: {}, with shortest time: {} minutes, which is {} hours {} min".format(sm[0],sm[1],sm[1]/60,sm[1]%60)

        
class Airport(QWidget):
    
    def __init__(self, parent):
        
        super(Airport,self).__init__(parent)
        
        self.setGeometry(50,50,500,300)
        self.db = DBI.connect("/Users/myrc/Downloads/ChenRen_Midterm/Graph.db")
        self.cu = self.db.cursor()
        
        
        
        self.initUI()
        
    def initUI(self):
        #self.setWindowTitle(self.title)
        #.setGeometry(self.left, self.top, self.width, self.height)
   
        
        label_1 = QLabel("Departure:",self)
        label_2 = QLabel("Destination:",self)
        
        
        search_airport = 'select Airport from Airports'
        self.db.text_factory = str
        self.cu.execute(search_airport)
        
        data=self.cu.fetchall()
        aa=[]
        
        for item in data:
            aa.append(item[0])
        
        
        self.cbx_dep = QComboBox(self)
        model = QStandardItemModel(0,1)
        for item in aa:
            model.appendRow(QStandardItem(item))
            
        self.cbx_dep.setModel(model)
        self.cbx_dep.currentTextChanged.connect(self.on_destinationChanged)
        
        
        self.cbx_des = QComboBox(self)
        self.cbx_des.setModel(model)
        self.cbx_des.currentTextChanged.connect(self.on_departureChanged)
        
        pbtn_search = QPushButton("search",self)
        pbtn_search.clicked.connect(self.on_search_clicked)
        
        self.result = QTextEdit(self)
        self.result.setText("Ready to Calculate!")
        self.result.setReadOnly(1)
        
        pbtn_reset = QPushButton("Reset View",self)
        pbtn_reset.clicked.connect(self.on_reset_clicked)
    
        
        lyt = QGridLayout()
        lyt.addWidget(label_1,0,0)
        lyt.addWidget(self.cbx_dep,0,1)
        
        lyt.addWidget(label_2,1,0)
        lyt.addWidget(self.cbx_des,1,1)
        
        lyt.addWidget(pbtn_search,2,2,1,1)
        lyt.addWidget(self.result,3,0,8,18)
        lyt.addWidget(pbtn_reset,12,2,1,1)
        
       
        
        # label_1 , label_2,self.cbx_dep,self.cbx_des,pbtn_search,self.result,pbtn_reset
        

        self.setLayout(lyt)
        self.show()
        
    def on_departureChanged(self, s):
        global Dep
        Dep = s
        self.result.setText("")
        
    def on_destinationChanged(self, s):
        global Dest
        Dest = s
        self.result.setText("")
    

    def on_search_clicked(self,event):
        dep = self.cbx_dep.currentText()
        des = self.cbx_des.currentText()
        if dep == des:
            self.result.setText("Error: The destination can't be the same as departure")
        else:
            g=Graph("/Users/myrc/Downloads/ChenRen_Midterm/Graph.db")
            self.method=g.shortest_time(str(dep), str(des))
            self.result.setText("Depart:"+self.cbx_dep.currentText()+"\n"
                            +"Destination:"+self.cbx_des.currentText()+"\n"
                            + "Through Flight:"+str(self.method[0])+"\n"
                            +"Shortest Time:"+str(self.method[1])+"min")

    def on_reset_clicked(self,event):   
        print "reset clicked"
        screen =QDesktopWidget().availableGeometry()
        width=(screen.width()/2)
        height=(screen.height()/2)
        self.window().resize(width,height)

        cp=QDesktopWidget().availableGeometry().center()
        
        fg=self.frameGeometry()
        fg.moveCenter(cp)
        self.window().move(fg.topLeft())
 
class App(QMainWindow):
    
    def __init__(self):
        super(App,self).__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        self.setCentralWidget(Airport(self))
        
        menuBar=self.menuBar()
        menuBar.setNativeMenuBar(False)
        file_menu=menuBar.addMenu('&About')
        about_action=QAction('&Hello! This is the dialog for assignnent 6.',self)
        file_menu.addAction(about_action)
        file_menu=menuBar.addMenu('&Quit')
        exit_action=QAction(QIcon('EXIT.png'),'&Exit',self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit program')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
        #self.statusBar().showMessage('Ready')
        #self.setGeometry(300, 300, 250, 150)
        #self.setWindowTitle('Statusbar')    
        self.show()
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
       


