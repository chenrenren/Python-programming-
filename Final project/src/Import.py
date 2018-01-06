'''
Created on Nov 14, 2017

@author: michellesong
'''


import sqlite3 as dbi
import sys
#import pandas as pd

#counters for primary keys
#AirportKey = 0
CityKey = 0
FlightKey = 0
AirlineKey = 0

def getCityID(db, Name, State):
    cu = db.cursor()
    sql = """select CityID from Cities 
           where Name='{}' and State='{}'"""
    cu.execute(sql.format(Name, State))
    CityID=cu.fetchone()
    return CityID

def createCityEntry(db, CityID, Name, State):
    entry = getCityID(db, Name, State)
    cu = db.cursor()
    sql = """insert into Cities (CityID, Name, State)
                     values ({}, '{}', '{}')"""
    if entry == None:
        cu.execute(sql.format(CityID, Name, State))

'''
def getAirportID(db, AirportCode, CityID, Longitude,
              Latitude, X, Y):
    cu = db.cursor()
    sql = """select AirportID from Airport 
           where AirportCode='{}' and CityID={} and Longitude={} 
           and Latitude={} and X={} and Y={}"""
    cu.execute(do.format(Name, State))
    AirportID=cu.fetchone()
    return AirportID
'''
        
def createAirportEntry(db, AirportID, CityID, Longitude, Latitude, X, Y):
    cu = db.cursor()
    sql = """insert into Airport (AirportID, CityID, Longitude, 
            Latitude, X, Y) values ('{}', {}, {}, {}, {}, {})"""

    cu.execute(sql.format(AirportID, CityID, Longitude, Latitude, X, Y))

def getAirlineID(db, Operator):
    cu = db.cursor()
    sql = """select AirlineID from Airlines 
           where Operator='{}'"""
    cu.execute(sql.format(Operator))
    AirlineID = cu.fetchone()
    return AirlineID    

def createAirlineEntry(db, AirlineID, Operator):
    a = getAirlineID(db, Operator)
    sql = """insert into Airlines (AirlineID, Operator)
                     values ({}, '{}')"""
    cu = db.cursor()
    if a == None:
        cu.execute(sql.format(AirlineID, Operator))
'''    
def getFlightID(db, FlightNum, OperatorID, 
                FromCity, ToCity, DepartureTime, ArrivalTime, TripTime):
    cu = db.cursor()
    sql = """select FlightID from Flights 
           where FlightNum='{}' and OperatorID={} and FromCity='{}' 
           and ToCity='{}' and DepartureTime={} and ArrivalTime={} 
           and TripTime={}"""
    cu.execute(sql.format(Operator))
    AirlineID = cu.fetchone()
    return AirlineID         
'''
        
def createFlightEntry(db, FlightID, FlightNum, OperatorID, 
                      FromCity, ToCity, DepartureTime, ArrivalTime, TripTime):
    cu=db.cursor()
    sql="""insert into Flights (FlightID, FlightNum, OperatorID, 
                    FromCity, ToCity, DepartureTime, ArrivalTime, TripTime)
                    values ({}, '{}', {}, '{}', '{}', {}, {}, {})"""
    cu.execute(sql.format(FlightID, FlightNum, OperatorID, 
                    FromCity, ToCity, DepartureTime, ArrivalTime, TripTime))




##########################
filename1 = "Airports.txt"
#filename1 = "AirportData.csv"

#connect to db
db = dbi.connect('Graph.db')

#open file   
try:
    file1 = open(filename1,'rU')
    #Lines = file1.readlines()
    #file1 = pd.read_excel('../RawData_update3.xlsx', sheetname = 'Airport Data')
except IOError:
    print 'Failed to open AirportData.txt'
    sys.exit()

#print Lines 
cursor = db.cursor()
#header = file1.splitlines().readline().split('\t')
header = file1.readline().split('\t')
print header
#print header1

for line in file1:
    line = line.split('\t')
    for i in range(3,len(line)):
            line[i] = float(line[i])
    CityKey += 1
    createCityEntry(db, CityKey, line[1], line[2])
    
    #find the cityID and store in cID
    sql="""select CityID From Cities
               where Name= '{}' and State = '{}'"""
    cursor.execute(sql.format(line[1], line[2]))
    cID=cursor.fetchone()[0]

    createAirportEntry(db, line[0], cID, line[3], line[4], line[5], line[6])
file1.close()

#filename2="Flight Data.txt"
filename2 = "FlightData.txt"
#open file

try:
    file2 = open(filename2,'rU')
except IOError:
    print 'Failed to open Flight Data.txt'
    sys.exit()

header = file2.readline().split('\t')
print header
    
for line in file2:
    line = line.split('\t')
    FlightKey += 1
    AirlineKey += 1
    createAirlineEntry(db, AirlineKey, line[1])

    sql="""select AirlineID From Airlines
               where Operator = '{}'"""
    cursor.execute(sql.format(line[1]))
    opID=cursor.fetchone()[0]
    
    #get the hour and minutes of departTime and arrivalTime
    departTime = line[4].split(':')
    arriveTime = line[5].split(':')
    #Turn times into minutes
    departTime = int(departTime[0])*60+int(departTime[1])
    arriveTime = int(arriveTime[0])*60+int(arriveTime[1])
    
    #To take into account redeyes 
    if arriveTime < departTime:
        arriveTime += int(24*60)
        
    #Calculate the TripTime
    TT = arriveTime-departTime
    createFlightEntry(db, FlightKey, line[0], opID, line[2], line[3], 
                      departTime, arriveTime, TT)

db.commit()
db.close()

            



