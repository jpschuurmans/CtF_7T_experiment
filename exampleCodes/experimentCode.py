#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:06:24 2020

Experiment code - temporal masking, blocked-design
intact, negated and scrambled faces with their phase scrambled mask. 
4 durations

@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data
import os
import numpy as np
import glob
from PIL import Image
import random
import copy



#%% =============================================================================

# a block contains 20 unique images + their mask
monRR = 60 # refresh rate on monitor is 60Hz
frame = 1000/monRR # one 
durCond = [3, 5, 6, 9] #50, 83.33, 100, 150 ms
durCondNames = [str(int(durCond[0]*frame)),str(int(durCond[1]*frame)),str(int(durCond[2]*frame)),str(int(durCond[3]*frame))]
typCond = ['Int', 'Neg', 'Scr']
sfType = ['LSF', 'HSF']
nCond = len(durCond)*len(typCond)*len(sfType) #nr of conditions = 24

nBlockPerCond = 20 #nr of blocks per condition (in total)
nUniBlocks = int(nBlockPerCond/2) #nr of unique blocks per condition = 10 (10 sequences to make)
nBlocks = nCond*nBlockPerCond # 264 blocks in total

nRuns = 20 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)

durBlock = 10 # seconds
nStim = 20 # stimuli per block
nPositions = 24 # 24 positions in a block (for stim distribution)

fixStEn = 12 # Duration of fixation at begin/end of run in ms

colourChange = (0.8, 1.0, 1.0) #(0, 1.0, 1.0) = too red

#%% =============================================================================
#paths
baseFolder = ''
#commented out, this is just for testing in Spyder
#baseFolder = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\mainExpCode\\'

dataPath = baseFolder + 'data'
stimPath = baseFolder + 'stimuli'
backPath = baseFolder + 'background'
seqLocation = baseFolder + 'sequence_withinBlock.txt'


#%% =============================================================================
# in case we need to shut down the expt

def esc():
    if 'escape' in last_response:
        logfile.close()
        eventfile.close()
        win.mouseVisible = True
        win.close()
        core.quit
#%% =============================================================================
# Store info about the experiment session
# Get subject participant ID and run nr through a dialog box
expName = 'Recurrent face processing in V1'
expInfo = {
        '1. Participant ID': '',
        '2. Run number': ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'),
        '3. Screen hight in px': '1080', #1080
        '4. Screen width in px': '1920', #1920
        '5. Make sequence?': ('no','yes')
        }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

dataPath = os.path.join(dataPath, expInfo['1. Participant ID'])

# Make sure there is a path to write away the data
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)

runNr = int(expInfo['2. Run number'])

scrsize = (int(expInfo['4. Screen width in px']),int(expInfo['3. Screen hight in px']))
    
# make a text file to save data with 'comma-separated-values'
eventName = expInfo['1. Participant ID'] + '_task-mainExp_run-' + expInfo['2. Run number'] + '_events.csv'
eventFname = os.path.join(dataPath, eventName)

dataName = expInfo['1. Participant ID'] + '_run' + expInfo['2. Run number'] + '_' + expInfo['date'] + '.csv'
dataFname = os.path.join(dataPath, dataName)


logfile = open(dataFname, 'w')
logfile.write('BlockNumber,PositionInRun,PositionInBlock,TrialNumber,ConditionName,SpatialFrequency,TrialStart,TrialDuration,StimDuration,MaskDuration,NumberOfStimulusFrames,ImageFileName,MaskFileName,BackFrame,CatchTrial,Keypress,ResponseStamp,ResponseTime\n')

eventfile = open(eventFname, 'w')
eventfile.write('onset, duration, trial_type\n')


stimSize = 550

if expInfo['5. Make sequence?'] == 'yes':
    sequence_path = os.path.join(baseFolder + 'sequence_creator.py')
    exec(open(sequence_path).read())



