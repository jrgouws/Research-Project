# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:15:31 2019

@author: project
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

doNonPreemptiveTrace        = False
doPreemptiveTrace           = False
doNoPriority                = False
doAveragePreemptive         = False
doAverageNonPreemptive      = False
doAverageNoPriority         = False
doVaryingArrivalPreempt     = False
doVaryingArrivalNonPreempt  = True
doVaryingArrivalNoPriority  = False

averagedOver = 10

arrRates = [200,300,400,500,600]

linkCapacity = 1*10**6

class Packet:
    def __init__(self, size, interArrivalTime, priority):
        self.size             = size             
        self.interArrivalTime = interArrivalTime 
        self.priority         = priority         
        self.arrivalTime      = 0                
        self.transTime        = 0                 
        self.queueDelay       = 0
        self.startTime        = 0
        self.endTime          = 0
        self.responseTime     = 0
 
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
def calcNonPreemptive(transCap, packets):
    currTime         = 0
    completedPackets = []
    
    # Calculate when the packets were received for low priority
    for i in range(0, len(packets[0])):
        if (i == 0):
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime
            
        else:
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime + packets[0][i - 1].arrivalTime
            
    # Calculate when the packets were received for high priority
    for i in range(0, len(packets[1])):
        if (i == 0):
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime
            
        else:
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime + packets[1][i - 1].arrivalTime
    
    # Calculate how long each packet takes to transmit for low priority
    for i in range(0, len(packets[0])):
        packets[0][i].transTime = (packets[0][i].size/transCap)*10**6
    
    # Calculate how long each packet takes to transmit for high priority
    for i in range(0, len(packets[1])):
        packets[1][i].transTime = (packets[1][i].size/transCap)*10**6
           
    while (len(packets[0]) > 0 or len(packets[1]) > 0):
        # For the first packet arriving
        toProcess = None
        
        # If a high priority packet was received
        if (len(packets[1]) > 0 and packets[1][0].arrivalTime <= currTime):
            toProcess = packets[1][0]
            packets[1] = packets[1][1:]
            
        # If a low priority packet was received and no high priority
        elif (len(packets[0]) > 0 and packets[0][0].arrivalTime <= currTime):
            toProcess = packets[0][0]
            packets[0] = packets[0][1:]
            
        # If server is idle, get the next packet and update the packet to
        # the corresponding arrival time
        else:
            # If there are still packets to be processed of high and low priority
            if (len(packets[1]) > 0 and len(packets[0]) > 0):
                if (packets[1][0].arrivalTime <= packets[0][0].arrivalTime):
                    toProcess = packets[1][0]
                    currTime = packets[1][0].arrivalTime
                    packets[1] = packets[1][1:]
                    
                    
                else:
                    toProcess = packets[0][0]
                    currTime = packets[0][0].arrivalTime
                    packets[0] = packets[0][1:]
                    
            elif (len(packets[1]) > 0):
                toProcess = packets[1][0]
                currTime = packets[1][0].arrivalTime
                packets[1] = packets[1][1:]
            
            elif (len(packets[0]) > 0):
                toProcess = packets[0][0]
                currTime = packets[0][0].arrivalTime
                packets[0] = packets[0][1:]
           
        if (toProcess != None):
            # Process all the packets that has arrived
            toProcess.startTime  = currTime
            toProcess.endTime    = currTime + toProcess.transTime
            toProcess.queueDelay = currTime - toProcess.arrivalTime
            completedPackets.append(toProcess)
            currTime = toProcess.endTime
            toProcess = None
            
    # Calculate the reponse times for each of the packets
    for i in range(len(completedPackets)):
        completedPackets[i].responseTime = completedPackets[i].endTime - completedPackets[i].startTime + completedPackets[i].queueDelay

    arrivalTimes   = [[],[]] 
    transTimes     = [[],[]] 
    queuingDelays  = [[],[]] 
    startEnd       = [[],[]] 
    respTimes      = [[],[]]


    for i in range(0, len(completedPackets)):
        if (completedPackets[i].priority == "HIGH"):
            arrivalTimes[1].append(completedPackets[i].arrivalTime)
            transTimes[1].append(completedPackets[i].transTime)
            queuingDelays[1].append(completedPackets[i].queueDelay)
            startEnd[1].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[1].append(completedPackets[i].responseTime)
            
        elif (completedPackets[i].priority == "LOW"):
            arrivalTimes[0].append(completedPackets[i].arrivalTime)
            transTimes[0].append(completedPackets[i].transTime)
            queuingDelays[0].append(completedPackets[i].queueDelay)
            startEnd[0].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[0].append(completedPackets[i].responseTime)

    return arrivalTimes, transTimes, queuingDelays, startEnd, respTimes, completedPackets

# Takes the packets as a list of two lists corrensponding to  
# [[class:packetLowPriority], class[packetHighPriority]] and the transmission 
# capacity as an integer and returns arrivalTimes, transTimes, queuingDelays,
# startEnd, idleTimes, respTimes.
def calcPreemptive(transCap, packets):
    currTime         = 0
    completedPackets = []
    
    # Calculate when the packets were received for low priority
    for i in range(0, len(packets[0])):
        if (i == 0):
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime
            
        else:
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime + packets[0][i - 1].arrivalTime
            
    # Calculate when the packets were received for high priority
    for i in range(0, len(packets[1])):
        if (i == 0):
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime
            
        else:
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime + packets[1][i - 1].arrivalTime
    
    # Calculate how long each packet takes to transmit for low priority
    for i in range(0, len(packets[0])):
        packets[0][i].transTime = (packets[0][i].size/transCap)*10**6
    
    # Calculate how long each packet takes to transmit for high priority
    for i in range(0, len(packets[1])):
        packets[1][i].transTime = (packets[1][i].size/transCap)*10**6
           
    while (len(packets[0]) > 0 or len(packets[1]) > 0):
        # For the first packet arriving
        toProcess = None
        
        # If a high priority packet was received
        if (len(packets[1]) > 0 and packets[1][0].arrivalTime <= currTime):
            toProcess = packets[1][0]
            packets[1] = packets[1][1:]
            
        # If a low priority packet was received and no high priority
        elif (len(packets[0]) > 0 and packets[0][0].arrivalTime <= currTime):
            toProcess = packets[0][0]
            
        # If server is idle, get the next packet and update the packet to
        # the corresponding arrival time
        else:
            # If there are still packets to be processed of high and low priority
            if (len(packets[1]) > 0 and len(packets[0]) > 0):
                if (packets[1][0].arrivalTime <= packets[0][0].arrivalTime):
                    toProcess = packets[1][0]
                    currTime = packets[1][0].arrivalTime
                    packets[1] = packets[1][1:]
                    
                    
                else:
                    toProcess = packets[0][0]
                    currTime = packets[0][0].arrivalTime
                    
            elif (len(packets[1]) > 0):
                toProcess = packets[1][0]
                currTime = packets[1][0].arrivalTime
                packets[1] = packets[1][1:]
            
            elif (len(packets[0]) > 0):
                toProcess = packets[0][0]
                currTime = packets[0][0].arrivalTime
           
        if (toProcess != None):
            toProcess.startTime  = currTime
            toProcess.endTime    = currTime + toProcess.transTime
            toProcess.queueDelay = currTime - toProcess.arrivalTime
            currTime = toProcess.endTime
            
            # Process all the packets that has arrived
            if (toProcess.priority == "LOW"):
                if (len(packets[1]) > 0 and currTime > packets[1][0].arrivalTime):
                    currTime = packets[1][0].arrivalTime
                    toProcess = None
                    continue
                
                else:
                    packets[0] = packets[0][1:]
            
            completedPackets.append(toProcess)
            
    # Calculate the reponse times for each of the packets
    for i in range(len(completedPackets)):
        completedPackets[i].responseTime = completedPackets[i].endTime - completedPackets[i].startTime + completedPackets[i].queueDelay

    arrivalTimes   = [[],[]] 
    transTimes     = [[],[]] 
    queuingDelays  = [[],[]] 
    startEnd       = [[],[]] 
    respTimes      = [[],[]]


    for i in range(0, len(completedPackets)):
        if (completedPackets[i].priority == "HIGH"):
            arrivalTimes[1].append(completedPackets[i].arrivalTime)
            transTimes[1].append(completedPackets[i].transTime)
            queuingDelays[1].append(completedPackets[i].queueDelay)
            startEnd[1].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[1].append(completedPackets[i].responseTime)
            
        elif (completedPackets[i].priority == "LOW"):
            arrivalTimes[0].append(completedPackets[i].arrivalTime)
            transTimes[0].append(completedPackets[i].transTime)
            queuingDelays[0].append(completedPackets[i].queueDelay)
            startEnd[0].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[0].append(completedPackets[i].responseTime)

    return arrivalTimes, transTimes, queuingDelays, startEnd, respTimes, completedPackets

