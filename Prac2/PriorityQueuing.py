# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:15:31 2019

@author: project
"""

import csv

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


def getTraceInfo():
    # Read the csv file data into respective lists to store the data
    interArrivalHigh, packetSizeHigh = readCSV('HighPriority.txt')
    interArrivalLow , packetSizeLow  = readCSV('LowPriority.txt')
    print("Low Priority Packets  :", len(interArrivalLow))
    print("High Priority Packets :", len(interArrivalHigh))
    print("Avg interarrival Low  :", sum(interArrivalLow)/len(interArrivalLow))
    print("Avg interarrival High :", sum(interArrivalHigh)/len(interArrivalHigh))
    print("Avg size Low          :", sum(packetSizeLow)/len(packetSizeLow))
    print("Avg size High         :", sum(packetSizeHigh)/len(packetSizeHigh))
    print("Total interarrival    :", (sum(interArrivalHigh)+sum(interArrivalLow))/(len(interArrivalHigh)+len(interArrivalLow)))

getTraceInfo()

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
