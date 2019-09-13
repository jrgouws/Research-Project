# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:15:31 2019

@author: project
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

doTrace = True

linkCapacity = 1*10**6

class Packet:
    def __init__(self, size, arrivalTime, priority):
        self.size        = size
        self.arrivalTime = arrivalTime
        self.processed   = 0
        self.completed   = False
        self.priority    = priority

# Read the text file and the inter-arrival time and the size
def readCSV(filePath):
    arrival = []
    size = []
    
    with open(filePath,'r') as f:
        data = csv.reader(f)
        for row in data:
            arrival.append(row[0])
            size.append(row[1])
    
    # Convert the strings lists to integer lists
    arrival = list(map(int, arrival))
    size = list(map(int, size))

    return arrival, size

# Takes the packets as a list of two lists corrensponding to  
# [[class:packetLowPriority], class[packetHighPriority]] and the transmission 
# capacity as an integer and returns arrivalTimes, transTimes, queuingDelays,
# startEnd, idleTimes, respTimes.
def calculateParameters(transCap, packets):
    arrivalTimes     = [[],[]]
    transTimes       = [[],[]]
    queuingDelays    = [[],[]]   
    startEnd         = [[],[]]
    idleTimes        = [[],[]]
    respTimes        = [[],[]]
    currTime         = 0
    
    # Calculate when the packets were received for low priority
    for i in range(0, len(packets[0])):
        if (i == 0):
            arrivalTimes[0].append(packets[0][i].arrivalTime)
            
        else:
            arrivalTimes[0].append(packets[0][i].arrivalTime + arrivalTimes[0][i - 1])
            
    # Calculate when the packets were received for high priority
    for i in range(0, len(packets[1])):
        if (i == 0):
            arrivalTimes[1].append(packets[1][i].arrivalTime)
            
        else:
            arrivalTimes[1].append(packets[1][i].arrivalTime + arrivalTimes[1][i - 1])
    
    # Calculate how long each packet takes to transmit for low priority
    for i in range(0, len(packets[0])):
        transTimes[0].append(packets[0][i].size/transCap)
    
    # Calculate how long each packet takes to transmit for high priority
    for i in range(0, len(packets[1])):
        transTimes[1].append(packets[1][i].size/transCap)
    
    
    
    '''
    # Calculate the delay for each packet
    for i in range(len(interArrival)):
        
        # If the first packet is received
        if (i == 0):
            currTime += arrivalTimes[i] + transTimes[i]
            startEnd.append([arrivalTimes[i], currTime])
            idleTimes.append(0)
            queuingDelays.append(0)
        
        # If a packet is received and the server is on idle    
        elif (arrivalTimes[i] > currTime):
            idleTimes.append(arrivalTimes[i] - currTime)
            currTime = arrivalTimes[i] + transTimes[i]
            startEnd.append([arrivalTimes[i], currTime])
            queuingDelays.append(0)
            
        # If a server has received a new packet at the same time as finishing the old    
        elif (arrivalTimes[i] == currTime):
            currTime += transTimes[i]
            startEnd.append([arrivalTimes[i], currTime])
            idleTimes.append(0)
            queuingDelays.append(0)
            
        # If a packet is received and the server is currently busy
        else:
            startEnd.append([currTime, currTime + transTimes[i]])
            queuingDelays.append(currTime - arrivalTimes[i])
            currTime += transTimes[i]
            idleTimes.append(0)
            
    # Calculate the reponse times for each of the packets
    for i in range(len(startEnd)):
        respTimes.append(startEnd[i][1] - startEnd[i][0] + queuingDelays[i])
    ''' 
    return arrivalTimes, transTimes, queuingDelays, startEnd, idleTimes, respTimes




if (doTrace == True):
    print("##################################################################")
    print("########        Processing High Priority Trace file        #######")
    print("##################################################################")
    
    packets = [[],[]]      
    allQueues = []
    time = []
    
    transCap = linkCapacity
    
    # Read the csv file data into respective lists to store the data
    interArrivalHigh, packetSizeHigh = readCSV('HighPriority.txt')
    interArrivalLow , packetSizeLow  = readCSV('LowPriority.txt')
    
    # Create the list of low priority packets
    for i in range(0, len(interArrivalLow)):
        lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
        packets[0].append(lowPacket)
    
    # Create the list of high priority packets
    for i in range(0, len(interArrivalHigh)):
        highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
        packets[1].append(highPacket)
    
    # Get the parameters            arrLow, sizeLow, arrHigh, sizeHigh, transCap
    arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(transCap, packets)
    sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
    print("Link capacity --------------------------", transCap/10**6, "Mbps") 
    print("Number of low priority packets ---------", len(packetSizeLow), "packets")
    print("Number of high priority packets --------", len(packetSizeHigh), "packets")
    print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
    print("Average inter-arrival time -- (LOW) ----", round((sum(interArrivalLow))/(len(interArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(interArrivalHigh))/(len(interArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(interArrivalHigh) + sum(interArrivalLow))/(len(interArrivalHigh) + len(interArrivalLow)), 4), "us" )
    #print("Average transmission time --- (LOW) ----", sum(transTimes)/len(transTimes), "us" )
    #print("Average response time -----------------", sum(respTimes)/len(respTimes), "us" )
    print("The average packet size ----- (LOW) ----", round(sizeAvg[0], 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sizeAvg[1], 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(packetSizeLow) + sum(packetSizeHigh)) / (float(len(packetSizeLow)) + float(len(packetSizeHigh))),4), "bits" )

    #print("Average delays ------------------------", sum(queuingDelays)/len(queuingDelays), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(packetSizeLow))/((sum(interArrivalLow))/10**6), 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(packetSizeHigh))/((sum(interArrivalHigh))/10**6), 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/((sum(interArrivalHigh) + sum(interArrivalLow))/10**6), 4), "packets/second")
    #print("Average service rate (mu) -------------", transCap/sizeAvg)
