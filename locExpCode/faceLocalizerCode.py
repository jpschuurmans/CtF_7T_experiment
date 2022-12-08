#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block design
Created on Tue Jan 28 14:22:20 2020
@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data
import os  
import numpy.random as rnd          # for random number generators
import glob
import numpy as np
import random
import copy
from PIL import Image

#%% =============================================================================
# Experimental settings for 1 run

nStim = 20 #number of unique stimuli per condition

nCond = 6 # nr of total conditions
conditions = list(range(1,nCond+1))
nBlocks = 6 # nr of blocks per condition

blockDur = 10 # Duration of block in sec
fixDur = 10 # Duration of fixation in sec (fix after every block)
fixStEn = 12 # Duration of fixation at begin/end of run in ms

trPerBlock = 10 #nr of trials per block

trialDur = 0.5 # Durations of trials defined in ms
isi = 0.5 #duration of inter stimulus 

colourChange = (1.0, 1.0, 0.8)

#%% =============================================================================
# paths
basefolder = '' 
#commented out, this is just for testing in Spyder
#basefolder = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\locExpCode\\' 

stimPath = basefolder + 'stimuli'
dataPath = basefolder + 'data'

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
        
# Get subject name, gender, age, handedness through a dialog box
expName = 'Recurrent face processing in V1'
expInfo = {
        'Participant ID': ''
        }    

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

# Make sure there is a path to write away the data
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)

# make a text file to save data with 'comma-separated-values'
eventName = expInfo['Participant ID'] + '_task-funcLoc__events.csv'
eventFname = os.path.join(dataPath, eventName)

dataName = expInfo['Participant ID'] + '_faceLoc_' + expInfo['date'] + '.csv'
dataFname = os.path.join(dataPath, dataName)

logfile = open(dataFname, 'w')
logfile.write('BlockNumber, TrialNumber, StimulusType, ImageName, StimOnset, StimOffset, CatchTrial, Response, ResponseTime \n')

eventfile = open(eventFname, 'w')
eventfile.write('onset, duration, trial_type\n')

#%% =============================================================================
# create stimuli

#get all stimuli from the folder
stimPathList = glob.glob(os.path.join(stimPath,'*.bmp'))

#Check if all images exist
if not len(stimPathList) == (nStim*nCond):
    raise Exception('Images not complete')

#the extention of the used images is:
item01 =stimPathList[1]
imExt = item01[-4:]
lenStimName = len(item01[len(stimPath)+1:])

#create a list with the stimulus names
stimName=[]
for image in stimPathList:
    stimName.append(image[-lenStimName:])
stimName.sort()

#split list for all conditions
w=0
v=0
condList=[]
for unit in conditions:
    sliceStimList = slice(w,w+nStim,1) 
    stimListThisCon = stimName[sliceStimList]
    w += nStim
        
    #shuffle +append shuffeled. softcoded, but should be now: 3 times
    #(6 blocks per cond, 10 trials per block, and 20 unique stimuli in total --> 20*3)
    repTimes = int((nBlocks*trPerBlock)/nStim)
    shufStimList = []
    for shuff in range(repTimes):
        rnd.shuffle(stimListThisCon)
        toAdd = list(stimListThisCon)
        shufStimList.extend(toAdd)
    
    #splitting the 60 trials (nBlocks*trPerBlock) in 6 blocks (nBlock),
    u=0
    for num in list(range(1,nBlocks+1)):
        sliceTrials = slice(u,u+10,1)
        trialsCurrCon = shufStimList[sliceTrials]
        condList.append(trialsCurrCon)
        u += 10
        v += 1