#%% =============================================================================
#make or load block order for participant
path_blockSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'blockSeq.txt')
path_backSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'backSeq.txt')
path_blockCount = os.path.join(dataPath, expInfo['1. Participant ID'] + 'blockCount.txt')
path_stimSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'stimSeq.txt')

blockSeq = []
backSeq = []
stimSeq = []

# opening the block sequence list
with open(path_blockSeq, 'r') as f:
    mystring = f.read()
my_list = mystring.split("\n")
for item in my_list:
    line = item.split(',')
    line.remove('')
    new_line = [int(i) for i in line]
    blockSeq.append(new_line)
blockSeq.remove([])  


# opening the background sequence list
with open(path_backSeq, 'r') as f:
    mystring = f.read()
my_list = mystring.split("\n")
for item in my_list:
    line = item.split(',')
    line.remove('')
    new_line = [int(i) for i in line]
    backSeq.append(new_line)
backSeq.remove([])


# opening the stimulus sequence list
with open(path_stimSeq, 'r') as f:
    mystring = f.read()
my_list = mystring.split("\n")
for item in my_list:
    line = item.split(',')
    line.remove('')
    new_line = [int(i) for i in line]
    stimSeq.append(new_line)
stimSeq.remove([])    


#%% =============================================================================
#stim settings
runSeq =  blockSeq[runNr-1] #sequence of blocks within the current run


faceNames = []
maskLSFNames = []
maskHSFNames = []
for times in range(nUniBlocks):
    if times < 9:
        name = 'bg0' + str(times+1)
    else:
        name = 'bg' + str(times+1)
    
    stimSpecBack = glob.glob(os.path.join(stimPath, name + '*Stim*.bmp'))
    stimSpecBack.sort()
    maskLSFSpecBack = glob.glob(os.path.join(stimPath, name + '*MaskLSF*.bmp'))
    maskLSFSpecBack.sort()
    maskHSFSpecBack = glob.glob(os.path.join(stimPath, name + '*MaskHSF*.bmp'))
    maskHSFSpecBack.sort()    
    faceNames.append(stimSpecBack)
    #maskNames.append(maskSpecBack)
    maskLSFNames.append(maskLSFSpecBack)
    maskHSFNames.append(maskHSFSpecBack)

backNames = glob.glob(os.path.join(backPath, '*.bmp'))
backNames.sort()


allTrialsOrder = []
stimPos = list(range(nPositions)) #possible positions within a block
blockPos = 1

#For shuffle every run
blockCount = list(np.zeros(nCond)) #there are 24 conditions.
blockCount = [x+(runNr-1) for x in blockCount]

#creating a trials order for all 

