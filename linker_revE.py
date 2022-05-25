# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 21:14:03 2021

@author: Jimmy
"""
'''
dat2=['1','2','3','4','5','6','7','8','9','10','11','12','13'] #event ID
dat9=['2m6','3','4m5','na','7m8','5','9','9','10','11m12','na','13','na'] #links
preEvents=['1']
checkOutput=['1n2n3n5n7n9n10n13','1n2n4n6n7n9n10n13','1n2n3n5n7n9n10n11n12',
             '1n2n4n6n7n9n10n11n12','1n8n9n10n11n12','1n8n9n10n13','14n8n9n10n13',
             '14n8n9n10n11n12']
'''
def linker(dat2,dat9,preEvents):
#determine starting points
#break up dat9 and dat2
#this block re-lists the inputs 
    dat2Broke=[]
    dat9Broke=[]
    for x in range(len(dat9)):
        if dat9[x]=='na':
            dat2Broke.append(dat2[x])
            dat9Broke.append(dat9[x])
        elif 'm' in dat9[x]:
            workList=dat9[x].split('m')
            for y in range(len(workList)):
                dat2Broke.append(dat2[x])
                dat9Broke.append(workList[y])
        else:
            dat2Broke.append(dat2[x])
            dat9Broke.append(dat9[x])
    
    #print(dat2Broke)
    #print(dat9Broke)
    
    #find starting points
    startPts=[]
    for x in range(len(dat2)):
        if dat2[x] not in dat9Broke:
            startPts.append(dat2[x])
    #print('starting points:',startPts)
    
    #find junctions (if an event is the link multiple times, it is a junction point)
    datJunct=[]
    for x in range(len(dat2)):
        ct=0
        if dat2[x] in dat9Broke:
            for y in range(len(dat9Broke)):
                if dat9Broke[y]==dat2[x]:
                    ct+=1
        if ct > 1:
            datJunct.append(dat2[x])
    #print('junctions:',datJunct)
    
    #find branches
    datBran=[]
    for x in range(len(dat2)):
        ct=0
        for y in range(len(dat2Broke)):
            if dat2[x] == dat2Broke[y]:
                ct+=1
        if ct > 1:
            datBran.append(dat2[x])
    #print('branches:',datBran)
            
    
    #find end points?
    endPts=[]
    for x in range(len(dat2Broke)):
        if dat9Broke[x]=='na':
            endPts.append(dat2Broke[x])
    #print('end points:',endPts)
    
    listOfPairs=[]
    for x in range(len(dat2Broke)):
        workingStr=dat2Broke[x]+'q'+dat9Broke[x]
        listOfPairs.append(workingStr)
    
    #find starting pairs
    startPairs=[]
    for x in range(len(listOfPairs)):
        workVar=listOfPairs[x].split('q')[0]
        if workVar in startPts:
            startPairs.append(listOfPairs[x])
    
    #meat and potato
    finalPaths=[]
    listOfPaths=[]
    count=0
    cont=True
    while cont:
        if count==0:
            for x in range(len(listOfPairs)):
                curPath=listOfPairs[x]
                curPathVals=curPath.split('q')
                for y in range(len(listOfPairs)):
                    matchVal=listOfPairs[y].split('q')
                    if curPathVals[1]==matchVal[0]:
                        listOfPaths.append(curPath+'q'+matchVal[1])
            count+=1
        elif count > 0:
            addlPaths=[]
            for x in range(len(listOfPaths)):
                curPath=listOfPaths[x]
                curPathCheck=len(curPath.split('q'))
                curPathEnd=curPath.split('q')[curPathCheck-1]
                for y in range(len(listOfPairs)):
                    matchVal=listOfPairs[y].split('q')
                    if curPathEnd==matchVal[0]:
                        addlPaths.append(curPath+'q'+matchVal[1])
            for x in range(len(addlPaths)):
                pathLen=len(addlPaths[x])
                if addlPaths[x].split('q')[0] in startPts:
                    addlPathStr=addlPaths[x].split('q')
                    lenPath=len(addlPathStr)
                    if addlPathStr[lenPath-1]=='na':
                        finalPaths.append(addlPaths[x])
            listOfPaths=[addlPaths[x] for x in range(len(addlPaths))]
            count+=1
            if len(listOfPaths)==0:
                cont=False
    #split via q and then stitch with n to get right formatting
    finalPathsFormatted=[]
    for x in range(len(finalPaths)):
        workList=finalPaths[x].split('q')
        workStr=''
        for y in range(len(workList)):
            if workList[y]!='na':
                workStr=workStr+'n'+workList[y]
        workStr=workStr[1:]
        finalPathsFormatted.append(workStr)
    return(finalPathsFormatted)
