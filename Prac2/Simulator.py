# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:15:31 2019

@author: project
"""

import csv
import matplotlib.pyplot as plt
import numpy as np

test =        False
doTrace =     True
doQueuelen =  True
doLambdMus  = True
genTrace =    True

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
    
    # Calculate how long each packet takes to transmit ?????????
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




def generateTrace(workload, linkCap, packetSz):
    print('#############   Generating trace file   ##########################')
    serviceRate = linkCap/packetSz
    
    arrRate = []
    avgInterArr = []
    
    
    arrRate = workload * serviceRate
    avgInterArr = 10**6/arrRate
    
    workloads = arrRate*100
        
    interArrival = np.random.exponential(int(avgInterArr), int(workloads))
    packetSize = np.random.exponential(int(packetSz), int(workloads))
    
    print(len(interArrival),"packets generated")
    print("Mean inter-arrival generated = ", sum(interArrival)/len(interArrival))
    print("Mean packet size   generated = ", sum(packetSize)/len(packetSize))
    
    with open('generatedTrace.txt', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(zip(map(int,interArrival), map(int, packetSize)))




def queuLenVsTime(packetSz, linkCap):
    print("###########  Queue length vs time ################################")
    serviceRate = linkCap/packetSz
    simPerc = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    arrRate = []
    avgInterArr = []
    
    for i in simPerc:
          arrRate.append(i*serviceRate)
          avgInterArr.append(10**6/arrRate[-1])
          
    # Calculate the amount of packet to generate (arrival rate * 100 sec)      
    workloads = []
    for i in arrRate:
          workloads.append(i*100)
    
   
    total = []
    time = []

    for p in range(0,200):
        print(p, end = " ")
        allQueues = []
        
        for z in range(0, len(workloads)):
            transCap = linkCap
            
            # Read the csv file data into respective lists to store the data
            interArrival = np.random.exponential(int(avgInterArr[z]), int(workloads[z]))
            packetSize = np.random.exponential(int(packetSz), int(workloads[z]))
                
            # Get the parameters
            arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
           
           
            if (p == 0):
                time.append(np.arange(0, startEnd[-1][1], 1000000))
            
                       
            queue = []
            
            for i in range(0, len(time[z])):
                length = 0
                for j in range(0, len(startEnd)):
                    if (time[z][i] >= arrivalTimes[j] and startEnd[j][1] > time[z][i]):
                        if (startEnd[j][0] > arrivalTimes[j]):
                            length += 1
                queue.append(length)            
            
            allQueues.append(queue)
            
        if (p == 0):
            total = allQueues
        
        else:
            for i in range(0, len(allQueues)):
                for j in range(0, len(allQueues[i])):
                    total[i][j] += allQueues[i][j]
                    

    for i in range(0, len(allQueues)):
        for j in range(0, len(allQueues[i])):
            total[i][j] /= 100
        
    plt.figure()
    for i in range(0, len(total)):
        plt.plot(time[i], total[i], label=str(simPerc[i]*100) + ' % load')
    plt.legend(loc='best')
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of customers waiting in a M/M/1 queue\n of different link workloads')
    plt.show()
    
def calcLambMuWorkloads(packetSz, linkCap):
    print("########### Lambda, mu and delay time for workloads ##############")
    serviceRate = linkCap/packetSz
    simPerc = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    arrRate = []
    avgInterArr = []
    
    for i in simPerc:
        arrRate.append(i*serviceRate)
        avgInterArr.append(10**6/arrRate[-1])
      
    workloads = []
    for i in arrRate:
        workloads.append(i*100)
        
    lambdas = [0] * len(workloads)    
    mus = [0] * len(workloads)
    queueDels = [0] * len(workloads)

    for p in range(0,10):
        print(p, end = " ")
        
        for z in range(0, len(workloads)):
            transCap = linkCap
            
            # Read the csv file data into respective lists to store the data
            interArrival = np.random.exponential(int(avgInterArr[z]), int(workloads[z]))
            packetSize = np.random.exponential(int(packetSz), int(workloads[z]))
   
            # Get the parameters
            arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
            
            sizeAvg = sum(packetSize) / float(len(packetSize))
            lambdas[z] += (len(packetSize))/(sum(interArrival)/10**6)
            mus[z] += transCap/sizeAvg
            queueDels[z] += sum(queuingDelays)/len(queuingDelays)
      
    lambdas = np.asarray(lambdas)/10
    mus = np.asarray(mus)/10
    queueDels = np.asarray(queueDels)/10
    
    print("Lambdas            at [10%. 20%, ...., 80%, 90%] workload =")
    for i in lambdas:
          print(i)
    
    print("Mu's               at [10%. 20%, ...., 80%, 90%] workload =")
    for i in mus:
          print(i)
    
    print("Avg queuing delays at [10%. 20%, ...., 80%, 90%] workload =")
    for i in queueDels:
          print(i)
    


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

if (test == True):
    # Transmission Capacity of 10 Mbps
    transCap = 10 * 10 ** 6
    
    # Read the csv file data into respective lists to store the data
    interArrival, packetSize = readCSV('example.txt')
    
    # Get the parameters
    arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
          
    print("Arrival times of the packets...........", arrivalTimes)
    print("Transmission times of the packets......", transTimes)
    print("Response times of the packet...........", respTimes)
    print("Start and end times of the packets.....", startEnd)
    print("Queuing delays of the packets..........", queuingDelays)
    print("System idel times are .................", idleTimes)

if (doTrace == True):
    print("######## Processing trace file given    ##########################")
    allQueues = []
    capacities = [1.00]
    
    time = []
    
    for z in range(0, len(capacities)):
        transCap = capacities[z] * 10 ** 6
        
        # Read the csv file data into respective lists to store the data
        interArrival, packetSize = readCSV('trace.txt')
        
        # Get the parameters
        arrivalTimes,transTimes,queuingDelays,startEnd,idleTimes,respTimes = calculateParameters(interArrival, packetSize, transCap)
        sizeAvg = sum(packetSize) / float(len(packetSize))
            
        
  
        if (transCap == 1*10**6):
            print("Link capacity --------------------", transCap, "bps") 
            print("Number of packets ---------------", len(packetSize), "packets" )
            print("Average inter-arrival time ------", sum(interArrival)/len(interArrival), "us" )
            print("Average transmission time -------", sum(transTimes)/len(transTimes), "us" )
            print("Average response time -----------", sum(respTimes)/len(respTimes), "us" )
            print("The average packet size is ------", sizeAvg, "bits" )
            print("Average delays ------------------", sum(queuingDelays)/len(queuingDelays), "us")
            print("Average arrival rate (lambda)----", (len(packetSize))/(sum(interArrival)/10**6))
            print("Average service rate (mu) -------", transCap/sizeAvg)
            
        
        time.append(np.arange(0, startEnd[-1][1], 1000000))
        queue = []
        
        for i in range(0, len(time[z])):
            length = 0
            for j in range(0, len(startEnd)):
                if (time[z][i] >= arrivalTimes[j] and startEnd[j][1] > time[z][i]):
                    if (startEnd[j][0] > arrivalTimes[j]):
                        length += 1
            queue.append(length)            
        
        
        allQueues.append(queue)
        
        
    for i in range(0, len(allQueues)):
        plt.plot(time[i], allQueues[i], label=str(capacities[i]) + 'Mbps')
    plt.legend(loc='best')
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Customers waiting in queue')
    plt.title('Time vs number of customers waiting in a M/M/1 queue\n of different link capacities')
    plt.show()

if (doQueuelen == True):
    queuLenVsTime(1000, 100*10**2)
    
if (doLambdMus == True):
    calcLambMuWorkloads(1000, 1*10**6)

if (genTrace == True):
    generateTrace(0.5, 100*10**6, 1000)