# Takes the packets as a list of two lists corrensponding to  
# [[class:packetLowPriority], class[packetHighPriority]] and the transmission 
# capacity as an integer and returns arrivalTimes, transTimes, queuingDelays,
# startEnd, idleTimes, respTimes.
def calcNoPriority(transCap, packets):
    
    currTime         = 0
    completedPackets = []
    
    # Calculate when the packets were received for low priority
    for i in range(0, len(packets[0])):
        if (i == 0):
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime
            
        else:
            packets[0][i].arrivalTime = packets[0][i].interArrivalTime + packets[0][i - 1].arrivalTime
            
    # Calculate when the packets were received for high priority
    for i in range(0, len(packets[1])):
        if (i == 0):
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime
            
        else:
            packets[1][i].arrivalTime = packets[1][i].interArrivalTime + packets[1][i - 1].arrivalTime
    
    # Calculate how long each packet takes to transmit for low priority
    for i in range(0, len(packets[0])):
        packets[0][i].transTime = (packets[0][i].size/transCap)*10**6
    
    # Calculate how long each packet takes to transmit for high priority
    for i in range(0, len(packets[1])):
        packets[1][i].transTime = (packets[1][i].size/transCap)*10**6
           
    while (len(packets[0]) > 0 or len(packets[1]) > 0):
        # For the first packet arriving
        toProcess = None
        
        if (len(packets[1]) > 0 and len(packets[0]) > 0 and packets[1][0].arrivalTime <= currTime and packets[0][0].arrivalTime <= currTime):
            if (packets[1][0].arrivalTime <= packets[0][0].arrivalTime):
                toProcess = packets[1][0]
                packets[1] = packets[1][1:]
                
            else:
                toProcess = packets[0][0]
                packets[0] = packets[0][1:]
        
        # If a high priority packet was received
        elif (len(packets[1]) > 0 and packets[1][0].arrivalTime <= currTime):
            toProcess = packets[1][0]
            packets[1] = packets[1][1:]
            
        # If a low priority packet was received and no high priority
        elif (len(packets[0]) > 0 and packets[0][0].arrivalTime <= currTime):
            toProcess = packets[0][0]
            packets[0] = packets[0][1:]
            
        # If server is idle, get the next packet and update the packet to
        # the corresponding arrival time
        else:
            # If there are still packets to be processed of high and low priority
            if (len(packets[1]) > 0 and len(packets[0]) > 0):
                if (packets[1][0].arrivalTime < packets[0][0].arrivalTime):
                    toProcess = packets[1][0]
                    currTime = packets[1][0].arrivalTime
                    packets[1] = packets[1][1:]
                    
                    
                else:
                    toProcess = packets[0][0]
                    currTime = packets[0][0].arrivalTime
                    packets[0] = packets[0][1:]
                    
            elif (len(packets[1]) > 0):
                toProcess = packets[1][0]
                currTime = packets[1][0].arrivalTime
                packets[1] = packets[1][1:]
            
            elif (len(packets[0]) > 0):
                toProcess = packets[0][0]
                currTime = packets[0][0].arrivalTime
                packets[0] = packets[0][1:]
           
        if (toProcess != None):
            # Process all the packets that has arrived
            toProcess.startTime  = currTime
            toProcess.endTime    = currTime + toProcess.transTime
            toProcess.queueDelay = currTime - toProcess.arrivalTime
            completedPackets.append(toProcess)
            currTime = toProcess.endTime
            toProcess = None
            
    # Calculate the reponse times for each of the packets
    for i in range(len(completedPackets)):
        completedPackets[i].responseTime = completedPackets[i].endTime - completedPackets[i].startTime + completedPackets[i].queueDelay

    arrivalTimes   = [[],[]] 
    transTimes     = [[],[]] 
    queuingDelays  = [[],[]] 
    startEnd       = [[],[]] 
    respTimes      = [[],[]]


    for i in range(0, len(completedPackets)):
        if (completedPackets[i].priority == "HIGH"):
            arrivalTimes[1].append(completedPackets[i].arrivalTime)
            transTimes[1].append(completedPackets[i].transTime)
            queuingDelays[1].append(completedPackets[i].queueDelay)
            startEnd[1].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[1].append(completedPackets[i].responseTime)
            
        elif (completedPackets[i].priority == "LOW"):
            arrivalTimes[0].append(completedPackets[i].arrivalTime)
            transTimes[0].append(completedPackets[i].transTime)
            queuingDelays[0].append(completedPackets[i].queueDelay)
            startEnd[0].append([completedPackets[i].startTime, completedPackets[i].endTime])
            respTimes[0].append(completedPackets[i].responseTime)

    return arrivalTimes, transTimes, queuingDelays, startEnd, respTimes, completedPackets

