# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:15:31 2019

@author: project
"""

import csv

debug = True

# Read the text file and the inter-arrival time and the size
def readCSV(filePath):
    arrival = []
    size = []
    
    with open(filePath,'r')as f:
        data = csv.reader(f)
        for row in data:
            arrival.append(row[0])
            size.append(row[1])
    
    # Convert the strings lists to integer lists
    arrival = list(map(int, arrival))
    size = list(map(int, size))

    return arrival, size  


# Takes the inter-arrival times, packet sizes in bits of packets as an 
# integer list and the transmission capacity as an integer and returns
# arrivalTimes, transTimes, queuingDelays, startEnd, idleTimes, respTimes.
def calculateParameters(interArrival, packetSize, transCap):
    arrivalTimes = []
    transTimes = []
    queuingDelays = []   
    startEnd = []
    idleTimes = []
    respTimes = []
    currTime = 0
    
    # Calculate when the packets were received
    for i in range(0, len(interArrival)):
        if (i == 0):
            arrivalTimes.append(interArrival[i])
            
        else:
            arrivalTimes.append(interArrival[i] + arrivalTimes[i - 1])
    
    # Calculate how long each packet takes to transmit
    for i in packetSize:
        transTimes.append(i/transCap*10**6)
    
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
  
    return arrivalTimes, transTimes, queuingDelays, startEnd, idleTimes, respTimes

# List of inter-arrival times of the packages received
interArrival = []

# List of the size in bits of the packages received
packetSize = []

# Time of arrival of each packet, corresponding to the index positions 
arrivalTimes = []

# Time to transmit each packet
transTimes = []

# Transmission Capacity of 1 Mbps
transCap = 1 * 10 ** 6

# Queuing delays of the packets
queuingDelays = []   

# Start and end time of service of packet
startEnd = []

# Server idle times
idleTimes = []

# Response times of each packet
respTimes = []

if (debug == True):
    # Transmission Capacity of 10 Mbps
    transCap = 10 * 10 ** 6
    
    # Read the csv file data into respective lists to store the data
    interArrival, packetSize = readCSV('example.txt')
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
          
    print("Arrival times of the packets...........",arrivalTimes)
    print("Transmission times of the packets......", transTimes)
    print("Response times of the packet...........", respTimes)
    print("Start and end times of the packets.....", startEnd)
    print("Queuing delays of the packets..........", queuingDelays)
    print("System idel times are .................", idleTimes)

else:
    # Read the csv file data into respective lists to store the data
    interArrival, packetSize = readCSV('trace.txt')
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
    
    # Get the average arrival time of the csv file
    print("The average arrival time is", sum(interArrival) / float(len(interArrival)), "us")
    
    # Get the average packet size
    sizeAvg = sum(packetSize) / float(len(packetSize))
    print("The average packet size is", sizeAvg, "bits")
    
    # Get the average service time
    print("The average service time is (avg packet size)/(link capacity)",
          sizeAvg/transCap*10**6, "packets/sec")