for blockNr in runSeq: #loop through blocks in specific run
    stimSeqNr = int(blockNr+(blockCount[blockNr])) #i.e. block 1 starts with stim sequence 1
    if stimSeqNr > 19: # there are only 20 sequences (0-19)..  
        stimSeqNr = int(stimSeqNr - 24) #so when an index is above 19.. start over from start (0)
    trials = stimSeq[stimSeqNr] #get specific stim order for this block
    trialNumber = 0
    #select the correct back frame -> backSeq[block][run]
    backType = backSeq[blockNr][int(blockCount[blockNr])]
    if backType < 9:
        backName = 'bg0' + str(backType+1)
    else:
        backName = 'bg' + str(backType+1)
    back = [i for i in backNames if (backName + '.bmp') in i]
    blockFaceNames = faceNames[backType]
    blockMaskLSFNames = maskLSFNames[backType]
    blockMaskHSFNames = maskHSFNames[backType]
    
    # decide which trials will be catch trials
    # 2 per block, one in first half other in second half
    catchList = list(np.zeros(int(nPositions/2)))
    catchList[0]=1
    random.shuffle(catchList)
    while catchList[0] == 1:
        random.shuffle(catchList)
    toAdd = copy.deepcopy(catchList)
    random.shuffle(toAdd)
    catchList.extend(toAdd)
    
    #condition/block numbers, to make it more clear:
    #LSF		50		83.3	100	    150
    #int		1		7		13		19
    #neg		2		8		14		20
    #scr		3		9		15		21
    
    #HSF		50		83.3	100	    150
    #int		4		10		16		22
    #neg		5		11		17		23
    #scr		6		12		18		24    
    #,13,16,19,22
    
    
    for position in stimPos: #if position contains no stims, no im/mask/trailnr 
        image = None 
        mask = None
        maskType = None
        trialNr = None
        condiName = None
        #if there is a trial for the specific position, give it correct timing info
        if any(map((lambda value: value == blockNr), (0,1,2,3,4,5))): #50ms
            stimFr = durCond[0]
            duration = durCondNames[0] +'ms'
        elif any(map((lambda value: value == blockNr), (6,7,8,9,10,11))): #83ms
            stimFr = durCond[1]
            duration = durCondNames[1] +'ms'
        elif any(map((lambda value: value == blockNr), (12,13,14,15,16,17))):#100ms
            stimFr = durCond[2]
            duration = durCondNames[2] +'ms'
        elif any(map((lambda value: value == blockNr), (18,19,20,21,22,23))):#150ms
            stimFr = durCond[3]
            duration = durCondNames[3] +'ms'
            
        if any(map((lambda value: value == blockNr), (0,3,6,9,12,15,18,21))): #intact stim
            trType = 0
        elif any(map((lambda value: value == blockNr), (1,4,7,10,13,16,19,22))): #neg stim
            trType = 20
        elif any(map((lambda value: value == blockNr), (2,5,8,11,14,17,20,23))): #scr
            trType = 40
        
        if any(map((lambda value: value == blockNr), (0,1,2,6,7,8,12,13,14,18,19,20))): #LSF
            maskset = blockMaskLSFNames;
        elif any(map((lambda value: value == blockNr), (3,4,5,9,10,11,15,16,17,21,22,23))): #HSF
            maskset = blockMaskHSFNames;
        if position in trials:
            #index = np.where(trials == position)
            index = trials.index(position)
            image = blockFaceNames[index+trType][-19:]
            mask = maskset[index+trType][-22:]
            maskType = mask[12:-7]
            trialNumber += 1
            trialNr  = trialNumber
            condiName = image[5:8] + '_' + duration
        allTrialsOrder.append({'blockNr' : blockNr+1,
                               'posInRun': blockPos,
                               'posInBlock' : position+1,
                               'trialNr': trialNr,
                               'condName': condiName,
                               'stimFrames': stimFr,
                               'imageName': image,
                               'maskName': mask,
                               'maskType' : maskType,
                               'backFrame': back[0][-8:],
                               'nrOfBlockOccurenceInExp': blockCount[blockNr],
                               'catchTrial': catchList[position]})
    blockPos += 1
    blockCount[blockNr] += 1
    


trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)
#%% =============================================================================
#loading the checkerboards for the last part of the run
checkerboards = []
checkerboards.append(glob.glob(os.path.join(dataPath, '*Back.bmp')))
checkerboards.append(glob.glob(os.path.join(dataPath, '*Face.bmp')))


#%% =============================================================================
#window setup

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)
#win.close()

frameRate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
print('framerate is', frameRate)

#cra
instruc01 = 'Welcome!\nHopefully you are comfortable and relaxed.\n\nDuring this experiment you will see faces flashed on the screen.\nThe only thing you should do\nis press a button when the colour changes.\n\nPress a button to continue.\n(1 -> buttonbox key)'
instruc01 = visual.TextStim(win, color='black', height=32, text=instruc01)
instruc02 = 'The experiment is about to start!\n\n Waiting for the scanner trigger.. (s)'
instruc02 = visual.TextStim(win, color='black',height=32,text=instruc02)

