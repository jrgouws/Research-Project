# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:32:37 2019

@author: project
"""

import matplotlib.pyplot as plt
import numpy as np
import math

###############################################################################    
#############################    M/M/1 class    ###############################
###############################################################################
class MM1():
        
    def __init__(self, lamb, mu, customers):
        self.n    = customers
        self.lamb = lamb
        self.mu   = mu
        self.p    = self.calc_p(self.lamb, self.mu)
        self.U    = self.calc_U(self.lamb, self.mu)
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.Lq   = self.calc_Lq()
        self.Wq   = self.calc_Wq()
        self.W    = self.calc_W()
        self.L    = self.calc_L()
       
    def calc_p(self, lamb, mu):
        return lamb/mu
    
    def calc_U(self, lamb, mu):
        return lamb/mu
    
    def calc_P0(self):
        return (1 - self.p)
    
    def calc_Pn(self):
        return (1 - self.p)*(self.p)**self.n
    
    def calc_Lq(self):
        return self.p**2/(1 - self.p)
    
    def calc_Wq(self):
        return (self.p/self.mu)/(1 - self.p)
    
    def calc_W(self):
        return (1/self.mu)/(1 - self.p)
    
    def calc_L(self):
        return self.p/(1 - self.p)
    
    def recalc(self):
        self.p    = self.calc_p(self.lamb, self.mu)
        self.U    = self.calc_U(self.lamb, self.mu)
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.Lq   = self.calc_Lq()
        self.Wq   = self.calc_Wq()
        self.W    = self.calc_W()
        self.L    = self.calc_L()
 
###############################################################################    
#############################    M/M/s class    ###############################
###############################################################################    
    
class MMs():
        
    def __init__(self, lamb, mu, customers, servers):
        self.s    = servers
        self.n    = customers
        self.lamb = lamb
        self.mu   = mu
        self.p    = self.calc_p(self.lamb, self.mu)
        self.U    = self.calc_U(self.lamb, self.mu)
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.Lq   = self.calc_Lq()
        self.Wq   = self.calc_Wq()
        self.L    = self.calc_L()
        self.W    = self.calc_W()
       
    def calc_p(self, lamb, mu):
        return lamb/mu
    
    def calc_U(self, lamb, mu):
        return self.p/self.s
    
    def calc_P0(self):
        
        total = 0
        
        for i in range(0, self.s):
            total += (((self.s*self.U)**i)/math.factorial(i)) + (((self.s*self.U)**self.s)/(math.factorial(self.s)*(1-self.U)))
        
        
        return 1/total
    
    def calc_Pn(self):
        returnVal = 0
        if (self.n <= self.s):
            returnVal = self.P0 * (((self.U * self.s)**self.n)/math.factorial(self.n))
    
        else:
            returnVal = self.P0 * (((self.U ** self.n) * (self.s ** self.s))/(math.factorial(self.s)))
            
        return returnVal
    
    def calc_Lq(self):
        return ((self.U/(1-self.U))*(((self.s*self.U)**self.s)/(math.factorial(self.s)*(1-self.U))))*(self.P0)
    
    def calc_Wq(self):
        return self.Lq/self.lamb
    
   
    def calc_L(self):
        return self.Lq + self.s*self.U

    def calc_W(self):
        return self.L/self.lamb
    
    def recalc(self):
        self.p    = self.calc_p(self.lamb, self.mu)
        self.U    = self.calc_U(self.lamb, self.mu)
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.Lq   = self.calc_Lq()
        self.L    = self.calc_L()
        self.Wq   = self.calc_Wq()
        self.W    = self.calc_W()
    
    
###############################################################################    
#############################    M/M/inf class    #############################
###############################################################################  
class MMI():
        
    def __init__(self, lamb, mu, customers):
        self.n    = customers
        self.lamb = lamb
        self.mu   = mu
        self.p    = self.calc_p(self.lamb, self.mu)
        self.U    = 0
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.Lq   = 0
        self.Wq   = 0
        self.W    = self.calc_W()
        self.L    = self.calc_L()
       
    def calc_p(self, lamb, mu):
        return lamb/mu
        
    def calc_P0(self):
        return math.exp(-1*self.p)
    
    def calc_Pn(self):
        return self.P0* (self.p ** self.n)/(math.factorial(self.n))
    
    def calc_W(self):
        return 1/self.mu
    
    def calc_L(self):
        return self.p
        
    def recalc(self):
        self.p    = self.calc_p(self.lamb, self.mu)
        self.P0   = self.calc_P0()
        self.Pn   = self.calc_Pn()
        self.W    = self.calc_W()
        self.L    = self.calc_L() 
    
###############################################################################    
#############################    M/M/1 testing  ###############################
###############################################################################
lambd = 50
mu    = 65
customers = 10
print('')
mm1 = MM1(lambd, mu, customers)
print("##############      MM1     ######################")
print("p  =", mm1.p)
print("U  =", mm1.U)
print("P0 =", mm1.P0)
print("Pn =", mm1.Pn)
print("Lq =", mm1.Lq)
print("Wq =", mm1.Wq)
print("W  =", mm1.W)
print("L  =", mm1.L)

print('')
mm2 = MMs(lambd, mu, customers, 2)
print("##############      MM2     ######################")
print("p  =", mm2.p)
print("U  =", mm2.U)
print("P0 =", mm2.P0)
print("Pn =", mm2.Pn)
print("Lq =", mm2.Lq)
print("Wq =", mm2.Wq)
print("W  =", mm2.W)
print("L  =", mm2.L)

print('')
mm5 = MMs(lambd, mu, customers, 5)
print("##############      MM5     ######################")
print("p  =", mm5.p)
print("U  =", mm5.U)
print("P0 =", mm5.P0)
print("Pn =", mm5.Pn)
print("Lq =", mm5.Lq)
print("Wq =", mm5.Wq)
print("W  =", mm5.W)
print("L  =", mm5.L)

print('')
mm10 = MMs(lambd, mu, customers, 10)
print("##############      MM10    ######################")
print("p  =", mm10.p)
print("U  =", mm10.U)
print("P0 =", mm10.P0)
print("Pn =", mm10.Pn)
print("Lq =", mm10.Lq)
print("Wq =", mm10.Wq)
print("W  =", mm10.W)
print("L  =", mm10.L)

print('')
mm20 = MMs(lambd, mu, 10, 20)
print("##############      MM20    ######################")
print("p  =", mm20.p)
print("U  =", mm20.U)
print("P0 =", mm20.P0)
print("Pn =", mm20.Pn)
print("Lq =", mm20.Lq)
print("Wq =", mm20.Wq)
print("W  =", mm20.W)
print("L  =", mm20.L)

print('')
mmI= MMI(lambd, mu, 10)
print("##############      MMI     ######################")
print("p  =", mmI.p)
print("U  =", mmI.U)
print("P0 =", mmI.P0)
print("Pn =", mmI.Pn)
print("Lq =", mmI.Lq)
print("Wq =", mmI.Wq)
print("W  =", mmI.W)
print("L  =", mmI.L)


###############################################################################
############## Utilization (x-axis) vs Response time (y-axis) vs  #############
##############       (single and multi-server comparison)         #############
###############################################################################
# Utilization = U   (x-axis)
# Response time = W (y-axis)


customers = 100
mu        = 65 

x = []
y = []

servers = [2,5,10,20]

#########################    M/M/1       ######################################

lamb = np.linspace(0.01, (mu -1), 1000)

mm1 = MM1(lamb, mu, customers)    
     
x.append(mm1.U)
y.append(mm1.W)

#########################    M/M/s       ######################################

for j in servers:
    lamb = np.linspace(0.01, (mu -1) * j, 1000)
    mm2 = MMs(lamb, mu, customers, j)
    x.append(mm2.U)
    y.append(mm2.W)
    
#########################    M/M/inf     ######################################
lamb = np.linspace(0.01, (mu -1), 1000)
xTemp = []
yTemp = []

for i in range(0, len(lamb)):
    mmi = MMI(lamb[i], mu, customers)
    xTemp.append(mmi.U)
    yTemp.append(mmi.W)

x.append(xTemp)
y.append(yTemp)


plt.subplot(1,2,1)

for i in range(0, len(x)):
      if (i == 0):
            plt.plot(x[i], y[i], label=str('M/M/1'))
            
      elif (i == len(x) - 1):
            plt.plot(x[i], y[i], label=str('M/M/inf' ))
      else:
            plt.plot(x[i], y[i], label=str('M/M/' + str(servers[i-1])))


plt.legend(loc='best')
plt.xlabel('Utilization (U)')
plt.ylabel('Response time (W)')
plt.title('Utilization vs Response time (y-axis)\n for single and multi server models')
plt.show()


###############################################################################
##########################   Throughput (lambda) vs number customers ##########
###############################################################################

# Throughput/lambda   (x-axis)
# Num customers L     (y-axis)
x = []
y = []

#########################    M/M/1       ######################################

lamb = np.linspace(0.01, (mu -1) ,1000)
mm1 = MM1(lamb, mu, customers)    
x.append(mm1.L)
y.append(mm1.lamb)

#########################    M/M/s       ######################################

for j in servers:
      lamb = np.linspace(0.01, (mu -1) * j,1000)
      mm2 = MMs(lamb, mu, customers, j)
      x.append(mm2.L)
      y.append(mm2.lamb)

#########################    M/M/inf     ######################################
lamb = np.linspace(0.01, (mu -1), 1000)

xTemp = []
yTemp = []

for i in range(0, len(lamb)):
    mmi = MMI(lamb[i], mu, customers)
    xTemp.append(mmi.L)
    yTemp.append(mmi.lamb)

x.append(xTemp)
y.append(yTemp)

plt.subplot(1,2,2)
for i in range(0, len(x)):
      if (i == 0):
            plt.plot(x[i], y[i], label=str('M/M/1'))
            
      elif (i == len(x) - 1):
            plt.plot(x[i], y[i], label=str('M/M/inf' ))
      else:
            plt.plot(x[i], y[i], label=str('M/M/' + str(servers[i-1])))

plt.legend(loc='best')
plt.xlabel('Number of customers (L)')
plt.ylabel('Throughput (lambda)')
plt.title('Number of customers vs Throughput\n for single and multi server models')
plt.show()

###############################################################################
##########################   Response time (W) vs number customers   ##########
###############################################################################

# Response time (W)   (x-axis)
# Num customers L     (y-axis)
x = []
y = []

#########################    M/M/1       ######################################
lamb = np.linspace(0.01, (mu -1) ,1000)

mm1 = MM1(lamb, mu, customers)    
      
x.append(mm1.L)
y.append(mm1.W)

#########################    M/M/s       ######################################

for j in servers:
    lamb = np.linspace(0.01, (mu -1) * j,1000)
    mm2 = MMs(lamb, mu, customers, j)
    x.append(mm2.L)
    y.append(mm2.W)
    
    
#########################    M/M/inf     ######################################
      
lamb = np.linspace(0.01, (mu -1), 1000)
xTemp = []
yTemp = []

for i in range(0, len(lamb)):
    mmi = MMI(lamb[i], mu, customers)
    xTemp.append(mmi.L)
    yTemp.append(mmi.W)

x.append(xTemp)
y.append(yTemp)

plt.figure()
plt.subplot(1,2,1)
for i in range(0, len(x)):
      if (i == 0):
            plt.plot(x[i], y[i], label=str('M/M/1'))
            
      elif (i == len(x) - 1):
            plt.plot(x[i], y[i], label=str('M/M/inf' ))
      else:
            plt.plot(x[i], y[i], label=str('M/M/' + str(servers[i-1])))

plt.legend(loc='best')
plt.xlabel('Number of customers (L)')
plt.ylabel('Response time (W)')
plt.title('Number of customers vs Response time\n for single and multi server models')
plt.show()

###############################################################################
##########################   Utilization vs number customers ##########
###############################################################################

# Utilization (U)     (x-axis)
# Num customers L     (y-axis)

x = []
y = []

#########################    M/M/1       ######################################
lamb = np.linspace(0.01, (mu -1) ,1000)
mm1 = MM1(lamb, mu, customers)    
x.append(mm1.L)
y.append(mm1.U)

#########################    M/M/s       ######################################

for j in servers:
      lamb = np.linspace(0.01, (mu -1) * j,1000)
      mm2 = MMs(lamb, mu, customers, j)
      x.append(mm2.L)
      y.append(mm2.U)
  
#########################    M/M/inf     ######################################
      
lamb = np.linspace(0.01, (mu -1), 1000)
xTemp = []
yTemp = []

for i in range(0, len(lamb)):
    mmi = MMI(lamb[i], mu, customers)
    xTemp.append(mmi.L)
    yTemp.append(mmi.U)

x.append(xTemp)
y.append(yTemp)

plt.subplot(1,2,2)

for i in range(0, len(x)):
      if (i == 0):
            plt.plot(x[i], y[i], label=str('M/M/1'))
            
      elif (i == len(x) - 1):
            plt.plot(x[i], y[i], label=str('M/M/inf' ))
      else:
            plt.plot(x[i], y[i], label=str('M/M/' + str(servers[i-1])))

plt.legend(loc='best')
plt.xlabel('Number of customers (L)')
plt.ylabel('Utilization (U)')
plt.title('Number of customers vs Utilization\n for single and multi server models')
plt.show()