#make a list for the nr of blocks
#making sure that same conditions never follow eachother
#and some conditions dont follow a specific condition more often than others
blockList = []
cond = copy.deepcopy(conditions)
posCombi = np.zeros((nCond,nCond))
step = nCond-1
for num in range(nBlocks):
    print(str(num))
    rnd.shuffle(cond)
    restart = True
    while restart:
        temPosCombi = copy.deepcopy(posCombi)
        for time in range(step):
            num1 = cond[time]-1
            num2 = cond[time+1]-1
            if num1 == num2 or temPosCombi[num1,num2] == 2:
                rnd.shuffle(cond)
                temPosCombi = copy.deepcopy(posCombi)
                break
            elif time == 4:
                if blockList == []:
                    toAdd = copy.deepcopy(cond)
                    blockList.extend(toAdd)
                    restart = False
                elif blockList[-1] == cond[0]: 
                    rnd.shuffle(cond)
                    temPosCombi = copy.deepcopy(posCombi)
                    break
                else:
                    toAdd = copy.deepcopy(cond)
                    blockList.extend(toAdd)
                    restart = False
            temPosCombi[num1,num2] += 1
        posCombi = copy.deepcopy(temPosCombi)




#get all 1... replace by 123456
#get all 2... replace by 789101112
#etc
x = len(blockList)-1
list.reverse(conditions)
for cond in conditions:
    i = 0
    for num in blockList:
        if num == cond:
            blockList[i] = x
            x -= 1
        i += 1

num1=blockList[24]-1
num2=blockList[25]-1


#make 1 big dictionary list
#append10 trials per condition in the order of the shuffled conditon list.
#et voila, un list des trials

r=0
s=1
allTrialsOrder = []
for blocks in blockList:
    blockNr = blockList[r]
    trials = condList[blockNr]
    q=0
    
    # decide which trials will be catch trials
    # 2 per block, one in first half other in second half
    catchList = list(np.zeros(int(trPerBlock/2)))
    catchList[0]=1
    random.shuffle(catchList)
    while catchList[0] == 1:
        random.shuffle(catchList)
    toAdd = copy.deepcopy(catchList)
    random.shuffle(toAdd)
    catchList.extend(toAdd)
    
    for amoun in trials:
        currTrial = trials[q]
        allTrialsOrder.append({'blockNr' : r+1,
                               'trialNr': s,
                               'condName': currTrial[0:8],
                               'imageName': currTrial,
                               'catchTrial': catchList[q]})
        q += 1
        s += 1
    r += 1
        

trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)

#%% =============================================================================

scrsize = (1920,1080)

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True) 
frameRate = win.getActualFrameRate()
print('framerate is' , frameRate)
#win.close()

instruct1 = 'During the experiment you\'ll see images appearing on the screen. \nPress a button as soon as you see the colour of the image change.\n\nIt is important to fixate on the fixation dot in the middle of the screen.\n\nPress a button to continue.. (buttonbox key = 1)'
instruct1 = visual.TextStim(win, height=32, text=instruct1)
instruct2 = 'The experiment is about to start!\nWaiting for scanner..\n(trigger = s)'
instruct2 = visual.TextStim(win, height=32, text=instruct2)
   