#create fixation cross
fix1=visual.Line(win,start=(-stimSize,-stimSize),end=(stimSize, stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
fix2=visual.Line(win,start=(-stimSize,stimSize),end=(stimSize, -stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')


instruc01.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

instruc02.draw()
win.flip()
while not 's' in event.getKeys():
    core.wait(0.1)
    
win.mouseVisible = False
# =============================================================================

# start stopwatch clock
clock = core.Clock()
clock.reset()

# =============================================================================
# clear any previous presses/escapes
last_response = ''; response_time = ''; reactionTime = '';
response = []

esc() # in case we need to shut down the expt

# =============================================================================
trialCount = 1
fr2 = 10
totalFr = 25 #total nr of trialframes is 25 = 416ms
trNum = 0
corrResp = 0; totalCatch = 0; ok = 2 #all necessary for the task
#draw fixation cross
fix1.setAutoDraw(True)
fix2.setAutoDraw(True)
fixEnd = 0

#win.close()
for trial in trialsReady:
    if trialCount == 1 or trialCount % nPositions == 1: #beginning fixation
        #if trialCount >= 4 and trialCount % nPositions == 1:
            #win.saveMovieFrames(name) #for saving the exp trial -> saves all frames 
        #create catchlist for the following block
        fixStart  = clock.getTime() #start tracking time trialCount =30
        
        if trialCount != 1:
            toSave2 = str(fixEnd) + ',' + str((fixStart-fixEnd)) + ',' +str(trial['condName']) + '\n'
            eventfile.write(toSave2) 
            
            
        win.flip()
        stim1=[]
        stim2=[]
        stim3=[]
        fr1=[]
        fr3=[]
        catchyCatch = []
        #load images for the next block
        for ii in range(nPositions):
            if allTrialsOrder[trNum]['trialNr'] == None: #if the trial doesnt contain a stimulus
                if allTrialsOrder[trNum]['catchTrial'] == True:
                    col = colourChange 
                else:
                    col = (1.0, 1.0, 1.0)
                im1 = Image.open(os.path.join(backPath, allTrialsOrder[trNum]['backFrame']))
                stim1.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im1,color=col))
                im2 = Image.open(os.path.join(backPath, allTrialsOrder[trNum]['backFrame']))
                stim2.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im2,color=col))
                im3 = Image.open(os.path.join(backPath, allTrialsOrder[trNum]['backFrame']))
                stim3.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im3,color=col))
                fr1.append(fr2)
                fr3.append((totalFr - fr2)-fr2)
            else:
                if allTrialsOrder[trNum]['catchTrial'] == True:
                    col = colourChange
                else:
                    col = (1.0, 1.0, 1.0)
                im1 = Image.open(os.path.join(stimPath, allTrialsOrder[trNum]['imageName']))
                stim1.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im1,color=col))
                im2 = Image.open(os.path.join(stimPath, allTrialsOrder[trNum]['maskName']))
                stim2.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im2,color=col))
                im3 = Image.open(os.path.join(backPath, allTrialsOrder[trNum]['backFrame']))
                stim3.append(visual.ImageStim(win, size=[stimSize,stimSize],image=im3,color=col))

                fr1.append(allTrialsOrder[trNum]['stimFrames'])
                fr3.append((totalFr - fr2) - allTrialsOrder[trNum]['stimFrames'])
                
            trNum += 1        
        
        #if clock hits the fixation time for start/end in seconds, end the fixation
        loadEnd = clock.getTime()
        loadTime = loadEnd-fixStart
        x=1
        if trialCount == 1:
            while x==1: 
                fixNow = clock.getTime()
                timeFix = fixNow-fixStart
                if timeFix > (fixStEn-1): # time to fixate more then 11 seconds? end
                    x=2
        else:
            while x==1: 
                fixNow = clock.getTime()   
                timeFix = fixNow-fixStart
                if timeFix > 9: # time to fixate more then 9 seconds? end
                    x=2
        for nFrames in range(60):  #last second of fixation start flipping, to prevent frame drops later on
            win.flip()            
        fixEnd = clock.getTime()
        toSave = str(int(trial['blockNr'])) + ',' + str(trial['posInRun']) +',0,0,'+ 'fixation,None,fix start: '+str(fixStart)+',fix dur: '+ str(round((timeFix)*1000)+1000) + ',load dur: ' + str(round(loadTime*1000)) + ',None,None,None,None,None,None,None,None,None\n'
        logfile.write(toSave)
        toSave2 = str(fixStart) + ',' + str((fixEnd-fixStart)) + ',fixation\n'
        eventfile.write(toSave2)
        
        print('fixation, dur: ' + str(round((timeFix)*1000)+1000) + ',load dur: ' + str(round(loadTime*1000)) + ' ms')       
        # name = (dataPath + str(trial['condName']) +'_'+ str(trial['maskType'])+'.png')#for saving the exp trial -> save name of frames 

    startTrial = clock.getTime()
    response = event.getKeys(timeStamped=clock) #check for responses to target
    esc()
    if trial['catchTrial'] == True: #if its a catchtrail, start the clock
        catchStart = clock.getTime()
        totalCatch += 1
        if ok == 0:
            corrResp += 1
        ok = 1
    elif not response == [] and ok == 1: #check for responses to target
        last_response = response[-1][0] # most recent response, first in tuple
        response_time = response[-1][1]
        ok = 0
        reactionTime = (response_time - catchStart)*1000
        print('CLICK!! The reactiontime is ', reactionTime, 'ms' )

    for nFrames in range(fr1[trial['posInBlock']-1]): #stimulus
        stim1[trial['posInBlock']-1].draw()
        #win.getMovieFrame(buffer = 'back') #for saving the exp trial -> saves all frames 
        win.flip()
    afterStim = clock.getTime()
    stimDur = afterStim - startTrial
    for nFrames in range(fr2): # mask
        stim2[trial['posInBlock']-1].draw()
        #win.getMovieFrame(buffer = 'back') #for saving the exp trial -> saves all frames 
        win.flip()
    afterMask = clock.getTime()
    maskDur = afterMask - afterStim
    for nFrames in range(fr3[trial['posInBlock']-1]): #background
        stim3[trial['posInBlock']-1].draw()
        #win.getMovieFrame(buffer = 'back')   #for saving the exp trial -> saves all frames    
        win.flip()
    if not response == [] and ok == 1: #check for responses to target
        last_response = response[-1][0] # most recent response, first in tuple
        response_time = response[-1][1]
        ok = 0
        reactionTime = (response_time - catchStart)*1000
        print('CLICK!! The reactiontime is ', reactionTime, 'ms' )
    endTrial = clock.getTime()
    trialDuration = round((endTrial-startTrial)*1000)

    
    print(trial['condName'],' - ',trial['maskType'] ,'block:', int(trial['blockNr']),', trial', int(trialCount),
          ', trial time: ', round((endTrial-startTrial)*1000), 'ms')
    toSave = str(trial['blockNr'])+','+str(trial['posInRun'])+','+str(trial['posInBlock'])+','+str(trial['trialNr']) +','+ str(trial['condName']) +','+ str(trial['maskType'])+','+ str(startTrial)+','+ str(trialDuration) +','+ str(round(stimDur*1000)) +','+ str(round(maskDur*1000)) +','+ str(trial['stimFrames']) +','+ str(trial['imageName']) +','+ str(trial['maskName']) +','+ str(trial['backFrame'])+','+ str(int(trial['catchTrial']))+','+str(last_response)+','+str(response_time)+','+str(reactionTime)+'\n' 
    logfile.write(toSave)
    
    if not last_response == '': #empry responses if it's already logged
        esc() # in case we need to shut down the expt
        last_response = ''; response_time = ''; reactionTime = '';
        response = []
    trialCount  += 1
