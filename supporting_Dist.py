# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:37:49 2021

@author: Jimmy
"""

#THE distribution plotter, meant to help debug some of my logic

import math as mt
import numpy as np
import pandas as pd
import random as rn
import seaborn as sns

#Posted duration, min, max, risk parameter, alpha
def betaRectangular(ex,a,b,delt,alp):
    ratio=(ex-a+0.00001)/(b-a) #the decimal is strategic
    beta=(alp-alp*ratio)/ratio
    randNum=delt*rn.betavariate(alp,beta)+(1-delt)*(rn.uniform(0,1))
    ranDuration=randNum*(b-a)+a
    return(beta,ranDuration)

#print(betaRectangular(5,3,10,1,3))

durs=[]
for x in range(1000000):
    durs.append(betaRectangular(4,3,9,0.5,2)[1])
#print(betaRectangular(5,3,9,0.2,2)[0])
print('mean: ',np.mean(durs))
print('variance: ',np.var(durs))

#print(sns.__version__)
sns.displot(durs)
#sns.displot(durs,x="random mean",binwidth=0.2)