#create fixation cross
fix1=visual.Line(win,start=(-500,-500),end=(500, 500),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
fix2=visual.Line(win,start=(-500,500),end=(500, -500),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')

instruct1.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

instruct2.draw()
win.flip()
while not 's' in event.getKeys():
    core.wait(0.1)

# =============================================================================
# start stopwatch clock
clock = core.Clock()
clock.reset()

expt_time_elapsed = clock.getTime()
calc_baseline = fixStEn - expt_time_elapsed

# =============================================================================
# clear any previous presses/escapes
last_response = ''; response_time = ''

esc() # in case we need to shut down the expt

# =============================================================================

fix1.setAutoDraw(True)
fix2.setAutoDraw(True)
win.mouseVisible = False

for nFrames in range(720): #12sec
    win.flip()
toSave = 'StartFix,NA,StartFix,fix,' + str(expt_time_elapsed) +','+ str(clock.getTime()) + ',NA, NA, NA\n'
logfile.write(toSave)
toSave2 = str(expt_time_elapsed) +','+ str(clock.getTime()-expt_time_elapsed) + ',fixation\n'
eventfile.write(toSave2)

trialCount = 1
trialInBlock = 0
totCaught = 0
fixEndtime = clock.getTime()

for trial in trialsReady:
    trialOnsetTime = clock.getTime()
    
    if trial['catchTrial'] == True:
        col = colourChange
    else:
        col = (1.0, 1.0, 1.0)   
        
    im1 = Image.open(os.path.join(stimPath, trial['imageName']))
    bitmap = visual.ImageStim(win, size=[500,500],image=im1,color=col)
    
# =============================================================================

    esc() # in case we need to shut down the expt

# =============================================================================
    for nFrames in range(30): #500ms trail
        bitmap.draw()
        win.flip()            
    for nFrames in range(30): #500ms trail
        win.flip()
        
    # get response and it's associated timestamp as a list of tuples: (keypress, time)
    response = event.getKeys(timeStamped=clock)
    caught = 1
    esc()
    
    if not response:
        response = [('No_Response', -1)]
        caught = 0
        
    if trial['catchTrial'] == True and caught == True:
        totCaught += 1
        print('click!')
        
    last_response = response[-1][0] # most recent response, first in tuple
    response_time = response[-1][1] # most recent response, second in tuple

    condition = trial['condName']; whichBlock = trial['blockNr']; imName = trial['imageName']; catTrial = trial['catchTrial']
    toSave = str(whichBlock) +','+ str(trialCount) +','+ str(condition) +','+ str(imName) +','+ str(trialOnsetTime) +','+ str(clock.getTime()) +','+ str(catTrial)  +','+ str(last_response)  +','+ str(response_time)  +'\n' 
    logfile.write(toSave)

    print('trial: ', trialCount, ', trial type: ', condition)
    if trialCount % 10 == 0:
        trialOnsetTime = clock.getTime()
        
        toSave2 = str(fixEndtime) +','+ str(trialOnsetTime-fixEndtime) +','+  str(condition) + '\n'
        eventfile.write(toSave2)
        
        for nFrames in range(600): #10sec
            win.flip()

        condition = trial['condName']
        whichBlock = trial['blockNr']
        fixEndtime = clock.getTime()
        toSave = 'Fixation, NA, Fixation, fix,' + str(trialOnsetTime) +','+ str(fixEndtime) +','+ str(last_response) +','+ str(response_time) + '\n'
        logfile.write(toSave)
        toSave2 = str(trialOnsetTime) +','+ str(clock.getTime()-trialOnsetTime) + ',fixation\n'
        eventfile.write(toSave2)

    else:
        trialInBlock += 1
        
    trialCount  += 1
        
endExpTime = clock.getTime()
for nFrames in range(120): #(it already did 10, so 2sec left)
    win.flip()
toSave = 'EndFixation, NA, EndFixation, fix,' + str(endExpTime) +','+ str(clock.getTime()) +','+ str(last_response) +','+ str(response_time) + '\n'
logfile.write(toSave)
toSave2 = str(endExpTime) +','+ str(clock.getTime()-endExpTime) + ',fixation\n'
eventfile.write(toSave2)

fix1.setAutoDraw(False)
fix2.setAutoDraw(False)
win.mouseVisible = True
endExperiment = clock.getTime()
totalTimeExp = endExperiment - expt_time_elapsed

maxCat = (len(allTrialsOrder)/trPerBlock)*2
endScore = (100/maxCat)*totCaught
toSave = str(endScore) + 'percent of colour changes detected\nTotal experiment time: ' + str(round(totalTimeExp)) + ' minutes'
logfile.write(toSave)


instruct3 = 'Done!\n\nYou\'ve detected ' + str(endScore) +'% of the colour changes, thanks!\n\nPress \'x\' to close the screen.'
instruct3 = visual.TextStim(win, height=32, text=instruct3)
instruct3.draw()
win.flip()
while not 'x' in event.getKeys():
    core.wait(0.1)
    
# Quit the experiment (closing the window)
logfile.close()
eventfile.close()
win.close()
core.quit