if ok == 0:
    corrResp += 1
    
#one more normal fixation
fixStart = clock.getTime()
for nFrames in range(600): # 600 = 10 seconds
    win.flip()
fixNow = clock.getTime()
timeFix = fixNow-fixStart 
toSave = str(int(trial['blockNr'])) + ',' + str(trial['posInRun']) +',0,0,'+ 'fixation,None,fix start: '+str(fixStart)+',fix dur: '+ str(round(timeFix)*1000) + ',None,None,None,None,None,None,None,None,None,None\n'
logfile.write(toSave)
toSave2 = str(fixStart) + ',' + str(timeFix) + ',fixation\n'
eventfile.write(toSave2)

#final face chackerboard, then background checkerboard    
for checks in range(2): #checks=1 is face checks=0 is background
    #per part, 10 seconds. 1 cicle (ori+inv) will show 4 times per sec. 
    checkerOri = visual.ImageStim(win=win,size=[stimSize,stimSize], image=Image.open(checkerboards[[checks][0]][1]))
    checkerInv = visual.ImageStim(win=win,size=[stimSize,stimSize], image=Image.open(checkerboards[[checks][0]][0]))
    checkerTimeStart= clock.getTime()
    for times in range(30):
        for nFrames in range(10): #6 frames = 100ms each -> 5Hz(or10)
            checkerOri.draw()
            win.flip()
        for nFrames in range(10): #10 frames = 166.6ms each -> 3Hz (or6)
            checkerInv.draw()
            win.flip()
            
    checkerTimeEnd = clock.getTime()
    checkerTimeTotal = checkerTimeEnd-checkerTimeStart
    print('it took ' + str(checkerTimeTotal) + 'ms')
   
    if checks == 1:
        checkName = 'face checkers'
    else:
        checkName = 'back checkers'
       
    toSave = checkName + ',3Hz aka 6Hz,0,0,'+ 'checkerboard,None,checker start: '+str(checkerTimeStart)+',checker dur: '+ str(round(checkerTimeTotal)*1000) + ',None,'+str(checkerboards[[checks][0]][1][-19:])+','+str(checkerboards[[checks][0]][0][-19:])+',None,None,None,None,None\n'
    logfile.write(toSave)
    toSave2 = str(checkerTimeStart) + ',' + str(checkerTimeTotal) + ',' + str(checkerboards[[checks][0]][1][-19:]) + '\n'
    eventfile.write(toSave2)

