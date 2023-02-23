#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block design
Created on Tue Jan 28 14:22:20 2020
@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import monitors, visual, event, core, gui, data
import os
import numpy.random as rnd          # for random number generators
import glob
import numpy as np
import random
import copy
from PIL import Image
import _pickle as pickle
import itertools
import csv

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

trialDur = 500 # Durations of trials defined in ms
isi = 500 #duration of inter stimulus

colourChange = (1.0, 1.0, 0.8)

#%% =============================================================================
# paths
basefolder = ''
#commented out, this is just for testing in Spyder
#basefolder = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/locExpCode/'

stimPath = basefolder + 'stimuli'
dataPath = basefolder + 'data'

#%% =============================================================================
# in case we need to shut down the expt


def escape_check(keys,win,logfile,eventfile):
    if keys != []:
        # close window and logfile if escape is pressed
        if 'escape' in keys[0]:
            win.close()
            logfile.close()
            eventfile.close()
            core.quit()

def keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught):

    keys = event.getKeys(keyList=keyList, timeStamped=clock)
    if not keys == [] and caught == 0:
        escape_check(keys,win,logfile,eventfile)
        response_time = keys[-1][1]
        rt = (response_time - catchStart)*1000
        caught = 1
        print(f'Reactiontime is {int(rt)} ms' )
    elif not keys == []:
        escape_check(keys,win,logfile,eventfile)
    return rt, caught

#%% =============================================================================
# Store info about the experiment session

# Get subject name, gender, age, handedness through a dialog box
expName = 'Recurrent face processing in V1'
expInfo = {
        'Participant ID': '',
        'Run' : ('01','02'),
        'Screen' : ('BOLD', 'Dell', 'hp'),
        }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()

# Get date and time
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

run = expInfo['Run']

if expInfo['Screen'] == 'BOLD':
    mon = monitors.Monitor('BOLD_JS')
    mon.setDistance(210)
    mon.setGamma(2.06)
    frameRate = 120
    scrsize = [1920, 1080]
elif expInfo['Screen'] == 'Dell':
    mon = monitors.Monitor('Dell_JS')
    mon.setDistance(60)
    frameRate = 60
    scrsize = [1920, 1200]
elif expInfo['Screen'] == 'hp':
    mon = monitors.Monitor('hp')
    mon.setDistance(60)
    frameRate = 60
    scrsize = [1920, 1080]



framelength = 1000/(float(frameRate))
trialFr = round(trialDur/framelength)
isiFr = round(isi/framelength)

# Make sure there is a path to write away the data
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)


keyList = ['b','y','g','r','e','w','n','d','escape']

#%% =============================================================================
sequences_pickle = f'{dataPath}/{expInfo["Participant ID"]}fLoc_alltrials-list.pickle'

# create stimuli
if run == '01':
    print('Making sequence..')
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

    trialsReady = {}
    for blockid, blocks in enumerate(blockList):
        allTrialsOrder = []
        blockNr = blockList[blockid]
        trials = condList[blockNr]

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

        for trialid, amoun in enumerate(trials):
            currTrial = trials[trialid]
            allTrialsOrder.append({'blockNr' : blocks,
                                   'trialNr': trialid,
                                   'condName': currTrial[0:8],
                                   'imageName': currTrial,
                                   'stimOnset' : '',
                                   'stimOffset' : '',
                                   'stimDur' : '',
                                   'catchTrial': catchList[trialid],
                                   'rt' : ''})
        trialsReady[f'block-{blockid}'] = allTrialsOrder

    ###### pickle
    with open(sequences_pickle, 'wb') as file:
        pickle.dump(trialsReady, file)

    blocks = dict(itertools.islice(trialsReady.items(), 0 ,int(len(nBlocks*conditions)/2)))

elif run == '02':
    #load triallist dict (unpickle it)
    with open(sequences_pickle, 'rb') as file:
        trialsReady = pickle.load(file)

    blocks = dict(itertools.islice(trialsReady.items(), int(len(nBlocks*conditions)/2),len(nBlocks*conditions)))


#%% =============================================================================
# make a text file to save data with 'comma-separated-values'
# open log file
dataName = f'{dataPath}/{expInfo["Participant ID"]}_faceLoc_run-{run}_{expInfo["date"]}.csv'
logfile = open(dataName,'a',encoding='UTF8', newline='')

# write header if it is the first session
header_names = list(trialsReady[f'block-0'][0].keys())
writer_log = csv.DictWriter(logfile, fieldnames=header_names)
writer_log.writeheader()
#logfile.close()
fixTrial = copy.deepcopy(trialsReady[f'block-0'][0]) # to save fixation info
fixTrial['blockNr'] = 'Fixation'
fixTrial['trialNr'] = 0
fixTrial['condName'] = 'Fixation'
fixTrial['imageName'] = ''
fixTrial['catchTrial'] = ''


eventfile_info = {
    'onset' : '',
    'duration' : '',
    'trial_type' : ''}

# make a event file to save data with 'comma-separated-values'
eventName = f'{dataPath}/{expInfo["Participant ID"]}_task-funcLoc_run-{run}_events.csv'
eventfile = open(eventName, 'a',encoding='UTF8', newline='')
header_names = list(eventfile_info.keys())
writer_event = csv.DictWriter(eventfile, fieldnames=header_names)
writer_event.writeheader()
#eventfile.close()

