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
        return lamb/(mu*self.s)
    
    def calc_P0(self):
        
        total = 0
        
        for i in range(0, self.s):
            total += (((self.s * self.p)**i)/(math.factorial(i)) + ((self.s * self.p)**self.s)/(math.factorial(self.s)*(1-self.p)))**(-1)
        
        return total
    
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

mm1 = MM1(50, 65, 10)
print("##############      MM1     ######################")
print("p  =", mm1.p)
print("U  =", mm1.U)
print("P0 =", mm1.P0)
print("Pn =", mm1.Pn)
print("Lq =", mm1.Lq)
print("Wq =", mm1.Wq)
print("W  =", mm1.W)
print("L  =", mm1.L)

###############################################################################    
#############################    M/M/s testing  ###############################
###############################################################################

mm2 = MMs(50, 65, 1, 2)

print("##############      MM2     ######################")
print("p  =", mm2.p)
print("U  =", mm2.U)
print("P0 =", mm2.P0)
print("Pn =", mm2.Pn)
print("Lq =", mm2.Lq)
print("Wq =", mm2.Wq)
print("W  =", mm2.W)
print("L  =", mm2.L)
    
###############################################################################
############## Utilization (x-axis) vs Response time (y-axis) vs  #############
##############       (single and multi-server comparison)         #############
###############################################################################

# Utilization = U   (x-axis)
# Response time = W (y-axis)

customers = 5
lamb      = np.arange(1,64,1)
mu        = 65 


x1 = []
y1 = []

for i in range(len(lamb)):
    mm1 = MM1(lamb[i], mu, customers)    
    x1.append(mm1.U)
    y1.append(mm1.W)
    
plt.xlabel('Utilization (U)')
plt.ylabel('Response time (W)')
plt.title('Utilization vs Response time (y-axis)\n for single and multi server models')
plt.figure(1)    
plt.plot(x1, y1)


    


