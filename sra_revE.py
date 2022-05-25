# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:51:12 2021

@author: Jimmy
"""

import random as rn
import datetime as dt
from linker_revE import linker

wd='data_folder\dates_testset_revE.csv'

#determine unique number of event dependencies
def depUnique(datX):
    itUni=[]
    for x in range(len(datX)):
        if datX[x] not in itUni:
            itUni.append(datX[x])
    itUni.sort()
    return(itUni)

def dateConv(st,dur):
    yA=int(st.split('/')[2])
    mA=int(st.split('/')[1])
    dA=int(st.split('/')[0])
    
    buf=dt.timedelta(dur)
    aS=dt.datetime(yA,mA,dA)
    aD=aS+buf
    return(aD)

def dateCont(d1,d2):
    yA1=int(d1.split('/')[2])
    mA1=int(d1.split('/')[1])
    dA1=int(d1.split('/')[0])
    yA2=int(d2.split('/')[2])
    mA2=int(d2.split('/')[1])
    dA2=int(d2.split('/')[0])
    
    aD1=dt.datetime(yA1,dA1,mA1)
    aD2=dt.datetime(yA2,dA2,mA2)
    aD=aD2-aD1
    return(aD)

def betaRectangular(ex,a,b,delt):
    alp=2
    ratio=(ex-a+0.00001)/(b-a)
    beta=(alp-alp*ratio)/ratio
    randNum=delt*rn.betavariate(alp,beta)+(1-delt)*rn.uniform(0,1)
    ranDuration=randNum*(b-a)+a
    return(ranDuration)

def triPointEst(opt,mle,pes):
    raNum=rn.uniform(0,1)
    lh=(mle-opt)/(pes-opt)
    if raNum<lh:
        val=opt+(raNum*(pes-opt)*(mle-opt))**0.5
    else:
        val=pes-((1-raNum)*(pes-opt)*(pes-mle))**0.5
    return(val)

itns=10000
if itns % 10 !=0:
    print('WARNING: ITNS mod 10 not 0, you will lose some post-calc data in right tail!')
    
#file read in
f=open(wd,'r')
g=f.readlines()
f.close()
h=[g[x][:-1] for x in range(len(g))]
dat1=[] #event name
dat2=[] #event ID
dat3=[] #event start
dat4=[] #event end
dat5=[] #duration (E[x])
dat6=[] #optimistic duration (a)
dat7=[] #pessimistic duration (b)
dat8=[] #risk tuning parameter (delt) or TPE
dat9=[] #pre-reqs

for x in range(1,len(h)):
    dat1.append(h[x].split(',')[0])
    dat2.append(h[x].split(',')[1])
    dat3.append(h[x].split(',')[2])
    dat4.append(h[x].split(',')[3])
    dat5.append(h[x].split(',')[4])
    dat6.append(h[x].split(',')[5])
    dat7.append(h[x].split(',')[6])
    dat8.append(h[x].split(',')[7])
    dat9.append(h[x].split(',')[8])

for x in range(len(dat1)):
    if dat1[x]=='':
        dat1.pop([x])
        dat2.pop([x])
        dat3.pop([x])
        dat4.pop([x])
        dat5.pop([x])
        dat6.pop([x])
        dat7.pop([x])
        dat8.pop([x])
        dat9.pop([x])

dat5=[int(dat5[x]) for x in range(len(dat5))]
dat6=[int(dat6[x]) for x in range(len(dat6))]
dat7=[int(dat7[x]) for x in range(len(dat7))]
dat10=depUnique(dat9)

datStart=[dat2[x] for x in range(len(dat2))]
datEnd=[dat9[x] for x in range(len(dat9))]

multiLink=[]
for x in range(len(dat9)):
    ncount=0
    if 'm' in dat9[x]:
        ncount=len(dat9[x].split('m'))
        for y in range(ncount):
            multiLink.append(dat9[x].split('m')[y])
        print('Event',dat2[x],'has',ncount,'linked events.')

uniList=[]
for x in range(len(dat9)):
    if('m' not in dat9[x]) and ('na' not in dat9[x]):
        uniList.append(dat9[x])
uniList=uniList+multiLink

preEvents=[]
for x in range(len(dat2)):
    if dat2[x] not in uniList:
        preEvents.append(dat2[x])

dat9Vars=[]
dat9String=''
for x in range(len(dat9)):
    dat9String=dat9String+dat9[x]

m_count=0
for x in range(len(dat9String)):
    if dat9String[x]=='m':
        m_count+=1
    
#call pathfinding 
strOfStrs=linker(dat2,dat9,preEvents)
pathDurs=[]
pathMars=[]
for y in range(len(strOfStrs)):
    workingStr=strOfStrs[y].split('n')
    curDr=0
    for x in range(len(workingStr)):
        if (workingStr[x] in preEvents) and (x!=0):
            pathDurs.append(curDr)
            curDr=int(dat5[int(workingStr[x])-1])
        else:
            curDr+=int(dat5[int(workingStr[x])-1])
    pathDurs.append(curDr)
    
    for x in range(len(workingStr)):
        if workingStr[x] in preEvents:
            curMar=0
            if x!=0:
                pathMars.append(curMar)
        else:
            nextMar=dateCont(dat4[int(workingStr[x-1])-1],dat3[int(workingStr[x])-1]).days-1
            curMar+=nextMar
    pathMars.append(curMar)
prettyPaths=[]
for y in range(len(strOfStrs)):
    workStr=''
    for x in range(len(strOfStrs[y])):
        if strOfStrs[y][x]=='n':
            workStr=workStr+'->'
        else:
            workStr=workStr+strOfStrs[y][x]
    prettyPaths.append(workStr)
print('The unique paths through the schedule are...')
for y in range(len(strOfStrs)):
    print(prettyPaths[y],'is',pathDurs[y],'task days long with',pathMars[y],'days of calendar margin.')
    
#SRA code time
masterPath=[]
avgPaths=[]
origPaths=[]
for z in range(len(strOfStrs)):
    print('----path',z+1,'----')
    currentPath=strOfStrs[z].split('n')
    cDiff=[]
    cOpt=[]
    cPes=[]
    cDelta=[]
    for y in range(len(currentPath)):
        for x in range(len(dat2)):
            if currentPath[y]==dat2[x]:
                cDiff.append(dat5[x])
                cOpt.append(dat6[x])
                cPes.append(dat7[x])
                cDelta.append(dat8[x])
    origPaths.append(sum(cDiff))
    avgSums=[]
    for y in range(itns):
        revisedDurs=[]
        for x in range(len(cDiff)):
            if cDelta[x]=='tpe':
                revisedDurs.append(triPointEst(cOpt[x],cDiff[x],cPes[x]))
            else:
                deltaVar=float(cDelta[x])
                revisedDurs.append(betaRectangular(cDiff[x],cOpt[x],cPes[x],deltaVar))
        masterPath.append(round(sum(revisedDurs)))
        avgSums.append(round(sum(revisedDurs)))
    avgPaths.append(sum(avgSums))
avgPaths=[avgPaths[x]/itns for x in range(len(avgPaths))]

dart=len(strOfStrs)
durListSum=[]
durListMax=[]
durListWinner=[]
cpWinners=[]
for x in range(itns):
    durList=[]
    for y in range(dart):
        durList.append(masterPath[itns*y+x])
    durWin=max(durList)
    cpWinners.append(durWin)
    for y in range(dart):
        if durWin==durList[y]:
            durListWinner.append(y+1)
    durListSum.append(sum(durList))
    
riskyEvents=[0]*len(dat2)
eventWeights=[0]*len(dat2)
for x in range(len(durListWinner)):
    workVal=durListWinner[x]-1
    workList=strOfStrs[workVal].split('n')
    for y in range(len(workList)):
        for z in range(len(riskyEvents)):
            if workList[y]==dat2[z]:
                riskyEvents[z]+=1
riskMax=max(riskyEvents)

#path weight calc
percDurs=dart*[0]
percVals=[x+1 for x in range(dart+1)]
for x in range(itns):
    for y in range(len(percVals)):
        if durListWinner[x]==percVals[y]:
            percDurs[y]+=1
percDurs=[percDurs[x]/itns for x in range(len(percDurs))]
print('')
dartWeights=[]
for x in range(dart):
    wt=round(percDurs[x]*100,2)
    dartWeights.append(wt)
    print('Path',x+1,'was the critical path',wt,'% of the time.')
    print('Avg duration:',round(avgPaths[x],1))
    print('Original Duration:',origPaths[x])
    print('')

print('Some more info..')
print('The traditional CP is:',max(origPaths))
wtDurs=[(dartWeights[x]/100)*avgPaths[x] for x in range(dart)]
print('The weighted project duration is:',sum(wtDurs))
print('\n')

totalWeights=[0]*len(dat2)
for x in range(len(strOfStrs)):
    workStr=strOfStrs[x].split('n')
    for y in range(len(dat2)):
        if dat2[y] in workStr:
            totalWeights[y]+=dartWeights[x]
print('event   weight (%)')
print('----------------------')
for x in range(len(dat2)):
    event=str(dat2[x])
    weight=str(totalWeights[x])
    if len(weight)>6:
        weight=weight[:5]
    strStitch='{:6s} |  {:6s}'.format(event,weight)
    print(strStitch)
    
maxPath=max(percDurs)
for x in range(dart):
    if percDurs[x]==maxPath:
        maxIndex=x
cpHistData=[cpWinners[x] for x in range(len(cpWinners))]
minSums=min(cpHistData)
maxSums=max(cpHistData)

#percentage bands
cpHistData.sort()
wData=[cpHistData[x] for x in range(len(cpHistData))]
itnsVal=itns
cont=True
while cont:
    if itnsVal%10!=0:
        itnsVal-=1
    elif itnsVal%10==0:
        cont=False
wData=wData[0:itnsVal]
wDataTen=int(len(wData)/10)
wMedian=int(len(wData)/2)
print('Median:',wData[wMedian])
print('+/- 10% interval: (',wData[wMedian-wDataTen],",",wData[wMedian+wDataTen],')')
print('+/- 20% interval: (',wData[wMedian-wDataTen*2],",",wData[wMedian+wDataTen*2],')')
print('+/- 30% interval: (',wData[wMedian-wDataTen*3],",",wData[wMedian+wDataTen*3],')')

#histogram bins
nbins=maxSums-minSums+1
binData=[0]*nbins
binVals=[x for x in range(int(minSums),int(maxSums+1))]
for x in range(nbins):
    for y in range(len(cpHistData)):
        if binVals[x]==cpHistData[y]:
            binData[x]+=1
print('histogram bin range:',minSums,'...',maxSums)

curVal=0
sumBins=[]
for x in range(len(binData)):
    curVal+=(binData[x]/itns)
    sumBins.append(curVal)

#final i/o
rd='data_folder\sra_results.csv'
f=open(rd,'w')
f.write('durs,counts,fraction\n')
for x in range(len(binData)):
    a=str(binVals[x])
    b=str(binData[x])
    c=str(sumBins[x])
    value=str(a+','+b+','+c+'\n')
    f.write(value)
f.write('event_name,criticality\n')
for x in range(len(dat2)):
    a=str(dat2[x])
    b=str(totalWeights[x])
    val=str(a+','+b+','+'\n')
    f.write(val)
f.close()
    
    
    

















