#%% =============================================================================

win = visual.Window(size=scrsize, color='grey', units='pix', screen=2,fullscr=True)

instruct1 = 'During the experiment you\'ll see images appearing on the screen. \nPress a button as soon as you see the colour of the image turns slightly blue.\n\nIt is important to fixate on the fixation cross in the middle of the screen.\n\nPress a button to continue..'
instruct1 = visual.TextStim(win, height=32, text=instruct1)
instruct2 = 'The experiment is about to start!\nWaiting for scanner..'
instruct2 = visual.TextStim(win, height=32, text=instruct2)



#create fixation cross
fix1=visual.Line(win,start=(-500,-500),end=(500, 500),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
fix2=visual.Line(win,start=(-500,500),end=(500, -500),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')

win.mouseVisible = False

instruct1.draw()
win.flip()
keys = event.waitKeys(keyList=keyList)
escape_check(keys,win,logfile,eventfile)

instruct2.draw()
win.flip()
keys = event.waitKeys(keyList=['t','escape'])
escape_check(keys,win,logfile,eventfile)


#%% =============================================================================
# start stopwatch clock
clock = core.Clock()

fix1.setAutoDraw(True)
fix2.setAutoDraw(True)


fixStart = clock.getTime()
for nFrames in range(int(((fixStEn)*1000)/framelength)): #12sec
    keys = event.getKeys()
    escape_check(keys,win,logfile,eventfile)
    win.flip()

fixTrial['stimOnset'] = fixStart; fixTrial['stimOffset'] = clock.getTime(); fixTrial['stimDur'] = clock.getTime()-fixStart;
writer_log.writerow(fixTrial)
eventfile_info['onset'] = fixStart; eventfile_info['duration'] = clock.getTime(); eventfile_info['trial_type'] = 'fixation'
writer_event.writerow(eventfile_info)


response = []
corrResp = 0
catchStart = '' #so the code does not crash for keyCheck (only first call)
caught = 1
rt = None

for blocknr, block in enumerate(blocks):
    print(f'block {blocknr} - condition: {blocks[block][0]["condName"]}')
    blockStart = clock.getTime()
    for trial in blocks[block]:
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)

        trialOnsetTime = clock.getTime()

        if trial['catchTrial'] == True:
            col = colourChange
            catchStart = clock.getTime()
            if caught == 1:
                corrResp += 1
            caught = 0
        else:
            col = (1.0, 1.0, 1.0)

        im1 = Image.open(os.path.join(stimPath, trial['imageName']))
        bitmap = visual.ImageStim(win, size=[500,500],image=im1,color=col,mask='circle')

        for nFrames in range(trialFr): #500ms trail
            bitmap.draw()
            win.flip()
        for nFrames in range(isiFr): #500ms trail
            win.flip()

        # get response and it's associated timestamp as a list of tuples: (keypress, time)
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)

        trial['stimOnset'] = trialOnsetTime; trial['stimOffset'] = clock.getTime();  fixTrial['stimDur'] = clock.getTime()-trialOnsetTime; trial['rt'] = rt; rt = None
        writer_log.writerow(trial)

    ### fixation
    eventfile_info['onset'] = blockStart; eventfile_info['duration'] = clock.getTime()-blockStart; eventfile_info['trial_type'] = trial['condName']
    writer_event.writerow(eventfile_info)

    fixStart = clock.getTime()

    for nFrames in range(int((fixDur*1000)/framelength)): #10sec
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
        win.flip()

    fixTrial['stimOnset'] = fixStart; fixTrial['stimOffset'] = clock.getTime(); fixTrial['stimDur'] = clock.getTime()-fixStart;
    writer_log.writerow(fixTrial)
    eventfile_info['onset'] = fixStart; eventfile_info['duration'] = clock.getTime()-fixStart; eventfile_info['trial_type'] = 'fixation'
    writer_event.writerow(eventfile_info)

fixStart = clock.getTime()
for nFrames in range(int(((fixStEn-fixDur)*1000)/framelength)): #(it already did 10, so 2sec left)
    win.flip()

fixTrial['stimOnset'] = fixStart; fixTrial['stimOffset'] = clock.getTime(); fixTrial['stimDur'] = clock.getTime()-fixStart;
writer_log.writerow(fixTrial)
eventfile_info['onset'] = fixStart; eventfile_info['duration'] = clock.getTime()-fixStart; eventfile_info['trial_type'] = 'fixation'
writer_event.writerow(eventfile_info)


fix1.setAutoDraw(False)
fix2.setAutoDraw(False)
win.mouseVisible = True

timeExp = clock.getTime()
print(f'time exp: {int(timeExp/60)} min ({int(timeExp)} sec)')

maxCat = (int(len(nBlocks*conditions)/2))*2
endScore = (100/maxCat)*corrResp

instruct3 = f'Run {run}/02 done!\n\nYou\'ve detected {round(endScore)}% of the colour changes, great!'
instruct3 = visual.TextStim(win, height=32, text=instruct3)
instruct3.draw()
win.flip()
while not 'escape' in event.getKeys():
    core.wait(0.1)

# Quit the experiment (closing the window)
logfile.close()
eventfile.close()
win.close()
core.quit
