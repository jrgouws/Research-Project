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
    def __init__(self, size, interArrivalTime, priority):
        self.size             = size             #
        self.interArrivalTime = interArrivalTime #
        self.priority         = priority         #
        self.arrivalTime      = 0                #
        self.transTime        = 0                # 
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
        if (currTime == 0):
            if (packets[0][0].interArrivalTime < packets[1][0].interArrivalTime):
                completedPackets.append(packets[0][0])
                completedPackets[0].startTime = completedPackets[0].interArrivalTime
                completedPackets[0].endTime = completedPackets[0].startTime + completedPackets[0].transTime
                packets[0] = packets[0][1:]
                currTime = completedPackets[0].interArrivalTime
                
            else:
                completedPackets.append(packets[1][0])
                completedPackets[0].startTime = completedPackets[0].interArrivalTime
                completedPackets[0].endTime = completedPackets[0].startTime + completedPackets[0].transTime
                packets[1] = packets[1][1:]
                currTime = completedPackets[1].interArrivalTime
    
        toProcess = []
        
        # Add all the packets from the high priority queue that have arrived
        # and process
        for i in range(0, len(packets[1])):
            if (packets[1][i].arrivalTime <= currTime):
                toProcess.append(packets[1][i])
                
                if (i == len(packets[1]) - 1):
                    packets[1] = []
                
                
            else:
                packets[1] = packets[1][i:]
                break
            
        # If no high priority packets were received, add a single low priority packet
        if (len(toProcess) == 0 and len(packets[0]) != 0):
            if (packets[0][0].arrivalTime <= currTime):
                toProcess.append(packets[0][0])
                packets[0] = packets[0][1:]
            
        # If no packet was received at the current time, update the time to the
        # next arrival time of the packet
        if (len(toProcess) == 0):
            if (len(packets[1]) != 0 and len(packets[0]) != 0):
                if (packets[0][0].arrivalTime < packets[1][0].arrivalTime):
                    currTime = packets[0][0].arrivalTime
                    
                else:
                    currTime = packets[1][0].arrivalTime
            
            elif (len(packets[0]) == 0):
                currTime = packets[1][0].arrivalTime
                
            else:
                currTime = packets[0][0].arrivalTime

        if (len(toProcess)>1):                
            print(len(toProcess))
        
        # Process all the packets that has arrived
        for i in range(0, len(toProcess)):
            toProcess[i].startTime  = currTime
            toProcess[i].endTime    = currTime + toProcess[i].transTime
            toProcess[i].queueDelay = currTime - toProcess[i].arrivalTime
            completedPackets.append(toProcess[i])
            currTime = toProcess[i].endTime
            
        toProcess = []
            
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




if (doTrace == True):
    print("##################################################################")
    print("########        Processing non-preemptive queuing          #######")
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
    print("Average service rate (mu) --- (TOTAL) --", round(transCap/(sizeAvg[0] + sizeAvg[1]), 4), "packets/second")


    startEnd = [[],[]]
    arrivalTimes = []
    
    for i in allPackets:
        startEnd[0].append(i.startTime)
        startEnd[1].append(i.endTime)
        arrivalTimes.append(i.arrivalTime)    
        
    time = np.arange(0, startEnd[1][-1], 1000000)
    queue = []
    
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimes)):
            if (time[i] >= arrivalTimes[j] and startEnd[1][j] > time[i]):
                if (startEnd[0][j] > arrivalTimes[j]):
                    length += 1
        queue.append(length)

    time = time/10**6            
            
    plt.plot(time, queue, label=str('1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of customers waiting in a M/M/1 queue\n of different link capacities')
    plt.show()
