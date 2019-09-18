# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:41:12 2019

@author: project
"""
import matplotlib.pyplot as plt
from PriorityQueuing import Packet, calcNoPriority, calcNonPreemptive, calcPreemptive
import numpy as np
from operator import add
from copy import deepcopy

doVaryingArrivalPreempt     = False
doVaryingArrivalNonPreempt  = True
doVaryingArrivalNoPriority  = False

averagedOver = 100
arrRates = [2100,2300,2500,2700,2900] # Actually interArrivalTimes
linkCapacity = 1*10**6


if (doVaryingArrivalNonPreempt == True):
    print("##################################################################")
    print("########        Averaged Non-Preemptive varying arrRate    #######")
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
            print(l,k)
            # Read the csv file data into respective lists to store the data
            interArrivalHigh = list(np.random.exponential(arrRates[l] , int(100/(arrRates[l]*10**-6))))            
            packetSizeHigh   = list(np.random.exponential(1000, int(100/(arrRates[l]*10**-6))))
            interArrivalLow  = list(np.random.exponential(2000 , 50000))
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
            
            lowPriority = []
            highPriority = []
            
                
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
      
            allCombinedLengths[k] = list( map(add, highPriority, lowPriority) )
        
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
        print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)*50000 + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)*arrRates[l]*10**-6)/(50000+arrRates[l]*10**-6)), 4), "packets/second")
            
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
    
    averagedQueuesHigh = [0]*len(allQueuesHigh[0])
    
    for a in range(0, len(allQueuesHigh)):
        for b in range(0, len(allQueuesHigh[a])):
            averagedQueuesHigh[b] += allQueuesHigh[a][b]
            
            if (a == len(allQueuesHigh) - 1):
                averagedQueuesHigh[b] = averagedQueuesHigh[b]/averagedOver
            
            
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesLow[t], label="Low " + str(arrRates[t]))
        
    plt.plot(time, averagedQueuesHigh, label="High " + str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Non-Preemptive Varying arrRate High LowPriority')
    plt.show()
    
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesComb[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Non-Preemptive Varying arrRate Combined Priority')
    plt.show()
    
if( doVaryingArrivalPreempt == True):
    print("##################################################################")
    print("########            Averaged Preemptive varying arrRate    #######")
    print("##################################################################")
    
    allQueuesLow  = []
    allQueuesHigh = []
    allQueuesComb = []
    
    for l in range(0, len(arrRates)):      
        time = np.arange(0, 125*10**6, 1000000)
        
              
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
            interArrivalHigh = list(np.random.exponential(arrRates[l] , int(100/(arrRates[l]*10**-6))))            
            packetSizeHigh   = list(np.random.exponential(1000, int(100/(arrRates[l]*10**-6))))
            interArrivalLow  = list(np.random.exponential(2000 , 50000))
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
            
            print(l,k)
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
            allCombinedLengths[k] = list( map(add, highPriority, lowPriority) )

        
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
        print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)*50000 + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)*arrRates[l]*10**-6)/(50000+arrRates[l]*10**-6)), 4), "packets/second")
        
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
                
    averagedQueuesHigh = [0]*len(allQueuesHigh[0])
    
    for a in range(0, len(allQueuesHigh)):
        for b in range(0, len(allQueuesHigh[a])):
            averagedQueuesHigh[b] += allQueuesHigh[a][b]
            
            if (a == len(allQueuesHigh) - 1):
                averagedQueuesHigh[b] = averagedQueuesHigh[b]/averagedOver
            
            
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesLow[t], label="Low priority " + str(arrRates[t]))
    plt.plot(time, averagedQueuesHigh, label="High priority " + str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Non-Preemptive Varying arrRate High LowPriority')
    plt.show()
    
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesComb[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Preemptive Varying arrRate Combined Priority')
    plt.show()
    
if( doVaryingArrivalNoPriority == True):
    print("##################################################################")
    print("########            Averaged No Priority varying arrRate   #######")
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
            interArrivalHigh = list(np.random.exponential(arrRates[l] , int(100/(arrRates[l]*10**-6))))            
            packetSizeHigh   = list(np.random.exponential(1000, int(100/(arrRates[l]*10**-6))))
            interArrivalLow  = list(np.random.exponential(2000 , 50000))
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
            
            print(l,k)
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
            allCombinedLengths[k] = list( map(add, highPriority, lowPriority) )

        
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
        print("Average service rate (mu) --- (TOTAL) --", round(transCap/((sum(totalAveragePacketSizeLow)/len(totalAveragePacketSizeLow)*50000 + sum(totalAveragePacketSizeHigh)/len(totalAveragePacketSizeHigh)*arrRates[l]*10**-6)/(50000+arrRates[l]*10**-6)), 4), "packets/second")
           
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
                
    averagedQueuesHigh = [0]*len(allQueuesHigh[0])
    
    for a in range(0, len(allQueuesHigh)):
        for b in range(0, len(allQueuesHigh[a])):
            averagedQueuesHigh[b] += allQueuesHigh[a][b]
            
            if (a == len(allQueuesHigh) - 1):
                averagedQueuesHigh[b] = averagedQueuesHigh[b]/averagedOver
            
            
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesLow[t], label="Low " + str(arrRates[t]))
    plt.plot(time, averagedQueuesHigh, label="High " + str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Non-Preemptive Varying arrRate High LowPriority')
    plt.show()
    
    plt.figure()
    for t in range(0, len(allQueuesHigh)):
        plt.plot(time, allQueuesComb[t], label=str(arrRates[t]))
    plt.legend(loc='best')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('No-Priority Varying arrRate Combined Priority')
    plt.show()