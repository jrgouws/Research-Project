# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:40:23 2019

@author: project
"""

import matplotlib.pyplot as plt
from PriorityQueuing import readCSV, Packet, calcNoPriority, calcNonPreemptive, calcPreemptive
import numpy as np
import time as t

doNonPreemptiveTrace        = False
doPreemptiveTrace           = False
doNoPriority                = True


linkCapacity = 1*10**6


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
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/(((sum(interArrivalHigh)*40000 + sum(interArrivalLow)*50000)/90000))*10**6, 4), "packets/second")
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
            
    time = np.arange(0, startEnd[1][-1], 1000000)
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
    plt.title('No priority combined Trace')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority trace file packets'))
    plt.plot(time, highPriority, label=str('High Priority trace file packets'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('No priority low and high Trace')
    plt.show()

    
if (doNonPreemptiveTrace == True):
    print("##################################################################")
    print("########        Processing non-preemptive queuing          #######")
    print("##################################################################")
    timeNow = t.time()
          
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
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/(((sum(interArrivalHigh)*40000 + sum(interArrivalLow)*50000)/90000))*10**6, 4), "packets/second")
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
            
    time = np.arange(0, startEnd[1][-1], 1000000)
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
    plt.title('Non-preemptive combined queues Trace')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority 1 Mbps'))
    plt.plot(time, highPriority, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Non-preemptive low and high queues Trace')
    plt.show()
    print(t.time() - timeNow)
    

if (doPreemptiveTrace == True):
    print("##################################################################")
    print("########            Processing preemptive queuing          #######")
    print("##################################################################")
    timeNow = t.time()
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
    print("Average arrival rate (lambda) (TOTAL) --", round((len(packetSizeLow) + len(packetSizeHigh))/(((sum(interArrivalHigh)*40000 + sum(interArrivalLow)*50000)/90000))*10**6, 4), "packets/second")
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
               
    time = np.arange(0, 120*10**6, 1000000)
    combined = []
    lowPriority = []
    highPriority = []
    
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimes)):
              if (time[i] >= arrivalTimes[j] and startEnd[0][j] > time[i] and startEnd[0][j] > arrivalTimes[j]):
                    length += 1
                    
        combined.append(length)
              
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesLow)):
            if (time[i] >= arrivalTimesLow[j] and startEndLow[0][j] > time[i] and startEndLow[0][j] > arrivalTimesLow[j]):
                  length += 1
        lowPriority.append(length)
                
    for i in range(0, len(time)):
        length = 0
        for j in range(0, len(arrivalTimesHigh)):
            if (time[i] >= arrivalTimesHigh[j] and startEndHigh[0][j] > time[i] and startEndHigh[0][j] > arrivalTimesHigh[j]):
                    length += 1
        highPriority.append(length)
            
    time = time/10**6            
            
    plt.figure()
    plt.plot(time, combined, label=str('Combined 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Combined Preemptive queues Trace')
    plt.show()
    
    plt.figure()
    plt.plot(time, lowPriority, label=str('Low Priority 1 Mbps'))
    plt.plot(time, highPriority, label=str('High Priority 1 Mbps'))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Preemptive queues low and high Trace')
    plt.show()
    print(t.time() - timeNow)