if (doNoPriority == True):
    print("##################################################################")
    print("########        Processing no priority queuing             #######")
    print("##################################################################")
    
    packets = [[],[]]      
    time = []
    
    transCap = linkCapacity
    
    # Read the csv file data into respective lists to store the data
    interArrivalHigh, packetSizeHigh = readCSV('HighPriority.txt')
    interArrivalLow , packetSizeLow  = readCSV('LowPriority.txt')
    
    print(len(interArrivalHigh), len(interArrivalLow))
    
    # Create the list of low priority packets
    for i in range(0, len(interArrivalLow)):
        lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
        packets[0].append(lowPacket)
    
    # Create the list of high priority packets
    for i in range(0, len(interArrivalHigh)):
        highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
        packets[1].append(highPacket)
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcNoPriority(transCap, packets)
    sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
    print("Link capacity --------------------------", transCap/10**6, "Mbps") 
    print("Number of low priority packets ---------", len(packetSizeLow), "packets")
    print("Number of high priority packets --------", len(packetSizeHigh), "packets")
    print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
    print("Average inter-arrival time -- (LOW) ----", round((sum(interArrivalLow))/(len(interArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(interArrivalHigh))/(len(interArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(interArrivalHigh) + sum(interArrivalLow))/(len(interArrivalHigh) + len(interArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(transTimes[0])/len(transTimes[0]), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(transTimes[1])/len(transTimes[1]), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(transTimes[1]) + sum(transTimes[0]))/(len(transTimes[1])+len(transTimes[0])), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(respTimes[0])/len(respTimes[0]), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(respTimes[1])/len(respTimes[1]), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(respTimes[0]) + sum(respTimes[1]))/(len(respTimes[0]) + len(respTimes[1])), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sizeAvg[0], 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sizeAvg[1], 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(packetSizeLow) + sum(packetSizeHigh)) / (float(len(packetSizeLow)) + float(len(packetSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(queuingDelays[0])/len(queuingDelays[0]), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(queuingDelays[1])/len(queuingDelays[1]), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(queuingDelays[0]) + sum(queuingDelays[1]))/(len(queuingDelays[0]) + len(queuingDelays[1])), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(packetSizeLow))/((sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(packetSizeHigh))/((sum(interArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/((sum(interArrivalHigh) + sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/sizeAvg[0], 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/sizeAvg[1], 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sizeAvg[0] + sizeAvg[1])/2), 4), "packets/second")

    
    startEnd = [[],[]]
    arrivalTimes = []
    startEndLow = [[],[]]
    arrivalTimesLow = []
    startEndHigh = [[],[]]
    arrivalTimesHigh = []
    
    for i in allPackets:
        startEnd[0].append(i.startTime)
        startEnd[1].append(i.endTime)
        arrivalTimes.append(i.arrivalTime)    
        
        if (i.priority == 'LOW'):
            startEndLow[0].append(i.startTime)
            startEndLow[1].append(i.endTime)
            arrivalTimesLow.append(i.arrivalTime)    
        
        if (i.priority == 'HIGH'):
            startEndHigh[0].append(i.startTime)
            startEndHigh[1].append(i.endTime)
            arrivalTimesHigh.append(i.arrivalTime)    
            
    time = np.arange(0, startEnd[1][-1], 10000)
    combined = []
    lowPriority = []
    highPriority = []
    
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimes)):
            if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                if (startEnd[0][j] > arrivalTimes[j]):
                    length += 1
        combined.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesLow)):
            if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                if (startEndLow[0][j] > arrivalTimesLow[j]):
                    length += 1
        lowPriority.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesHigh)):
            if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                    length += 1
        highPriority.append(length)
        
        
    time = time/10**6            
            
    plt.figure()
    plt.plot(time, combined, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of packets waiting in an M/M/1 queue with no priority')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority trace file packets'))
    plt.plot(time, highPriority, label=str('High Priority trace file packets'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of packets from each trace file waiting in an M/M/1 queue with no priority')
    plt.show()

    
if (doNonPreemptiveTrace == True):
    print("##################################################################")
    print("########        Processing non-preemptive queuing          #######")
    print("##################################################################")
    
    packets = [[],[]]      
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
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcNonPreemptive(transCap, packets)
    sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
    print("Link capacity --------------------------", transCap/10**6, "Mbps") 
    print("Number of low priority packets ---------", len(packetSizeLow), "packets")
    print("Number of high priority packets --------", len(packetSizeHigh), "packets")
    print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
    print("Average inter-arrival time -- (LOW) ----", round((sum(interArrivalLow))/(len(interArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(interArrivalHigh))/(len(interArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(interArrivalHigh) + sum(interArrivalLow))/(len(interArrivalHigh) + len(interArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(transTimes[0])/len(transTimes[0]), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(transTimes[1])/len(transTimes[1]), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(transTimes[1]) + sum(transTimes[0]))/(len(transTimes[1])+len(transTimes[0])), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(respTimes[0])/len(respTimes[0]), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(respTimes[1])/len(respTimes[1]), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(respTimes[0]) + sum(respTimes[1]))/(len(respTimes[0]) + len(respTimes[1])), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sizeAvg[0], 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sizeAvg[1], 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(packetSizeLow) + sum(packetSizeHigh)) / (float(len(packetSizeLow)) + float(len(packetSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(queuingDelays[0])/len(queuingDelays[0]), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(queuingDelays[1])/len(queuingDelays[1]), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(queuingDelays[0]) + sum(queuingDelays[1]))/(len(queuingDelays[0]) + len(queuingDelays[1])), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(packetSizeLow))/((sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(packetSizeHigh))/((sum(interArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/((sum(interArrivalHigh) + sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/sizeAvg[0], 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/sizeAvg[1], 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sizeAvg[0] + sizeAvg[1])/2), 4), "packets/second")

    
    startEnd = [[],[]]
    arrivalTimes = []
    startEndLow = [[],[]]
    arrivalTimesLow = []
    startEndHigh = [[],[]]
    arrivalTimesHigh = []
    
    for i in allPackets:
        startEnd[0].append(i.startTime)
        startEnd[1].append(i.endTime)
        arrivalTimes.append(i.arrivalTime)    
        
        if (i.priority == 'LOW'):
            startEndLow[0].append(i.startTime)
            startEndLow[1].append(i.endTime)
            arrivalTimesLow.append(i.arrivalTime)    
        
        if (i.priority == 'HIGH'):
            startEndHigh[0].append(i.startTime)
            startEndHigh[1].append(i.endTime)
            arrivalTimesHigh.append(i.arrivalTime)    
            
    time = np.arange(0, startEnd[1][-1], 10000)
    combined = []
    lowPriority = []
    highPriority = []
    
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimes)):
            if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                if (startEnd[0][j] > arrivalTimes[j]):
                    length += 1
        combined.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesLow)):
            if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                if (startEndLow[0][j] > arrivalTimesLow[j]):
                    length += 1
        lowPriority.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesHigh)):
            if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                    length += 1
        highPriority.append(length)
        
        
    time = time/10**6            
            
    plt.figure()
    plt.plot(time, combined, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs combined number of packets waiting in an M/M/1 queue with non-preemptive queues')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority 1 Mbps'))
    plt.plot(time, highPriority, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of low- and high-priority packets waiting in an M/M/1 queue with non-preemptive queues')
    plt.show()
    

if (doPreemptiveTrace == True):
    print("##################################################################")
    print("########            Processing preemptive queuing          #######")
    print("##################################################################")
    
    packets = [[],[]]      
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
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcPreemptive(transCap, packets)
    sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
    print("Link capacity --------------------------", transCap/10**6, "Mbps") 
    print("Number of low priority packets ---------", len(packetSizeLow), "packets")
    print("Number of high priority packets --------", len(packetSizeHigh), "packets")
    print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
    print("Average inter-arrival time -- (LOW) ----", round((sum(interArrivalLow))/(len(interArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(interArrivalHigh))/(len(interArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(interArrivalHigh) + sum(interArrivalLow))/(len(interArrivalHigh) + len(interArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(transTimes[0])/len(transTimes[0]), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(transTimes[1])/len(transTimes[1]), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(transTimes[1]) + sum(transTimes[0]))/(len(transTimes[1])+len(transTimes[0])), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(respTimes[0])/len(respTimes[0]), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(respTimes[1])/len(respTimes[1]), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(respTimes[0]) + sum(respTimes[1]))/(len(respTimes[0]) + len(respTimes[1])), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sizeAvg[0], 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sizeAvg[1], 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(packetSizeLow) + sum(packetSizeHigh)) / (float(len(packetSizeLow)) + float(len(packetSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(queuingDelays[0])/len(queuingDelays[0]), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(queuingDelays[1])/len(queuingDelays[1]), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(queuingDelays[0]) + sum(queuingDelays[1]))/(len(queuingDelays[0]) + len(queuingDelays[1])), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(packetSizeLow))/((sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(packetSizeHigh))/((sum(interArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/((sum(interArrivalHigh) + sum(interArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/sizeAvg[0], 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/sizeAvg[1], 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sizeAvg[0] + sizeAvg[1])/2), 4), "packets/second")
    
    startEnd = [[],[]]
    arrivalTimes = []
    startEndLow = [[],[]]
    arrivalTimesLow = []
    startEndHigh = [[],[]]
    arrivalTimesHigh = []
    
    for i in allPackets:
        startEnd[0].append(i.startTime)
        startEnd[1].append(i.endTime)
        arrivalTimes.append(i.arrivalTime)    
        
        if (i.priority == 'LOW'):
            startEndLow[0].append(i.startTime)
            startEndLow[1].append(i.endTime)
            arrivalTimesLow.append(i.arrivalTime)    
        
        if (i.priority == 'HIGH'):
            startEndHigh[0].append(i.startTime)
            startEndHigh[1].append(i.endTime)
            arrivalTimesHigh.append(i.arrivalTime)    
            
    time = np.arange(0, startEnd[1][-1], 10000)
    combined = []
    lowPriority = []
    highPriority = []
    
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimes)):
            if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                if (startEnd[0][j] > arrivalTimes[j]):
                    length += 1
        combined.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesLow)):
            if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                if (startEndLow[0][j] > arrivalTimesLow[j]):
                    length += 1
        lowPriority.append(length)
        
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesHigh)):
            if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                    length += 1
        highPriority.append(length)
        
        
    time = time/10**6            
            
    plt.figure()
    plt.plot(time, combined, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs combined number of customers waiting in an M/M/1 queue with preemptive queues')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority 1 Mbps'))
    plt.plot(time, highPriority, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of low- and high-priority packets waiting in an M/M/1 queue with preemptive queues')
    plt.show()
    
    
if (doAverageNonPreemptive == True):
    print("##################################################################")
    print("########              Averaged Non-preemptive queuing      #######")
    print("##################################################################")
    
    time = np.arange(0, 101*10**6, 100000)      
    
          
    totalInterArrivalLow       = []
    totalInterArrivalHigh      = []
    totalTransmissionLow       = []
    totalTransmissionHigh      = []
    totalResponseLow           = []
    totalResponseHigh          = []
    totalAveragePacketSizeLow  = [] 
    totalAveragePacketSizeHigh = [] 
    totalAverageDelaysLow      = [] 
    totalAverageDelaysHigh     = []
    totalArrivalRateLow        = []
    totalArrivalRateHigh       = [] 
    totalServiceRateLow        = [] 
    totalServiceRateHigh       = []
    allCombinedLengths         = [[]] * averagedOver
    allLengthsHighPriority     = [[]] * averagedOver
    allLengthsLowPriority      = [[]] * averagedOver
          
    for k in range(0, averagedOver):      
        packets = [[],[]]      
        transCap = linkCapacity
        
        # Read the csv file data into respective lists to store the data
        interArrivalHigh = list(np.random.exponential(400 , 40000))            
        packetSizeHigh   = list(np.random.exponential(1000, 40000))
        interArrivalLow  = list(np.random.exponential(500 , 50000))
        packetSizeLow    = list(np.random.exponential(1000, 50000))
        
        # Create the list of low priority packets
        for i in range(0, len(interArrivalLow)):
            lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
            packets[0].append(lowPacket)
        
        # Create the list of high priority packets
        for i in range(0, len(interArrivalHigh)):
            highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
            packets[1].append(highPacket)
        
        # Get the parameters
        arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcNonPreemptive(transCap, packets)
        sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
        if (k == 0):
            print("Link capacity --------------------------", transCap/10**6, "Mbps") 
            print("Number of low priority packets ---------", len(packetSizeLow), "packets")
            print("Number of high priority packets --------", len(packetSizeHigh), "packets")
            print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
        
        totalInterArrivalLow       += interArrivalLow
        totalInterArrivalHigh      += interArrivalHigh
        totalTransmissionLow       += transTimes[0]
        totalTransmissionHigh      += transTimes[1]
        totalResponseLow           += respTimes[0]
        totalResponseHigh          += respTimes[1]
        totalAveragePacketSizeLow  += packetSizeLow 
        totalAveragePacketSizeHigh += packetSizeHigh
        totalAverageDelaysLow      += queuingDelays[0]
        totalAverageDelaysHigh     += queuingDelays[1]
        
        startEnd = [[],[]]
        arrivalTimes = []
        startEndLow = [[],[]]
        arrivalTimesLow = []
        startEndHigh = [[],[]]
        arrivalTimesHigh = []
        
        for i in allPackets:
            startEnd[0].append(i.startTime)
            startEnd[1].append(i.endTime)
            arrivalTimes.append(i.arrivalTime)    
            
            if (i.priority == 'LOW'):
                startEndLow[0].append(i.startTime)
                startEndLow[1].append(i.endTime)
                arrivalTimesLow.append(i.arrivalTime)    
            
            if (i.priority == 'HIGH'):
                startEndHigh[0].append(i.startTime)
                startEndHigh[1].append(i.endTime)
                arrivalTimesHigh.append(i.arrivalTime)    
        
        combined = []
        lowPriority = []
        highPriority = []
        
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimes)):
                if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                    if (startEnd[0][j] > arrivalTimes[j]):
                        length += 1
            combined.append(length)
       
        allCombinedLengths[k] = deepcopy(combined)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesLow)):
                if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                    if (startEndLow[0][j] > arrivalTimesLow[j]):
                        length += 1
            lowPriority.append(length)
            
        allLengthsLowPriority[k] = deepcopy(lowPriority)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesHigh)):
                if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                    if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                        length += 1
            highPriority.append(length)
            
        allLengthsHighPriority[k] = deepcopy(highPriority)       
    
    print("Average inter-arrival time -- (LOW) ----", round((sum(totalInterArrivalLow))/(len(totalInterArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(totalInterArrivalHigh))/(len(totalInterArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow))/(len(totalInterArrivalHigh) + len(totalInterArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(totalTransmissionLow)/len(totalTransmissionLow), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(totalTransmissionHigh)/len(totalTransmissionHigh), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(totalTransmissionHigh) + sum(totalTransmissionLow))/(len(totalTransmissionHigh)+len(totalTransmissionLow)), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(totalResponseLow)/len(totalResponseLow), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(totalResponseHigh)/len(totalResponseHigh), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(totalResponseLow) + sum(totalResponseHigh))/(len(totalResponseLow) + len(totalResponseHigh)), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow), 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh), 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)) / (float(len(totalAveragePacketSizeLow)) + float(len(totalAveragePacketSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(totalAverageDelaysLow)/len(totalAverageDelaysLow), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(totalAverageDelaysHigh)/len(totalAverageDelaysHigh), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(totalAverageDelaysLow) + sum(totalAverageDelaysHigh))/(len(totalAverageDelaysHigh) + len(totalAverageDelaysLow)), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(totalAveragePacketSizeLow))/((sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(totalAveragePacketSizeLow) + len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)), 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)), 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh))/2), 4), "packets/second")
        
    time = time/10**6        

    averagedCombinedLength = [0] * len(allCombinedLengths[0])    
    averagedLowPriorLength = [0] * len(allLengthsLowPriority[0])         
    averagedHighPrioLength = [0] * len(allLengthsHighPriority[0]) 

    for x in range(0, len(allLengthsHighPriority)):
        for y in range(0, len(allLengthsHighPriority[x])):
            averagedCombinedLength[y] += allCombinedLengths[x][y]
            averagedLowPriorLength[y] += allLengthsLowPriority[x][y]
            averagedHighPrioLength[y] += allLengthsHighPriority[x][y]
        
    averagedCombinedLength = np.asarray(averagedCombinedLength)
    averagedLowPriorLength = np.asarray(averagedLowPriorLength)
    averagedHighPrioLength = np.asarray(averagedHighPrioLength)
            
        
    for x in range(0, len(averagedCombinedLength)):
        averagedCombinedLength[x] = averagedCombinedLength[x]/averagedOver
        averagedLowPriorLength[x] = averagedLowPriorLength[x]/averagedOver 
        averagedHighPrioLength[x] = averagedHighPrioLength[x]/averagedOver 
            
        
            
    plt.figure()
    plt.plot(time, averagedCombinedLength, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs combined number of customers waiting in an M/M/1 queue with preemptive queues')
    plt.show()
    
    plt.figure()
    plt.plot(time, averagedLowPriorLength, label=str('Low Priority 1 Mbps'))
    plt.plot(time, averagedHighPrioLength, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of low- and high-priority packets waiting in an M/M/1 queue with preemptive queues')
    plt.show()  
    
    
if (doAveragePreemptive == True):
    print("##################################################################")
    print("########            Averaged Preemptive queuing            #######")
    print("##################################################################")
    
    time = np.arange(0, 101*10**6, 1000000)      
    
          
    totalInterArrivalLow       = []
    totalInterArrivalHigh      = []
    totalTransmissionLow       = []
    totalTransmissionHigh      = []
    totalResponseLow           = []
    totalResponseHigh          = []
    totalAveragePacketSizeLow  = [] 
    totalAveragePacketSizeHigh = [] 
    totalAverageDelaysLow      = [] 
    totalAverageDelaysHigh     = []
    totalArrivalRateLow        = []
    totalArrivalRateHigh       = [] 
    totalServiceRateLow        = [] 
    totalServiceRateHigh       = []
    allCombinedLengths         = [[]] * averagedOver
    allLengthsHighPriority     = [[]] * averagedOver
    allLengthsLowPriority      = [[]] * averagedOver
          
    for k in range(0, averagedOver):      
        packets = [[],[]]      
        transCap = linkCapacity
        
        # Read the csv file data into respective lists to store the data
        interArrivalHigh = list(np.random.exponential(400 , 40000))            
        packetSizeHigh   = list(np.random.exponential(1000, 40000))
        interArrivalLow  = list(np.random.exponential(500 , 50000))
        packetSizeLow    = list(np.random.exponential(1000, 50000))
        
        # Create the list of low priority packets
        for i in range(0, len(interArrivalLow)):
            lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
            packets[0].append(lowPacket)
        
        # Create the list of high priority packets
        for i in range(0, len(interArrivalHigh)):
            highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
            packets[1].append(highPacket)
        
        # Get the parameters
        arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcPreemptive(transCap, packets)
        sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
        if (k == 0):
            print("Link capacity --------------------------", transCap/10**6, "Mbps") 
            print("Number of low priority packets ---------", len(packetSizeLow), "packets")
            print("Number of high priority packets --------", len(packetSizeHigh), "packets")
            print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
        
        totalInterArrivalLow       += interArrivalLow
        totalInterArrivalHigh      += interArrivalHigh
        totalTransmissionLow       += transTimes[0]
        totalTransmissionHigh      += transTimes[1]
        totalResponseLow           += respTimes[0]
        totalResponseHigh          += respTimes[1]
        totalAveragePacketSizeLow  += packetSizeLow 
        totalAveragePacketSizeHigh += packetSizeHigh
        totalAverageDelaysLow      += queuingDelays[0]
        totalAverageDelaysHigh     += queuingDelays[1]
        
        startEnd = [[],[]]
        arrivalTimes = []
        startEndLow = [[],[]]
        arrivalTimesLow = []
        startEndHigh = [[],[]]
        arrivalTimesHigh = []
        
        for i in allPackets:
            startEnd[0].append(i.startTime)
            startEnd[1].append(i.endTime)
            arrivalTimes.append(i.arrivalTime)    
            
            if (i.priority == 'LOW'):
                startEndLow[0].append(i.startTime)
                startEndLow[1].append(i.endTime)
                arrivalTimesLow.append(i.arrivalTime)    
            
            if (i.priority == 'HIGH'):
                startEndHigh[0].append(i.startTime)
                startEndHigh[1].append(i.endTime)
                arrivalTimesHigh.append(i.arrivalTime)    
        
        combined = []
        lowPriority = []
        highPriority = []
        
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimes)):
                if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                    if (startEnd[0][j] > arrivalTimes[j]):
                        length += 1
            combined.append(length)
       
        allCombinedLengths[k] = deepcopy(combined)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesLow)):
                if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                    if (startEndLow[0][j] > arrivalTimesLow[j]):
                        length += 1
            lowPriority.append(length)
            
        allLengthsLowPriority[k] = deepcopy(lowPriority)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesHigh)):
                if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                    if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                        length += 1
            highPriority.append(length)
            
        allLengthsHighPriority[k] = deepcopy(highPriority)       
    
    print("Average inter-arrival time -- (LOW) ----", round((sum(totalInterArrivalLow))/(len(totalInterArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(totalInterArrivalHigh))/(len(totalInterArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow))/(len(totalInterArrivalHigh) + len(totalInterArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(totalTransmissionLow)/len(totalTransmissionLow), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(totalTransmissionHigh)/len(totalTransmissionHigh), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(totalTransmissionHigh) + sum(totalTransmissionLow))/(len(totalTransmissionHigh)+len(totalTransmissionLow)), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(totalResponseLow)/len(totalResponseLow), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(totalResponseHigh)/len(totalResponseHigh), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(totalResponseLow) + sum(totalResponseHigh))/(len(totalResponseLow) + len(totalResponseHigh)), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow), 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh), 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)) / (float(len(totalAveragePacketSizeLow)) + float(len(totalAveragePacketSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(totalAverageDelaysLow)/len(totalAverageDelaysLow), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(totalAverageDelaysHigh)/len(totalAverageDelaysHigh), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(totalAverageDelaysLow) + sum(totalAverageDelaysHigh))/(len(totalAverageDelaysHigh) + len(totalAverageDelaysLow)), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(totalAveragePacketSizeLow))/((sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(totalAveragePacketSizeLow) + len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)), 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)), 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh))/2), 4), "packets/second")
        
    time = time/10**6        

    averagedCombinedLength = [0] * len(allCombinedLengths[0])    
    averagedLowPriorLength = [0] * len(allLengthsLowPriority[0])         
    averagedHighPrioLength = [0] * len(allLengthsHighPriority[0]) 

    for x in range(0, len(allLengthsHighPriority)):
        for y in range(0, len(allLengthsHighPriority[x])):
            averagedCombinedLength[y] += allCombinedLengths[x][y]
            averagedLowPriorLength[y] += allLengthsLowPriority[x][y]
            averagedHighPrioLength[y] += allLengthsHighPriority[x][y]
        
    averagedCombinedLength = np.asarray(averagedCombinedLength)
    averagedLowPriorLength = np.asarray(averagedLowPriorLength)
    averagedHighPrioLength = np.asarray(averagedHighPrioLength)
            
        
    for x in range(0, len(averagedCombinedLength)):
        averagedCombinedLength[x] = averagedCombinedLength[x]/averagedOver
        averagedLowPriorLength[x] = averagedLowPriorLength[x]/averagedOver 
        averagedHighPrioLength[x] = averagedHighPrioLength[x]/averagedOver 
            
        
            
    plt.figure()
    plt.plot(time, averagedCombinedLength, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs combined number of customers waiting in an M/M/1 queue with preemptive queues')
    plt.show()
    
    plt.figure()
    plt.plot(time, averagedLowPriorLength, label=str('Low Priority 1 Mbps'))
    plt.plot(time, averagedHighPrioLength, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of low- and high-priority packets waiting in an M/M/1 queue with preemptive queues')
    plt.show()    
    
    
if (doAverageNoPriority == True):
    print("##################################################################")
    print("########              Averaged No Priority queuing         #######")
    print("##################################################################")
    
    time = np.arange(0, 101*10**6, 1000000)      
    
          
    totalInterArrivalLow       = []
    totalInterArrivalHigh      = []
    totalTransmissionLow       = []
    totalTransmissionHigh      = []
    totalResponseLow           = []
    totalResponseHigh          = []
    totalAveragePacketSizeLow  = [] 
    totalAveragePacketSizeHigh = [] 
    totalAverageDelaysLow      = [] 
    totalAverageDelaysHigh     = []
    totalArrivalRateLow        = []
    totalArrivalRateHigh       = [] 
    totalServiceRateLow        = [] 
    totalServiceRateHigh       = []
    allCombinedLengths         = [[]] * averagedOver
    allLengthsHighPriority     = [[]] * averagedOver
    allLengthsLowPriority      = [[]] * averagedOver
          
    for k in range(0, averagedOver):      
        packets = [[],[]]      
        transCap = linkCapacity
        
        # Read the csv file data into respective lists to store the data
        interArrivalHigh = list(np.random.exponential(400 , 40000))            
        packetSizeHigh   = list(np.random.exponential(1000, 40000))
        interArrivalLow  = list(np.random.exponential(500 , 50000))
        packetSizeLow    = list(np.random.exponential(1000, 50000))
        
        # Create the list of low priority packets
        for i in range(0, len(interArrivalLow)):
            lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
            packets[0].append(lowPacket)
        
        # Create the list of high priority packets
        for i in range(0, len(interArrivalHigh)):
            highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
            packets[1].append(highPacket)
        
        # Get the parameters
        arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcNoPriority(transCap, packets)
        sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
     
        if (k == 0):
            print("Link capacity --------------------------", transCap/10**6, "Mbps") 
            print("Number of low priority packets ---------", len(packetSizeLow), "packets")
            print("Number of high priority packets --------", len(packetSizeHigh), "packets")
            print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
        
        totalInterArrivalLow       += interArrivalLow
        totalInterArrivalHigh      += interArrivalHigh
        totalTransmissionLow       += transTimes[0]
        totalTransmissionHigh      += transTimes[1]
        totalResponseLow           += respTimes[0]
        totalResponseHigh          += respTimes[1]
        totalAveragePacketSizeLow  += packetSizeLow 
        totalAveragePacketSizeHigh += packetSizeHigh
        totalAverageDelaysLow      += queuingDelays[0]
        totalAverageDelaysHigh     += queuingDelays[1]
        
        startEnd = [[],[]]
        arrivalTimes = []
        startEndLow = [[],[]]
        arrivalTimesLow = []
        startEndHigh = [[],[]]
        arrivalTimesHigh = []
        
        for i in allPackets:
            startEnd[0].append(i.startTime)
            startEnd[1].append(i.endTime)
            arrivalTimes.append(i.arrivalTime)    
            
            if (i.priority == 'LOW'):
                startEndLow[0].append(i.startTime)
                startEndLow[1].append(i.endTime)
                arrivalTimesLow.append(i.arrivalTime)    
            
            if (i.priority == 'HIGH'):
                startEndHigh[0].append(i.startTime)
                startEndHigh[1].append(i.endTime)
                arrivalTimesHigh.append(i.arrivalTime)    
        
        combined = []
        lowPriority = []
        highPriority = []
        
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimes)):
                if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                    if (startEnd[0][j] > arrivalTimes[j]):
                        length += 1
            combined.append(length)
       
        allCombinedLengths[k] = deepcopy(combined)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesLow)):
                if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                    if (startEndLow[0][j] > arrivalTimesLow[j]):
                        length += 1
            lowPriority.append(length)
            
        allLengthsLowPriority[k] = deepcopy(lowPriority)
            
        for i in range(0, len(time)):
            length = 0
            for j in range(0, len(arrivalTimesHigh)):
                if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                    if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                        length += 1
            highPriority.append(length)
            
        allLengthsHighPriority[k] = deepcopy(highPriority)       
    
    print("Average inter-arrival time -- (LOW) ----", round((sum(totalInterArrivalLow))/(len(totalInterArrivalLow)), 4), "us" )
    print("Average inter-arrival time -- (HIGH) ---", round((sum(totalInterArrivalHigh))/(len(totalInterArrivalHigh)) ,4), "us" )
    print("Average inter-arrival time -- (TOTAL) --", round((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow))/(len(totalInterArrivalHigh) + len(totalInterArrivalLow)), 4), "us" )
    print("Average transmission time --- (LOW) ----", round(sum(totalTransmissionLow)/len(totalTransmissionLow), 4), "us" )
    print("Average transmission time --- (HIGH) ---", round(sum(totalTransmissionHigh)/len(totalTransmissionHigh), 4), "us" )
    print("Average transmission time --- (TOTAL) --", round((sum(totalTransmissionHigh) + sum(totalTransmissionLow))/(len(totalTransmissionHigh)+len(totalTransmissionLow)), 4), "us" )
    print("Average response time ------- (LOW)  ---", round(sum(totalResponseLow)/len(totalResponseLow), 4), "us" )
    print("Average response time ------- (HIGH) ---", round(sum(totalResponseHigh)/len(totalResponseHigh), 4), "us" )
    print("Average response time ------- (TOTAL) --", round((sum(totalResponseLow) + sum(totalResponseHigh))/(len(totalResponseLow) + len(totalResponseHigh)), 4) , "us" )
    print("The average packet size ----- (LOW) ----", round(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow), 4) , "bits" )
    print("The average packet size ----- (HIGH) ---", round(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh), 4) , "bits" )
    print("The average packet size ----- (TOTAL) --", round((sum(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)) / (float(len(totalAveragePacketSizeLow)) + float(len(totalAveragePacketSizeHigh))),4), "bits" )
    print("Average delays -------------- (LOW) ----", round(sum(totalAverageDelaysLow)/len(totalAverageDelaysLow), 4), "us")
    print("Average delays -------------- (HIGH) ---", round(sum(totalAverageDelaysHigh)/len(totalAverageDelaysHigh), 4), "us")
    print("Average delays -------------- (TOTAL) --", round((sum(totalAverageDelaysLow) + sum(totalAverageDelaysHigh))/(len(totalAverageDelaysHigh) + len(totalAverageDelaysLow)), 4), "us")
    print("Average arrival rate (lambda) (LOW) ----", round((len(totalAveragePacketSizeLow))/((sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (HIGH) ---", round((len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh)))*10**6, 4), "packets/second")
    print("Average arrival rate (lambda) (TOTAL) --", round((len(totalAveragePacketSizeLow) + len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
    print("Average service rate (mu) --- (LOW) ----", round(transCap/(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)), 4), "packets/second")
    print("Average service rate (mu) --- (HIGH) ---", round(transCap/(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)), 4), "packets/second")
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh))/2), 4), "packets/second")
        
    time = time/10**6        

    averagedCombinedLength = [0] * len(allCombinedLengths[0])    
    averagedLowPriorLength = [0] * len(allLengthsLowPriority[0])         
    averagedHighPrioLength = [0] * len(allLengthsHighPriority[0]) 

    for x in range(0, len(allLengthsHighPriority)):
        for y in range(0, len(allLengthsHighPriority[x])):
            averagedCombinedLength[y] += allCombinedLengths[x][y]
            averagedLowPriorLength[y] += allLengthsLowPriority[x][y]
            averagedHighPrioLength[y] += allLengthsHighPriority[x][y]
        
    averagedCombinedLength = np.asarray(averagedCombinedLength)
    averagedLowPriorLength = np.asarray(averagedLowPriorLength)
    averagedHighPrioLength = np.asarray(averagedHighPrioLength)
            
        
    for x in range(0, len(averagedCombinedLength)):
        averagedCombinedLength[x] = averagedCombinedLength[x]/averagedOver
        averagedLowPriorLength[x] = averagedLowPriorLength[x]/averagedOver 
        averagedHighPrioLength[x] = averagedHighPrioLength[x]/averagedOver 
            
        
            
    plt.figure()
    plt.plot(time, averagedCombinedLength, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs combined number of customers waiting in an M/M/1 queue with preemptive queues')
    plt.show()
    
    plt.figure()
    plt.plot(time, averagedLowPriorLength, label=str('Low Priority 1 Mbps'))
    plt.plot(time, averagedHighPrioLength, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of low- and high-priority packets waiting in an M/M/1 queue with preemptive queues')
    plt.show()        
    
if (doVaryingArrivalNonPreempt == True):
    print("##################################################################")
    print("########            Averaged Preemptive varying arrRate    #######")
    print("##################################################################")
    
    allQueuesLow  = []
    allQueuesHigh = []
    allQueuesComb = []
    
    for l in range(0, len(arrRates)):      
        time = np.arange(0, 101*10**6, 1000000)      
        
              
        totalInterArrivalLow       = []
        totalInterArrivalHigh      = []
        totalTransmissionLow       = []
        totalTransmissionHigh      = []
        totalResponseLow           = []
        totalResponseHigh          = []
        totalAveragePacketSizeLow  = [] 
        totalAveragePacketSizeHigh = [] 
        totalAverageDelaysLow      = [] 
        totalAverageDelaysHigh     = []
        totalArrivalRateLow        = []
        totalArrivalRateHigh       = [] 
        totalServiceRateLow        = [] 
        totalServiceRateHigh       = []
        allCombinedLengths         = [[]] * averagedOver
        allLengthsHighPriority     = [[]] * averagedOver
        allLengthsLowPriority      = [[]] * averagedOver
              
        for k in range(0, averagedOver):      
            packets = [[],[]]      
            transCap = linkCapacity
            
            # Read the csv file data into respective lists to store the data
            interArrivalHigh = list(np.random.exponential(arrRates[l] , arrRates[l]*100))            
            packetSizeHigh   = list(np.random.exponential(1000, arrRates[l]*100))
            interArrivalLow  = list(np.random.exponential(500 , 50000))
            packetSizeLow    = list(np.random.exponential(1000, 50000))
            
            print("AAAAAAAAA\n", interArrivalHigh)
            print("BBBBBBBBB\n", interArrivalLow)
            print("CCCCCCCCC\n", packetSizeHigh)
            print("DDDDDDDDD\n", packetSizeLow)
            
            # Create the list of low priority packets
            for i in range(0, len(interArrivalLow)):
                lowPacket = Packet(packetSizeLow[i], interArrivalLow[i], 'LOW')
                packets[0].append(lowPacket)
            
            # Create the list of high priority packets
            for i in range(0, len(interArrivalHigh)):
                highPacket = Packet(packetSizeHigh[i], interArrivalHigh[i], 'HIGH')
                packets[1].append(highPacket)
            
            # Get the parameters
            arrivalTimes,transTimes,queuingDelays,startEnd,respTimes,allPackets = calcNonPreemptive(transCap, packets)
            sizeAvg = [sum(packetSizeLow) / (float(len(packetSizeLow))), float(sum(packetSizeHigh))/len(packetSizeHigh)]
         
            if (k == 0):
                print("Link capacity --------------------------", transCap/10**6, "Mbps") 
                print("Number of low priority packets ---------", len(packetSizeLow), "packets")
                print("Number of high priority packets --------", len(packetSizeHigh), "packets")
                print("Total number of packets ----------------", len(packetSizeLow) + len(packetSizeHigh), "packets" )
            
            totalInterArrivalLow       += interArrivalLow
            totalInterArrivalHigh      += interArrivalHigh
            totalTransmissionLow       += transTimes[0]
            totalTransmissionHigh      += transTimes[1]
            totalResponseLow           += respTimes[0]
            totalResponseHigh          += respTimes[1]
            totalAveragePacketSizeLow  += packetSizeLow 
            totalAveragePacketSizeHigh += packetSizeHigh
            totalAverageDelaysLow      += queuingDelays[0]
            totalAverageDelaysHigh     += queuingDelays[1]
            
            startEnd = [[],[]]
            arrivalTimes = []
            startEndLow = [[],[]]
            arrivalTimesLow = []
            startEndHigh = [[],[]]
            arrivalTimesHigh = []
            
            for i in allPackets:
                startEnd[0].append(i.startTime)
                startEnd[1].append(i.endTime)
                arrivalTimes.append(i.arrivalTime)    
                
                if (i.priority == 'LOW'):
                    startEndLow[0].append(i.startTime)
                    startEndLow[1].append(i.endTime)
                    arrivalTimesLow.append(i.arrivalTime)    
                
                if (i.priority == 'HIGH'):
                    startEndHigh[0].append(i.startTime)
                    startEndHigh[1].append(i.endTime)
                    arrivalTimesHigh.append(i.arrivalTime)    
            
            combined = []
            lowPriority = []
            highPriority = []
            
            for i in range(0, len(time)):
                length = 0
                for j in range(0, len(arrivalTimes)):
                    if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                        if (startEnd[0][j] > arrivalTimes[j]):
                            length += 1
                combined.append(length)
           
            allCombinedLengths[k] = deepcopy(combined)
                
            for i in range(0, len(time)):
                length = 0
                for j in range(0, len(arrivalTimesLow)):
                    if (time[i] >= arrivalTimesLow[j] and startEndLow[1][j] > time[i]):
                        if (startEndLow[0][j] > arrivalTimesLow[j]):
                            length += 1
                lowPriority.append(length)
                
            allLengthsLowPriority[k] = deepcopy(lowPriority)
                
            for i in range(0, len(time)):
                length = 0
                for j in range(0, len(arrivalTimesHigh)):
                    if (time[i] >= arrivalTimesHigh[j] and startEndHigh[1][j] > time[i]):
                        if (startEndHigh[0][j] > arrivalTimesHigh[j]):
                            length += 1
                highPriority.append(length)
                
            allLengthsHighPriority[k] = deepcopy(highPriority)       
        
        print("Average inter-arrival time -- (LOW) ----", round((sum(totalInterArrivalLow))/(len(totalInterArrivalLow)), 4), "us" )
        print("Average inter-arrival time -- (HIGH) ---", round((sum(totalInterArrivalHigh))/(len(totalInterArrivalHigh)) ,4), "us" )
        print("Average inter-arrival time -- (TOTAL) --", round((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow))/(len(totalInterArrivalHigh) + len(totalInterArrivalLow)), 4), "us" )
        print("Average transmission time --- (LOW) ----", round(sum(totalTransmissionLow)/len(totalTransmissionLow), 4), "us" )
        print("Average transmission time --- (HIGH) ---", round(sum(totalTransmissionHigh)/len(totalTransmissionHigh), 4), "us" )
        print("Average transmission time --- (TOTAL) --", round((sum(totalTransmissionHigh) + sum(totalTransmissionLow))/(len(totalTransmissionHigh)+len(totalTransmissionLow)), 4), "us" )
        print("Average response time ------- (LOW)  ---", round(sum(totalResponseLow)/len(totalResponseLow), 4), "us" )
        print("Average response time ------- (HIGH) ---", round(sum(totalResponseHigh)/len(totalResponseHigh), 4), "us" )
        print("Average response time ------- (TOTAL) --", round((sum(totalResponseLow) + sum(totalResponseHigh))/(len(totalResponseLow) + len(totalResponseHigh)), 4) , "us" )
        print("The average packet size ----- (LOW) ----", round(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow), 4) , "bits" )
        print("The average packet size ----- (HIGH) ---", round(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh), 4) , "bits" )
        print("The average packet size ----- (TOTAL) --", round((sum(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)) / (float(len(totalAveragePacketSizeLow)) + float(len(totalAveragePacketSizeHigh))),4), "bits" )
        print("Average delays -------------- (LOW) ----", round(sum(totalAverageDelaysLow)/len(totalAverageDelaysLow), 4), "us")
        print("Average delays -------------- (HIGH) ---", round(sum(totalAverageDelaysHigh)/len(totalAverageDelaysHigh), 4), "us")
        print("Average delays -------------- (TOTAL) --", round((sum(totalAverageDelaysLow) + sum(totalAverageDelaysHigh))/(len(totalAverageDelaysHigh) + len(totalAverageDelaysLow)), 4), "us")
        print("Average arrival rate (lambda) (LOW) ----", round((len(totalAveragePacketSizeLow))/((sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
        print("Average arrival rate (lambda) (HIGH) ---", round((len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh)))*10**6, 4), "packets/second")
        print("Average arrival rate (lambda) (TOTAL) --", round((len(totalAveragePacketSizeLow) + len(totalAveragePacketSizeHigh))/((sum(totalInterArrivalHigh) + sum(totalInterArrivalLow)))*10**6, 4), "packets/second")
        print("Average service rate (mu) --- (LOW) ----", round(transCap/(sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)), 4), "packets/second")
        print("Average service rate (mu) --- (HIGH) ---", round(transCap/(sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)), 4), "packets/second")
        print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow) + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh))/2), 4), "packets/second")
            
        time = time/10**6        
    
        averagedCombinedLength = [0] * len(allCombinedLengths[0])    
        averagedLowPriorLength = [0] * len(allLengthsLowPriority[0])         
        averagedHighPrioLength = [0] * len(allLengthsHighPriority[0]) 
    
        for x in range(0, len(allLengthsHighPriority)):
            for y in range(0, len(allLengthsHighPriority[x])):
                averagedCombinedLength[y] += allCombinedLengths[x][y]
                averagedLowPriorLength[y] += allLengthsLowPriority[x][y]
                averagedHighPrioLength[y] += allLengthsHighPriority[x][y]
            
        averagedCombinedLength = np.asarray(averagedCombinedLength)
        averagedLowPriorLength = np.asarray(averagedLowPriorLength)
        averagedHighPrioLength = np.asarray(averagedHighPrioLength)
                
            
        for x in range(0, len(averagedCombinedLength)):
            averagedCombinedLength[x] = averagedCombinedLength[x]/averagedOver
            averagedLowPriorLength[x] = averagedLowPriorLength[x]/averagedOver 
            averagedHighPrioLength[x] = averagedHighPrioLength[x]/averagedOver 
                
        allQueuesComb.append(deepcopy(averagedCombinedLength))
        allQueuesHigh.append(deepcopy(averagedHighPrioLength))
        allQueuesLow.append(deepcopy(averagedLowPriorLength))
                
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesLow[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Preemptive Varying arrRate LowPriority')
    plt.show()
    
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesHigh[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Preemptive Varying arrRate HighPriority')
    plt.show()
    
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesHigh[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Preemptive Varying arrRate Combined Priority')
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
if( doVaryingArrivalNonPreempt == True):
    print("helllo")

if( doVaryingArrivalNoPriority == True):
    print("helllo")

    
    