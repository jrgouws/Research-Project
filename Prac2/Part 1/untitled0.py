# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:47:05 2019

@author: project
"""

import csv

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


interArrivalHigh, packetSizeHigh = readCSV('HighPriority.txt')
interArrivalLow , packetSizeLow  = readCSV('LowPriority.txt')