#finalfixationnnn
fixStart = clock.getTime()
for nFrames in range(monRR*fixStEn): # 12 sec --> end fixation*refreshrate
    win.flip()
fixNow = clock.getTime()
timeFix = fixNow-fixStart 
toSave = 'EndFixatione,final,0,0,'+ 'fixation,fix start: '+str(fixStart)+',fix dur: '+ str(round(timeFix)*1000) + ',None,None,None,None,None,None,None,None,None,None\n'
logfile.write(toSave)
toSave2 = str(fixStart) + ',' + str(timeFix) + ',fixation\n'
eventfile.write(toSave2)
    
fix1.setAutoDraw(False)
fix2.setAutoDraw(False)
win.mouseVisible = True

totExpDur = clock.getTime()
percCorr = (100/totalCatch)*corrResp
toSave = 'Total run duration: ' + str(totExpDur) + '\nPercentage correct = ' + str(percCorr)
logfile.write(toSave)

instruc03 = 'This is the end of run ' + str(runNr) + ' out of 20\n\nYou have a score of ' + str(round(percCorr)) + '%\nThank you for paying attention :)\n\nPress \'x\' to close the screen.'
instruc03 = visual.TextStim(win, color='black',height=32,text=instruc03)
instruc03.draw()
win.flip()
while not 'x' in event.getKeys():
    core.wait(0.1)

print('time exp: ', int(clock.getTime()))
  
logfile.close()
eventfile.close()
win.close()



